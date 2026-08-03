"""Executor node in the LangGraph workflow.

Responsible for running the approved Python script using the python_executor module
and recording the output metrics (stdout, stderr, traceback) inside the shared state.
"""

import os
from executor.python_executor import execute_script
from graph.state import ResumeGraphState
from utils.logging import get_thread_logger


def executor_node(state: ResumeGraphState) -> ResumeGraphState:
    """Execute the generated Python resume script and capture execution outputs.

    Constructs the expected resume file path, executes the script, and updates the
    shared state with execution results.

    Parameters:
        state (ResumeGraphState): The shared graph state.

    Returns:
        ResumeGraphState: The updated graph state containing execution outcome details.
    """
    thread_id = state["thread_id"]
    logger = get_thread_logger(thread_id)

    retry_count = state.get("retry_count", 0)
    logger.info(
        f"[{thread_id}] Node: executor | "
        f"State keys: {list(state.keys())} | "
        f"Retry count: {retry_count} | "
        f"Status: starting"
    )

    # Determine expected resume output file
    expected_resume_path = None
    if state.get("generated_resume_filename"):
        expected_resume_path = os.path.join("generated", "resumes", state["generated_resume_filename"])

    logger.info(f"[{thread_id}] Node: executor | Running script. Expected resume destination: {expected_resume_path}")

    # Run the script using the subprocess executor
    success, stdout, stderr, traceback_str, resume_path, script_path = execute_script(
        script=state["generated_script"],
        expected_resume_path=expected_resume_path,
        thread_id=thread_id
    )

    # Create a new dictionary to prevent mutating in-place or returning invalid state structure
    new_state = dict(state)
    new_state["execution_success"] = success
    new_state["execution_stdout"] = stdout
    new_state["execution_error"] = stderr
    new_state["execution_traceback"] = traceback_str
    new_state["generated_resume_path"] = resume_path
    new_state["generated_script_path"] = script_path

    logger.info(
        f"[{thread_id}] Node: executor | "
        f"State keys: {list(new_state.keys())} | "
        f"Retry count: {retry_count} | "
        f"Result: Success={success}, Error={stderr} | "
        f"Status: completed"
    )

    return new_state