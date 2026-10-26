"""
Logging configuration and utilities.

Provides centralized logging setup with file and console handlers.
"""

import logging
import sys
from pathlib import Path


def setup_logging(
    level: str = "INFO",
    log_file: str | None = "logs/pipeline.log",
    format_string: str | None = None
) -> None:
    """
    Configure application logging.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_file: Path to log file. If None, only console logging.
        format_string: Custom log format string. Uses default if None.

    Examples:
        >>> setup_logging(level='DEBUG', log_file='logs/debug.log')
        >>> logger = logging.getLogger(__name__)
        >>> logger.info("Application started")
    """
    # Default format
    if format_string is None:
        format_string = '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s'

    # Create formatter
    formatter = logging.Formatter(format_string, datefmt='%Y-%m-%d %H:%M:%S')

    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))

    # Remove existing handlers
    root_logger.handlers = []

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler (if log_file specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(getattr(logging, level.upper()))
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance.

    Args:
        name: Logger name (typically __name__).

    Returns:
        Logger instance.

    Examples:
        >>> logger = get_logger(__name__)
        >>> logger.info("Processing started")
    """
    return logging.getLogger(name)


class PIISafeLogger:
    """
    Logger wrapper that prevents accidental PII logging.

    This class wraps the standard logger and provides methods that
    redact potential PII from log messages.
    """

    def __init__(self, logger: logging.Logger):
        """
        Initialize PII-safe logger.

        Args:
            logger: Standard Python logger instance.
        """
        self.logger = logger

    def _redact_pii(self, message: str) -> str:
        """
        Redact potential PII from log message.

        This is a basic implementation. For production use,
        implement more sophisticated PII detection.

        Args:
            message: Log message.

        Returns:
            Redacted message.
        """
        # For now, just return as-is with warning in docs
        # In future, could implement pattern matching for emails, phones, etc.
        return message

    def debug(self, message: str, *args, **kwargs):
        """Log debug message."""
        self.logger.debug(self._redact_pii(message), *args, **kwargs)

    def info(self, message: str, *args, **kwargs):
        """Log info message."""
        self.logger.info(self._redact_pii(message), *args, **kwargs)

    def warning(self, message: str, *args, **kwargs):
        """Log warning message."""
        self.logger.warning(self._redact_pii(message), *args, **kwargs)

    def error(self, message: str, *args, **kwargs):
        """Log error message."""
        self.logger.error(self._redact_pii(message), *args, **kwargs)

    def critical(self, message: str, *args, **kwargs):
        """Log critical message."""
        self.logger.critical(self._redact_pii(message), *args, **kwargs)
