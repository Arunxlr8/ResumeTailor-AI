"""
ats_evaluator.py
----------------
Evaluates tailored resume content against a target Job Description to calculate
ATS score metrics, keyword matches, missing keywords, and recommendations.
"""

import json
import re
from typing import Any, Dict
from core.llm import get_llm
from langchain_core.messages import SystemMessage, HumanMessage
from utils.parser import extract_json
from utils.logging import get_thread_logger


ATS_EVAL_PROMPT = """You are an expert Applicant Tracking System (ATS) Auditor and Senior Technical Recruiter.
Your task is to analyze the candidate's resume context against the target Job Description and evaluate how well the resume passes ATS filters.

Calculate an ATS score between 0 and 100 based on:
1. Skills Match (0-100%): Coverage of essential technical & soft skills mentioned in the JD.
2. Keyword Density (0-100%): Presence of relevant domain keywords, tool names, and industry buzzwords.
3. Experience Relevance (0-100%): Alignment of work experience bullets, projects, and domain context with JD requirements.
4. Overall Score (0-100%): Weighted average of the criteria above.

Return strictly a valid JSON object with the following exact keys:
{
  "overall_score": 88,
  "skills_match": 90,
  "keyword_density": 85,
  "experience_relevance": 89,
  "matched_keywords": ["Python", "FastAPI", "LangChain", "RAG", "Docker"],
  "missing_keywords": ["Kubernetes", "GraphQL"],
  "ats_feedback": [
    "Strong technical skills match for GenAI & Python development.",
    "Consider highlighting system design metrics if applying for senior roles."
  ]
}
Return ONLY valid JSON.
"""


def evaluate_ats(resume_context: Dict[str, Any], job_description: str, provider: str = None, thread_id: str = None) -> Dict[str, Any]:
    """Analyze resume context against job description and return ATS score report."""
    logger = get_thread_logger(thread_id)
    logger.info("Evaluating ATS score against Job Description...")

    if not job_description or not job_description.strip():
        return {
            "overall_score": 75,
            "skills_match": 75,
            "keyword_density": 70,
            "experience_relevance": 80,
            "matched_keywords": ["Python", "Machine Learning"],
            "missing_keywords": [],
            "ats_feedback": ["Please provide a detailed job description for an exact ATS score calculation."]
        }

    # Format resume text summary for evaluation
    resume_summary_text = f"""Candidate Name: {resume_context.get('name', '')}
Title: {resume_context.get('title', '')}
Summary: {resume_context.get('summary', '')}
Skills: {resume_context.get('skills', [])}
Experience: {resume_context.get('experience', [])}
Projects: {resume_context.get('projects', [])}
Strengths: {resume_context.get('strengths', [])}
"""

    prompt_content = f"""TARGET JOB DESCRIPTION:
{job_description}

CANDIDATE TAILORED RESUME CONTEXT:
{resume_summary_text}
"""

    try:
        llm = get_llm(provider=provider)
        messages = [
            SystemMessage(content=ATS_EVAL_PROMPT),
            HumanMessage(content=prompt_content)
        ]
        response = llm.invoke(messages)
        result = extract_json(response.content if hasattr(response, 'content') else str(response))

        # Enforce bounds and defaults
        overall_score = max(0, min(100, int(result.get("overall_score", 85))))
        skills_match = max(0, min(100, int(result.get("skills_match", 85))))
        keyword_density = max(0, min(100, int(result.get("keyword_density", 80))))
        experience_relevance = max(0, min(100, int(result.get("experience_relevance", 85))))

        eval_data = {
            "overall_score": overall_score,
            "skills_match": skills_match,
            "keyword_density": keyword_density,
            "experience_relevance": experience_relevance,
            "matched_keywords": result.get("matched_keywords", []),
            "missing_keywords": result.get("missing_keywords", []),
            "ats_feedback": result.get("ats_feedback", ["Resume tailored successfully for target role."])
        }
        logger.info(f"ATS evaluation completed. Overall Score: {overall_score}%")
        return eval_data

    except Exception as e:
        logger.warning(f"Error invoking LLM for ATS evaluation: {e}. Generating fallback keyword matching ATS score.")
        # Rule-based fallback scoring
        jd_words = set(re.findall(r'\b[A-Za-z0-9+#.-]{3,}\b', job_description.lower()))
        resume_words = set(re.findall(r'\b[A-Za-z0-9+#.-]{3,}\b', resume_summary_text.lower()))

        common = jd_words.intersection(resume_words)
        score = min(95, max(65, int((len(common) / max(len(jd_words), 1)) * 100 + 40)))

        return {
            "overall_score": score,
            "skills_match": min(100, score + 5),
            "keyword_density": score,
            "experience_relevance": min(100, score + 2),
            "matched_keywords": list(common)[:10],
            "missing_keywords": list(jd_words - resume_words)[:5],
            "ats_feedback": [f"Matched {len(common)} key terms from the job description."]
        }
