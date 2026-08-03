"""Defines the supported Large Language Model providers.

Exposes the Provider StrEnum used in configuration parsing and LLM instantiation.
"""

from enum import Enum


class Provider(str, Enum):

    """Enumeration of supported Large Language Model providers.

    Members:
        AZURE: Microsoft Azure OpenAI.
        OLLAMA: Locally hosted Ollama models.
        LMSTUDIO: Local server hosting API-compatible models via LM Studio.
    """

    AZURE = "azure"
    OLLAMA = "ollama"
    LMSTUDIO = "lmstudio"