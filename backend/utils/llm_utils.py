"""Large Language Model helper utilities.

Exposes a function to format system and user prompt strings into messages
and invoke the configured LangChain chat model.
"""

from langchain_core.messages import HumanMessage, SystemMessage
from core.llm import get_llm


def invoke_llm(system_prompt: str, user_prompt: str) -> str:
    """Format and invoke the configured LLM with system and user messages.

    Parameters:
        system_prompt (str): Text prompt specifying the agent's role and rules.
        user_prompt (str): Input text context for the agent to process.

    Returns:
        str: Content string of the model's completion response.
    """
    llm = get_llm()
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ])
    return str(response.content)