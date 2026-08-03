"""LLM provider initialization module.

Provides a function to retrieve the configured Large Language Model instance
based on AppSettings or explicit runtime provider choice.
"""

from functools import lru_cache
import os
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from langchain_ollama import ChatOllama
from core.config import settings
from core.providers import Provider


def get_llm(provider: str = None) -> BaseChatModel:
    """Return a chat model instance based on the specified provider or default settings."""
    prov = (provider or settings.LLM_PROVIDER or "azure").lower().strip()

    if prov == Provider.AZURE.value:
        return AzureChatOpenAI(
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            azure_deployment=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
            temperature=0
        )
    if prov == Provider.OLLAMA.value:
        return ChatOllama(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.OLLAMA_MODEL,
            temperature=0
        )
    if prov == Provider.LMSTUDIO.value:
        return ChatOpenAI(
            base_url=settings.LMSTUDIO_BASE_URL,
            api_key="lm-studio",
            model=settings.LMSTUDIO_MODEL,
            temperature=0
        )
    if prov == "openai":
        api_key = os.getenv("OPENAI_API_KEY", "sk-placeholder")
        return ChatOpenAI(
            api_key=api_key,
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=0
        )

    # Fallback to Azure if configured, or default ChatOpenAI
    try:
        return AzureChatOpenAI(
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            azure_deployment=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
            temperature=0
        )
    except Exception:
        return ChatOllama(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.OLLAMA_MODEL,
            temperature=0
        )