"""File service to handle file uploads and save them to disk.

Saves FastAPI UploadFile objects to designated folders securely.
"""

from pathlib import Path
import shutil
from fastapi import UploadFile


def save_uploaded_file(file: UploadFile, directory: str) -> str:
    """Save an uploaded FastAPI file to the specified target directory.

    Creates the destination directory if it doesn't already exist.

    Parameters:
        file (UploadFile): The uploaded file object from FastAPI.
        directory (str): The target directory path.

    Returns:
        str: Path of the saved file as a string.
    """
    dest_dir = Path(directory)
    dest_dir.mkdir(parents=True, exist_ok=True)
    destination = dest_dir / (file.filename or "uploaded_file")
    with open(destination, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return str(destination)