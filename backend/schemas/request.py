"""Pydantic request schemas for API payloads.

Defines schemas for starting, resuming, or querying the resume tailoring workflow.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class WorkflowResumeRequest(BaseModel):

    """Request payload schema for resuming an interrupted workflow stage.

    Attributes:
        thread_id (str): The unique identifier of the workflow execution thread.
        decision (str): User approval choice (e.g. 'approve', 'regenerate').
        feedback (Optional[str]): Reviewer feedback to apply if regenerating.
        approved_skills (Optional[List[str]]): List of approved skills.
        added_skills (Optional[List[str]]): Additional skills added by human reviewer.
        removed_skills (Optional[List[str]]): Skills removed by human reviewer.
        user_suggestions (Optional[str]): Custom instructions from human reviewer.
    """

    thread_id: str = Field(description="Unique workflow thread identifier.")
    decision: str = Field(description="Action decision (e.g., 'approve' or 'regenerate').")
    feedback: Optional[str] = Field(default=None, description="Optional text feedback.")
    approved_skills: Optional[List[str]] = Field(default=None, description="List of approved skills.")
    added_skills: Optional[List[str]] = Field(default=None, description="Skills added by reviewer.")
    removed_skills: Optional[List[str]] = Field(default=None, description="Skills removed by reviewer.")
    user_suggestions: Optional[str] = Field(default=None, description="Custom suggestions or feedback.")