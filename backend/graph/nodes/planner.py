"""Planner node in the LangGraph workflow.

Extracts current skills from existing resume, identifies missing supporting skills
and keywords from the job description, builds candidate context, and pauses for
Human-in-the-Loop (HITL) approval where the user can toggle/add/remove skills and add feedback.
"""

from typing import Any, Dict, List
from langgraph.types import interrupt
from core.llm import get_llm
from graph.state import ResumeGraphState
from langchain_core.messages import SystemMessage, HumanMessage
from utils.parser import extract_json
from utils.logging import get_thread_logger


SKILL_EXTRACTION_PROMPT = """You are an expert Resume Analyst and Recruiter.
Given an Existing Resume and a target Job Description, perform two tasks:
1. Extract current candidate skills and key technical domain competencies from the existing resume.
2. Identify high-value missing supporting skills, tools, frameworks, and keywords mentioned in or relevant to the Job Description that should be incorporated into the candidate's resume.
3. Draft an updated professional summary tailored to the job post.

Return strictly a JSON object with this exact shape:
{
  "extracted_skills": ["Python", "LangChain", "FastAPI", "Docker", "RAG"],
  "suggested_skills": ["Google ADK", "MCP", "vLLM", "ChromaDB", "Multi-Agent Orchestration"],
  "tailored_summary": "GenAI Engineer with 3+ years of experience specializing in Large Language Models, Agentic AI, RAG pipelines, and multi-agent workflows..."
}
Return ONLY valid JSON.
"""


def planner_node(state: ResumeGraphState) -> ResumeGraphState:
    """Analyze resume & JD, extract current skills, suggest supporting keywords, and await HITL review."""
    thread_id = state["thread_id"]
    logger = get_thread_logger(thread_id)
    provider = state.get("llm_provider")

    logger.info(f"[{thread_id}] Node: planner | Extracting skills and matching JD keywords...")

    resume_text = state.get("resume_text", "")
    job_description = state.get("job_description", "")

    # Invoke LLM for extraction
    try:
        llm = get_llm(provider=provider)
        prompt_content = f"JOB DESCRIPTION:\n{job_description}\n\nEXISTING RESUME:\n{resume_text}"
        messages = [
            SystemMessage(content=SKILL_EXTRACTION_PROMPT),
            HumanMessage(content=prompt_content)
        ]
        response = llm.invoke(messages)
        res_json = extract_json(response.content if hasattr(response, 'content') else str(response))

        extracted_skills = res_json.get("extracted_skills", [])
        suggested_skills = res_json.get("suggested_skills", [])
        tailored_summary = res_json.get("tailored_summary", "")
    except Exception as e:
        logger.warning(f"[{thread_id}] LLM extraction fallback triggered: {e}")
        extracted_skills = ["Python", "FastAPI", "LangChain", "RAG", "Docker", "React"]
        suggested_skills = ["Google ADK", "MCP", "vLLM", "Multi-Agent Orchestration", "ChromaDB"]
        tailored_summary = "Experienced GenAI Engineer skilled in building scalable LLM solutions, RAG pipelines, and full-stack AI applications."

    planner_output = {
        "extracted_skills": extracted_skills,
        "suggested_skills": suggested_skills,
        "tailored_summary": tailored_summary,
    }

    # Trigger HITL Interrupt for human reviewer
    logger.info(f"[{thread_id}] Node: planner | Pausing for Human-in-the-Loop approval...")
    decision = interrupt(
        {
            "stage": "planner",
            "title": "Skills & Keyword Approval",
            "message": "Review extracted skills, approve/add/remove keywords, and provide suggestions.",
            "output": {
                "extracted_skills": extracted_skills,
                "suggested_skills": suggested_skills,
                "tailored_summary": tailored_summary
            }
        }
    )

    logger.info(f"[{thread_id}] Node: planner | Decision received: {decision.get('type')}")

    # Process approved skills & feedback from decision payload
    approved_skills = decision.get("approved_skills") or (extracted_skills + suggested_skills)
    user_suggestions = decision.get("user_suggestions") or decision.get("feedback") or ""

    state["extracted_skills"] = extracted_skills
    state["suggested_skills"] = suggested_skills
    state["approved_skills"] = approved_skills
    state["user_suggestions"] = user_suggestions
    state["planner_output"] = planner_output

    logger.info(f"[{thread_id}] Node: planner | Completed. Approved {len(approved_skills)} skills.")
    return state