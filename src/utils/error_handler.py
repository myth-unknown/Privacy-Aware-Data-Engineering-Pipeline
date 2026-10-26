"""
User-friendly error handling for UI layer.
Sanitizes error messages to prevent information leakage.
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


# User-friendly error messages by category
ERROR_MESSAGES = {
    "file_load": "Unable to load the file. Please ensure it's a valid CSV or JSON file with proper encoding.",
    "data_validation": "The uploaded data contains validation issues. Please review the warnings above.",
    "quality_profiling": "Unable to analyze data quality. The dataset may have structural issues.",
    "pii_detection": "PII detection encountered an issue. Please ensure the data is properly loaded.",
    "anonymization": "Anonymization process failed. Please check your configuration and try again.",
    "configuration": "Invalid configuration. Please check your settings and try again.",
    "permission": "Operation not permitted. Please check your file access permissions.",
    "resource": "Insufficient resources to complete the operation. Try with a smaller dataset.",
    "unexpected": "An unexpected error occurred. Please try again or contact support if the issue persists.",
}


def get_user_friendly_error(error: Exception, category: str = "unexpected") -> str:
    """
    Convert exception to user-friendly error message.

    Args:
        error: The exception object
        category: Error category for context-appropriate message

    Returns:
        User-friendly error message (no internal details)
    """
    # Log the actual error with full details (for debugging)
    logger.error(f"Error in category '{category}': {error}", exc_info=True)

    # Return sanitized message for users
    base_message = ERROR_MESSAGES.get(category, ERROR_MESSAGES["unexpected"])

    # Add safe error type (no paths or line numbers)
    error_type = type(error).__name__

    # Common safe error types that users can understand
    safe_error_types = {
        "FileNotFoundError": "File not found.",
        "PermissionError": "Permission denied.",
        "MemoryError": "Insufficient memory.",
        "KeyError": "Missing required data field.",
        "ValueError": "Invalid data value.",
        "TypeError": "Data type mismatch.",
        "UnicodeDecodeError": "File encoding issue.",
        "JSONDecodeError": "Invalid JSON format.",
        "EmptyDataError": "File is empty.",
        "ParserError": "Unable to parse file format.",
    }

    # Add specific error type if it's safe to expose
    if error_type in safe_error_types:
        base_message += f" ({safe_error_types[error_type]})"

    return base_message


def log_error_safely(error: Exception, context: str = "") -> None:
    """
    Log error with full details for debugging (not shown to users).

    Args:
        error: The exception object
        context: Additional context about where the error occurred
    """
    if context:
        logger.error(f"{context}: {error}", exc_info=True)
    else:
        logger.error(f"Error: {error}", exc_info=True)


def sanitize_error_message(message: str) -> str:
    """
    Sanitize error message by removing file paths and line numbers.

    Args:
        message: Raw error message

    Returns:
        Sanitized message safe for display
    """
    import re

    # Remove file paths (Windows and Unix)
    message = re.sub(r'[A-Za-z]:\\[^\s]+', '[PATH]', message)
    message = re.sub(r'/[^\s]+', '[PATH]', message)

    # Remove line numbers
    message = re.sub(r'line \d+', 'line [N]', message)
    message = re.sub(r':\d+:', ':[N]:', message)

    # Remove module paths
    message = re.sub(r'\w+\.\w+\.\w+', '[MODULE]', message)

    return message


def get_safe_error_details(error: Exception, include_type: bool = True) -> dict[str, Any]:
    """
    Extract safe error details for logging or debugging display.

    Args:
        error: The exception object
        include_type: Whether to include error type

    Returns:
        Dictionary with safe error information
    """
    details = {}

    if include_type:
        details["type"] = type(error).__name__

    # Only include safe portions of the message
    error_msg = str(error)
    if len(error_msg) > 200:
        error_msg = error_msg[:200] + "..."

    details["message"] = sanitize_error_message(error_msg)

    return details


# Common error categories for convenience
FILE_LOAD_ERROR = "file_load"
DATA_VALIDATION_ERROR = "data_validation"
QUALITY_PROFILING_ERROR = "quality_profiling"
PII_DETECTION_ERROR = "pii_detection"
ANONYMIZATION_ERROR = "anonymization"
CONFIGURATION_ERROR = "configuration"
PERMISSION_ERROR = "permission"
RESOURCE_ERROR = "resource"
UNEXPECTED_ERROR = "unexpected"
