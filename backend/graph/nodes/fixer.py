"""Fixer node in the LangGraph workflow.

Responsible for taking a failed Python resume creation script, reading its execution
errors (stdout, stderr, traceback), and querying the LLM using the FIXER_PROMPT to
repair the script.
"""

from graph.state import ResumeGraphState
from prompts.fixer_prompt import FIXER_PROMPT
from utils.llm_utils import invoke_llm
from utils.parser import extract_python
from utils.logging import get_thread_logger


def fixer_node(state: ResumeGraphState) -> ResumeGraphState:
    """Repair the generated Python script using execution error context.

    Invokes the LLM to patch the broken python code using captured stdout, stderr,
    and Python traceback. Increments retry count on state.

    Parameters:
        state (ResumeGraphState): The shared graph state.

    Returns:
        ResumeGraphState: The updated graph state containing the patched python script.
    """
    thread_id = state["thread_id"]
    logger = get_thread_logger(thread_id)

    current_retry = state.get("retry_count", 0)
    logger.info(
        f"[{thread_id}] Node: fixer | "
        f"State keys: {list(state.keys())} | "
        f"Retry count: {current_retry} | "
        f"Status: starting"
    )

    fixer_input = f"""Resume Plan:
{state["planner_output"]}

Generated Python Script:
```python
{state["generated_script"]}
```

Execution stdout:
{state.get("execution_stdout", "")}

Execution stderr:
{state.get("execution_error", "")}

Execution traceback:
{state.get("execution_traceback", "")}
"""

    try:
        logger.info(f"[{thread_id}] Node: fixer | Requesting repaired script from LLM...")
        raw_response = invoke_llm(
            system_prompt=FIXER_PROMPT,
            user_prompt=fixer_input
        )
        fixed_script = extract_python(raw_response)
    except Exception as e:
        logger.error(
            f"[{thread_id}] Node: fixer | "
            f"Error occurred during script repair: {str(e)} | "
            f"Status: failed"
        )
        raise

    # Update state with the fixed script and increment retry count
    new_state = dict(state)
    new_state["generated_script"] = fixed_script
    new_state["retry_count"] = current_retry + 1

    logger.info(
        f"[{thread_id}] Node: fixer | "
        f"State keys: {list(new_state.keys())} | "
        f"Retry count: {new_state['retry_count']} | "
        f"Result: script repaired, length {len(fixed_script)} | "
        f"Status: completed"
    )

    return new_state