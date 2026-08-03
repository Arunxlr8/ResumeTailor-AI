"""Executes generated Python scripts to construct docx resumes.

Leverages the Python interpreter in the current virtual environment (sys.executable)
to safely run scripts in a subprocess, capturing output, errors, and tracebacks.
"""

import os
import subprocess
import sys
import traceback
import uuid
from pathlib import Path
from utils.logging import get_thread_logger


def execute_script(
    script: str,
    expected_resume_path: str | None = None,
    thread_id: str | None = None
) -> tuple[bool, str | None, str | None, str | None, str | None, str | None]:
    """Execute the generated Python script in a subprocess.

    Creates a temporary script file on disk, runs it using the current
    Python executable, captures and validates output files, and handles failures.

    Parameters:
        script (str): The Python script code to execute.
        expected_resume_path (str | None): Expected path to check for the generated resume docx.
        thread_id (str | None): Optional thread ID to log progress and errors to thread log.

    Returns:
        tuple[bool, str | None, str | None, str | None, str | None, str | None]:
            A tuple of:
            - success (bool): True if script executed and generated file successfully.
            - stdout (str | None): captured stdout from execution.
            - stderr (str | None): captured stderr from execution.
            - traceback_str (str | None): captured python traceback from execution or errors.
            - resume_path (str | None): Filepath to the generated resume docx on success.
            - script_path (str | None): Filepath to the executed python script.
    """
    logger = get_thread_logger(thread_id)

    script_dir = Path("generated/scripts")
    resume_dir = Path("generated/resumes")
    script_dir.mkdir(parents=True, exist_ok=True)
    resume_dir.mkdir(parents=True, exist_ok=True)

    script_filename = f"{uuid.uuid4().hex}.py"
    script_path = script_dir / script_filename

    logger.info(f"Saving generated script to {script_path}")

    # Write the script code to disk
    try:
        with open(script_path, "w", encoding="utf-8") as file:
            file.write(script)
    except Exception as e:
        error_msg = f"Failed to write script to disk: {str(e)}"
        tb = traceback.format_exc()
        logger.error(f"{error_msg}\n{tb}")
        return False, None, error_msg, tb, None, str(script_path)

    # Validate that the generated script actually exists on disk
    if not script_path.exists():
        error_msg = f"Generated script file does not exist on disk: {script_path}"
        logger.error(error_msg)
        return False, None, error_msg, None, None, str(script_path)

    logger.info(f"Executing python script using: {sys.executable}")

    try:
        # Run script in a subprocess with a timeout to prevent hang-ups
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=Path.cwd(),
            capture_output=True,
            text=True,
            timeout=30
        )

        stdout = result.stdout
        stderr = result.stderr
        returncode = result.returncode

        logger.info(f"Subprocess completed with exit code: {returncode}")
        if stdout:
            logger.info(f"Subprocess STDOUT:\n{stdout}")
        if stderr:
            logger.error(f"Subprocess STDERR:\n{stderr}")

        if returncode != 0:
            return False, stdout, stderr, stderr, None, str(script_path)

        # Validate that the expected resume file actually exists
        if expected_resume_path:
            resume_file = Path(expected_resume_path)
            if not resume_file.exists():
                error_msg = f"Script completed, but resume was not found at expected path: {expected_resume_path}"
                logger.error(error_msg)
                return False, stdout, error_msg, None, None, str(script_path)
            logger.info(f"Successfully generated resume at: {resume_file}")
            return True, stdout, None, None, str(resume_file), str(script_path)

        # Fallback to looking for the latest generated docx in the resumes directory
        generated_files = list(resume_dir.glob("*.docx"))
        if not generated_files:
            error_msg = "Script completed, but no .docx resumes found in resumes directory."
            logger.error(error_msg)
            return False, stdout, error_msg, None, None, str(script_path)

        latest_resume = max(generated_files, key=os.path.getctime)
        logger.info(f"Successfully generated resume (detected latest): {latest_resume}")
        return True, stdout, None, None, str(latest_resume), str(script_path)

    except subprocess.TimeoutExpired as te:
        error_msg = f"Script execution timed out after 30 seconds."
        tb = traceback.format_exc()
        logger.error(f"{error_msg}\n{tb}")
        return False, te.stdout or "", te.stderr or error_msg, tb, None, str(script_path)
    except Exception as e:
        error_msg = f"Subprocess execution failed: {str(e)}"
        tb = traceback.format_exc()
        logger.error(f"{error_msg}\n{tb}")
        return False, None, error_msg, tb, None, str(script_path)