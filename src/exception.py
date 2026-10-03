"""
Custom exception handling utilities.

This module provides a production-ready custom exception that captures:
- The original exception message
- Source file
- Line number
- Exception type
- Full traceback context

The implementation is platform-independent.
"""

from __future__ import annotations

import sys
import traceback
from typing import Optional
from src.logger import logging

def error_message_detail(
    error: BaseException,
    error_detail: Optional[object] = None,
) -> str:
    """
    Build a detailed, platform-independent error message.

    Parameters
    ----------
    error:
        The original exception.

    error_detail:
        Usually the `sys` module. If omitted, the current exception
        information is obtained automatically.

    Returns
    -------
    str
        A detailed error message containing the file, line number,
        exception type, and original error message.
    """

    if error_detail is None:
        error_detail = sys

    exc_type, exc_value, exc_tb = error_detail.exc_info()

    # If no active exception traceback is available, return
    # a safe fallback message.
    if exc_tb is None:
        return (
            f"Error occurred: "
            f"{type(error).__name__}: {error}"
        )

    # Get the last traceback frame.
    traceback_frames = traceback.extract_tb(exc_tb)

    if traceback_frames:
        last_frame = traceback_frames[-1]

        file_name = last_frame.filename
        line_number = last_frame.lineno
        function_name = last_frame.name

        return (
            f"Error occurred in "
            f"[{file_name}] "
            f"at line [{line_number}] "
            f"in function [{function_name}]: "
            f"{type(error).__name__}: {error}"
        )

    return (
        f"Error occurred: "
        f"{type(error).__name__}: {error}"
    )


class CustomException(Exception):
    """
    Application-specific exception.

    This exception preserves the original exception while providing
    additional debugging information.
    """

    def __init__(
        self,
        error_message: str,
        error_detail: Optional[object] = None,
    ) -> None:
        self.original_message = error_message

        self.error_message = error_message_detail(
            error_message,
            error_detail,
        )

        super().__init__(self.error_message)

    def __str__(self) -> str:
        return self.error_message