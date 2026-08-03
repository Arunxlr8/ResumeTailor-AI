"""Centralized logging utility for the Agentic Resume Tailor backend.

Provides functions to retrieve or configure thread-specific loggers that log
to both the console and dynamically generated files under logs/{thread_id}.log.
"""

import logging
import os
from pathlib import Path
from core.config import settings


def get_thread_logger(thread_id: str | None) -> logging.Logger:
    """Retrieve or create a logger for a specific workflow thread ID.

    Logs are written to the console and to a file named logs/{thread_id}.log.
    If thread_id is None or empty, returns a default backend logger.

    Parameters:
        thread_id (str | None): The unique identifier of the workflow thread.

    Returns:
        logging.Logger: The configured Logger instance.
    """
    if not thread_id:
        return logging.getLogger("backend_default")

    logger_name = f"thread_{thread_id}"
    logger = logging.getLogger(logger_name)

    # Prevent duplicate handlers if the logger has already been initialized
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # Ensure logs directory exists
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / f"{thread_id}.log"

    # Create file handler
    try:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.INFO)
    except Exception:
        # Fallback to stream logging if file logging fails
        file_handler = None

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Formatter configuration
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if file_handler:
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Prevent propagating to the root logger to avoid duplicated logs
    logger.propagate = False

    return logger
