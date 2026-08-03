"""Workflow API endpoints for the Agentic Resume Tailor backend.

Exposes endpoints to start workflows, resume workflow interrupts, query state,
and download generated resume files securely.
"""

from pathlib import Path
import traceback
from uuid import uuid4

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from langgraph.types import Command

from core.config import settings
from graph.builder import build_graph
from schemas.request import WorkflowResumeRequest
from services.file_service import save_uploaded_file
from services.resume_parser import parse_resume
from utils.logging import get_thread_logger


workflow_graph = build_graph()
router = APIRouter(prefix="/workflow", tags=["Workflow"])


def _extract_interrupts(state) -> list:
    """Return pending interrupts from state snapshot."""
    interrupts = []
    if not hasattr(state, "tasks"):
        return interrupts
    for task in state.tasks:
        if not hasattr(task, "interrupts"):
            continue
        for interrupt in task.interrupts:
            interrupts.append({
                "id": getattr(interrupt, "id", None),
                "value": getattr(interrupt, "value", None),
                "resumable": getattr(interrupt, "resumable", None),
            })
    return interrupts


def _get_stage_info(state) -> dict:
    """Derive stage metadata and state attributes."""
    next_nodes = list(state.next) if state.next else []
    next_stage = next_nodes[0] if next_nodes else "completed"
    values = state.values or {}

    if not values.get("approved_skills") and len(next_nodes) > 0:
        current_stage = "planner"
    elif values.get("generated_resume_path"):
        current_stage = "completed"
    else:
        current_stage = "generator" if len(next_nodes) > 0 else "completed"

    return {
        "current_stage": current_stage,
        "next_stage": next_stage,
        "execution_success": values.get("execution_success", False),
        "execution_error": values.get("execution_error"),
        "generated_resume_path": values.get("generated_resume_path"),
        "ats_score_result": values.get("ats_score_result"),
        "extracted_skills": values.get("extracted_skills", []),
        "suggested_skills": values.get("suggested_skills", []),
        "approved_skills": values.get("approved_skills", []),
    }


def _build_response(thread_id: str, state, result=None) -> dict:
    """Assemble standard API response from LangGraph snapshot."""
    stage_info = _get_stage_info(state)
    return {
        "status": "success",
        "thread_id": thread_id,
        "is_interrupted": len(state.next) > 0,
        "next_nodes": list(state.next),
        "pending_interrupt": _extract_interrupts(state),
        "result": result,
        **stage_info,
    }


def _validate_download_file(path_str: str | None, allowed_dirs: list[Path]) -> Path:
    """Validate file path before streaming response."""
    if not path_str:
        raise HTTPException(status_code=404, detail="File path not found in workflow state.")

    path = Path(path_str).resolve()
    if not path.exists() or not path.is_file():
        raise HTTPException(status_code=404, detail="Requested file does not exist on disk.")

    inside_allowed = any(
        directory.resolve() in path.parents or path.parent == directory.resolve()
        for directory in allowed_dirs
    )
    if not inside_allowed:
        raise HTTPException(status_code=400, detail="Access denied: file resides outside authorised directories.")

    return path


def _assert_thread_exists(thread_id: str) -> None:
    config = {"configurable": {"thread_id": thread_id}}
    state = workflow_graph.get_state(config)
    if not state.values:
        raise HTTPException(
            status_code=400,
            detail=f"No active workflow found for thread_id '{thread_id}'. Start a workflow first via POST /workflow/start."
        )


@router.post("/start")
async def start_workflow(
    job_description: str = Form(...),
    provider: str = Form(default="azure"),
    resume: UploadFile | None = File(default=None),
    template: UploadFile | None = File(default=None),
):
    """Start the resume tailoring workflow."""
    thread_id = uuid4().hex
    logger = get_thread_logger(thread_id)
    logger.info(f"[{thread_id}] Starting workflow. Provider: {provider}")

    # Validate file extension if provided
    if resume:
        ext = Path(resume.filename or "").suffix.lower()
        if ext not in {".docx", ".pdf", ".txt"}:
            raise HTTPException(status_code=400, detail=f"Unsupported resume extension '{ext}'. Allowed: .docx, .pdf, .txt")

    resume_text = ""
    template_path = ""

    try:
        if resume:
            resume_path = save_uploaded_file(resume, "uploads/resumes")
            resume_text = parse_resume(resume_path, thread_id=thread_id)

        if template:
            template_path = save_uploaded_file(template, "uploads/templates")

        initial_state = {
            "thread_id": thread_id,
            "job_description": job_description,
            "resume_text": resume_text,
            "llm_provider": provider,
            "template_path": template_path,
            "generated_resume_filename": f"{thread_id}.docx",
            "extracted_skills": [],
            "suggested_skills": [],
            "approved_skills": [],
            "user_suggestions": "",
            "planner_output": None,
            "tailored_context": None,
            "generated_resume_path": None,
            "ats_score_result": None,
            "execution_success": False,
            "execution_error": None,
            "retry_count": 0,
        }

        config = {"configurable": {"thread_id": thread_id}}
        result = workflow_graph.invoke(initial_state, config=config)
        state = workflow_graph.get_state(config)

        return _build_response(thread_id, state, result)

    except HTTPException:
        raise
    except Exception as exc:
        msg = f"Failed to start workflow: {exc}"
        logger.error(f"[{thread_id}] {msg}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=msg)


@router.post("/resume")
async def resume_workflow(request: WorkflowResumeRequest):
    """Resume workflow after HITL approval or modifications."""
    if not request.thread_id or not request.thread_id.strip():
        raise HTTPException(status_code=400, detail="thread_id is required.")

    thread_id = request.thread_id.strip()
    logger = get_thread_logger(thread_id)
    _assert_thread_exists(thread_id)

    decision = request.decision.lower().strip()
    resume_payload: dict = {
        "type": decision,
        "approved_skills": request.approved_skills,
        "added_skills": request.added_skills,
        "removed_skills": request.removed_skills,
        "user_suggestions": request.user_suggestions or request.feedback,
        "feedback": request.feedback,
    }

    config = {"configurable": {"thread_id": thread_id}}

    try:
        logger.info(f"[{thread_id}] Resuming graph with decision payload.")
        result = workflow_graph.invoke(Command(resume=resume_payload), config=config)
        state_after = workflow_graph.get_state(config)
        return _build_response(thread_id, state_after, result)

    except HTTPException:
        raise
    except Exception as exc:
        msg = f"Failed to resume workflow: {exc}"
        logger.error(f"[{thread_id}] {msg}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=msg)


@router.get("/state/{thread_id}")
async def get_workflow_state(thread_id: str):
    """Retrieve current snapshot of workflow state."""
    logger = get_thread_logger(thread_id)
    config = {"configurable": {"thread_id": thread_id}}
    try:
        state = workflow_graph.get_state(config)
        if not state.values:
            raise HTTPException(status_code=400, detail=f"No state found for thread '{thread_id}'.")

        response = _build_response(thread_id, state)
        response["values"] = state.values
        return response

    except HTTPException:
        raise
    except Exception as exc:
        msg = f"Failed to fetch state for thread '{thread_id}': {exc}"
        logger.error(f"[{thread_id}] {msg}")
        raise HTTPException(status_code=500, detail=msg)


@router.get("/download/resume/{thread_id}")
async def download_resume(thread_id: str):
    """Download generated DOCX resume."""
    logger = get_thread_logger(thread_id)
    config = {"configurable": {"thread_id": thread_id}}
    try:
        state = workflow_graph.get_state(config)
        path = (state.values or {}).get("generated_resume_path")

        if not path:
            raise HTTPException(status_code=404, detail="Resume has not been generated yet.")

        valid_path = _validate_download_file(path, [settings.GENERATED_RESUME_DIR])
        return FileResponse(
            str(valid_path),
            filename=f"Tailored_Resume_{thread_id[:8]}.docx",
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

    except HTTPException:
        raise
    except Exception as exc:
        msg = f"Error during resume download: {exc}"
        logger.error(f"[{thread_id}] {msg}")
        raise HTTPException(status_code=500, detail=msg)
