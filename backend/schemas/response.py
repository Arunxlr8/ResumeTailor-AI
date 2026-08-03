"""Pydantic response schemas for API responses.

Defines schemas returned by workflow startup, resumption, and status endpoints.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class WorkflowResponse(BaseModel):

    """Response payload returned by workflow execution endpoints.

    Attributes:
        status (str): Outcome status of the request (e.g. 'success').
        thread_id (str): The unique identifier of the workflow execution thread.
        is_interrupted (bool): Indicates if the workflow is currently paused awaiting human review.
        next_nodes (List[str]): List of node names that will execute next.
        pending_interrupt (Optional[List[Dict[str, Any]]]): Struct of interrupts waiting for user action.
        result (Dict[str, Any]): Dictionary of state variables returned from execution.
        current_stage (str): The node or stage currently being processed.
        next_stage (str): The subsequent node or stage in the graph.
        execution_success (bool): Whether the script was executed successfully.
        execution_error (Optional[str]): Error text if script execution failed.
        generated_resume_path (Optional[str]): Filepath to the generated DOCX resume.
        generated_script_path (Optional[str]): Filepath to the generated Python script.
    """

    status: str = Field(description="Request operation status.")
    thread_id: str = Field(description="Unique workflow thread identifier.")
    is_interrupted: bool = Field(description="Flag denoting if workflow is halted for review.")
    next_nodes: List[str] = Field(description="List of upcoming graph node execution targets.")
    pending_interrupt: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Metadata list of outstanding interrupts."
    )
    result: Dict[str, Any] = Field(description="State outputs and variables.")
    current_stage: str = Field(description="Current stage of the resume tailoring workflow.")
    next_stage: str = Field(description="Next stage of the resume tailoring workflow.")
    execution_success: bool = Field(description="Whether the Python script run succeeded.")
    execution_error: Optional[str] = Field(default=None, description="Detailed stderr if script execution failed.")
    generated_resume_path: Optional[str] = Field(default=None, description="Filepath to the final docx file.")
    generated_script_path: Optional[str] = Field(default=None, description="Filepath to the final resume script.")