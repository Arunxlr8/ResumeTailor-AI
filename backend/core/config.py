"""Application configuration management.

Loads and validates application settings from the environment variables or from
the backend/.env configuration file.
"""

import os
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Dynamically locate the backend directory and the .env file path
_backend_dir = Path(__file__).resolve().parents[1]
_env_file_path = _backend_dir / ".env"


class AppSettings(BaseSettings):

    """Application configuration settings parsed and validated using Pydantic.

    Attributes:
        PROJECT_NAME (str): Name of the project.
        PROJECT_VERSION (str): Current version of the project.
        API_PREFIX (str): Routing prefix for API endpoints.
        LLM_PROVIDER (str): LLM provider to use (e.g. 'azure', 'ollama', 'lmstudio').
        AZURE_OPENAI_ENDPOINT (str): Azure OpenAI API endpoint url.
        AZURE_OPENAI_API_VERSION (str): Azure OpenAI api version.
        AZURE_OPENAI_DEPLOYMENT_NAME (str): Azure model deployment name.
        AZURE_OPENAI_API_KEY (str): Azure API authorization key.
        OLLAMA_BASE_URL (str): Local URL for the Ollama server.
        OLLAMA_MODEL (str): Model tag to execute on the Ollama server.
        LMSTUDIO_BASE_URL (str): Local URL for the LM Studio server.
        LMSTUDIO_MODEL (str): Model tag to execute on the LM Studio server.
        MAX_RETRY_COUNT (int): Limit of automatic script fixing attempts.
        LOG_LEVEL (str): Log granularity level.
        BASE_DIR (Path): Reference path of the backend directory.
        GENERATED_RESUME_DIR (Path): Output directory for generated resumes.
        GENERATED_SCRIPT_DIR (Path): Output directory for temporary python scripts.
        TEMPLATE_DIR (Path): Directory for storing document templates.
        UPLOAD_DIR (Path): Directory for saved files.
        STATIC_DIR (Path): Directory for static frontend/assets.
        LOG_DIR (Path): Directory for thread logs.
    """

    model_config = SettingsConfigDict(
        env_file=str(_env_file_path),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    PROJECT_NAME: str = Field(default="Agentic Resume Tailor", description="Application name.")
    PROJECT_VERSION: str = Field(default="1.0.0", description="Application version.")
    API_PREFIX: str = Field(default="/api/v1", description="API route prefix.")
    LLM_PROVIDER: str = Field(default="azure", description="LLM provider to use.")
    AZURE_OPENAI_ENDPOINT: str = Field(description="Azure OpenAI endpoint.")
    AZURE_OPENAI_API_VERSION: str = Field(description="Azure OpenAI API version.")
    AZURE_OPENAI_DEPLOYMENT_NAME: str = Field(description="Azure deployment name.")
    AZURE_OPENAI_API_KEY: str = Field(description="Azure OpenAI API key.")
    OLLAMA_BASE_URL: str = Field(default="http://localhost:11434", description="Ollama server URL.")
    OLLAMA_MODEL: str = Field(default="llama3.1", description="Ollama model name.")
    LMSTUDIO_BASE_URL: str = Field(default="http://localhost:1234/v1", description="LM Studio endpoint.")
    LMSTUDIO_MODEL: str = Field(default="local-model", description="LM Studio model name.")
    MAX_RETRY_COUNT: int = Field(default=3, description="Maximum retry attempts for code fixing.")
    LOG_LEVEL: str = Field(default="INFO", description="Application log level.")

    BASE_DIR: Path = _backend_dir
    GENERATED_RESUME_DIR: Path = _backend_dir / "generated" / "resumes"
    GENERATED_SCRIPT_DIR: Path = _backend_dir / "generated" / "scripts"
    TEMPLATE_DIR: Path = _backend_dir / "templates"
    UPLOAD_DIR: Path = _backend_dir / "uploads"
    STATIC_DIR: Path = _backend_dir / "static"
    LOG_DIR: Path = _backend_dir / "logs"


settings = AppSettings()