"""Utility functions for extracting structured content from Large Language Model responses.

Provides helpers to parse JSON objects or Python code blocks out of LLM completions.
"""

import json
import re
from typing import Any, Dict


def extract_json(response: str) -> Dict[str, Any]:
    """Extract a structured JSON object from an LLM response text.

    Scans the response for braces and deserializes the JSON string.

    Parameters:
        response (str): The raw text response from the LLM.

    Returns:
        Dict[str, Any]: The parsed JSON object.

    Raises:
        ValueError: If no valid JSON substring is found.
    """
    match = re.search(r"\{.*\}", response, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in LLM response.")
    try:
        return json.loads(match.group())
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse extracted JSON block: {str(e)}") from e


def extract_python(response: str) -> str:
    """Extract Python source code from markdown python blocks.

    Finds content between ```python and ``` block delimiters, falling back
    to returning the stripped response if no code block delimiters are found.

    Parameters:
        response (str): The raw markdown or text response from the LLM.

    Returns:
        str: The extracted Python script code.
    """
    match = re.search(r"```python(.*?)```", response, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return response.strip()


def clean_llm_output(response: str) -> str:
    """Clean surrounding whitespace from raw LLM output.

    Parameters:
        response (str): The raw LLM response.

    Returns:
        str: The stripped response.
    """
    return response.strip()