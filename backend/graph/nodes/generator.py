"""Generator node in the LangGraph workflow.

Builds the final resume context parameters from approved skills and user suggestions,
executes the parametric generate_resume tool script, and evaluates the ATS match score.
"""

from pathlib import Path
from core.config import settings
from graph.state import ResumeGraphState
from services.ats_evaluator import evaluate_ats
from templates.generate_resume import generate_resume, DEFAULT_CONTEXT
from utils.logging import get_thread_logger
import copy


def generator_node(state: ResumeGraphState) -> ResumeGraphState:
    """Generate resume DOCX file using parametric generator script and compute ATS score."""
    thread_id = state["thread_id"]
    logger = get_thread_logger(thread_id)

    logger.info(f"[{thread_id}] Node: generator | Building resume context parameters...")

    approved_skills = state.get("approved_skills") or []
    user_suggestions = state.get("user_suggestions") or ""
    planner_output = state.get("planner_output") or {}
    job_description = state.get("job_description", "")
    provider = state.get("llm_provider")

    # Clone base template context
    context = copy.deepcopy(DEFAULT_CONTEXT)

    # Incorporate approved skills seamlessly into the 6 category blocks
    if approved_skills:
        approved_set = set(approved_skills)
        # Combine approved skills into technical categories
        context["skills"] = [
            ("Agentic AI & Frameworks: ", ", ".join(list(approved_set.intersection({
                "Google ADK", "LangChain", "LangGraph", "Multi-Agent Orchestration",
                "HITL Workflows", "Custom Tools", "MCP (Model Context Protocol)", "Orchestrator-Agent Pattern"
            })) or ["Google ADK (Agent Development Kit), LangChain, LangGraph, Multi-Agent Orchestration, HITL Workflows, Custom Tools, MCP"])),

            ("GenAI & LLM: ", ", ".join(list(approved_set.intersection({
                "LLM", "RAG", "Prompt Engineering", "Structured Outputs", "Embeddings",
                "Semantic Search", "Hallucination Detection", "Ollama", "vLLM", "Hugging Face"
            })) or ["LLM, RAG, Prompt Engineering (Few-Shot, System Prompts), Structured Outputs, Embeddings, Semantic Search, Ollama, vLLM"])),

            ("DS & ML: ", ", ".join(list(approved_set.intersection({
                "Scikit-learn", "Pandas", "NumPy", "Similarity Search", "Defect Classification",
                "Cosine Similarity", "Statistical Validation", "Data Preprocessing", "Anomaly Detection"
            })) or ["Scikit-learn, Pandas, NumPy, Similarity Search, Defect Classification, Cosine Similarity, Statistical Validation, Preprocessing"])),

            ("Vector DBs & RAG: ", ", ".join(list(approved_set.intersection({
                "ChromaDB", "FAISS", "Vector Databases", "Custom Chunking", "RAG Document Indexing",
                "Semantic Retrieval", "Hybrid Retrieval", "Embedding Models"
            })) or ["ChromaDB, FAISS, Vector Databases, Custom Chunking, RAG Document Indexing, Semantic Retrieval, Hybrid Indexing"])),

            ("Programming & Frameworks: ", ", ".join(list(approved_set.intersection({
                "Python", "Python (OOP)", "FastAPI", "Flask", "React", "PyTest", "SQLite", "REST APIs", "Selenium", "JIRA Integration"
            })) or ["Python (OOP), FastAPI, Flask, React, PyTest, SQLite, REST APIs, Selenium, JIRA Integration"])),

            ("DevOps & Key Tools: ", ", ".join(approved_set - {
                "Google ADK", "LangChain", "LangGraph", "Multi-Agent Orchestration", "HITL Workflows", "Custom Tools", "MCP",
                "LLM", "RAG", "Prompt Engineering", "Structured Outputs", "Embeddings", "Semantic Search", "Ollama", "vLLM",
                "Scikit-learn", "Pandas", "NumPy", "Similarity Search", "ChromaDB", "FAISS", "Python", "FastAPI", "Flask", "React"
            }) or "Docker, Git, GitHub, Jenkins, Azure DevOps, LM Studio, ECU Test (Tracetronics), Object API (RPC), CANoe")
        ]

    # Incorporate tailored summary if available
    tailored_summary = planner_output.get("tailored_summary")
    if tailored_summary:
        context["summary"] = tailored_summary

    # Ensure generated directory exists
    output_filename = state.get("generated_resume_filename") or f"{thread_id}.docx"
    output_path = settings.GENERATED_RESUME_DIR / output_filename

    try:
        logger.info(f"[{thread_id}] Node: generator | Triggering generate_resume script tool...")
        saved_path = generate_resume(context=context, output_path=str(output_path))
        logger.info(f"[{thread_id}] Node: generator | Resume created successfully at: {saved_path}")

        # Compute ATS Score Evaluation
        ats_result = evaluate_ats(
            resume_context=context,
            job_description=job_description,
            provider=provider,
            thread_id=thread_id
        )

        state["tailored_context"] = context
        state["generated_resume_path"] = saved_path
        state["ats_score_result"] = ats_result
        state["execution_success"] = True
        state["execution_error"] = None

    except Exception as exc:
        err_msg = f"Failed to generate resume DOCX: {exc}"
        logger.error(f"[{thread_id}] {err_msg}")
        state["execution_success"] = False
        state["execution_error"] = err_msg

    return state