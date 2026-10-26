"""
Tests for logger utilities.
"""

import logging

from src.utils.logger import PIISafeLogger, get_logger, setup_logging


def test_setup_logging(tmp_path):
    """Test logging setup."""
    log_file = tmp_path / "test.log"

    setup_logging(level='DEBUG', log_file=str(log_file))

    # Test that log file was created
    logger = logging.getLogger(__name__)
    logger.info("Test message")

    # Check log file exists and has content
    assert log_file.exists()
    content = log_file.read_text()
    assert "Test message" in content


def test_get_logger():
    """Test getting logger instance."""
    logger = get_logger(__name__)

    assert isinstance(logger, logging.Logger)
    assert logger.name == __name__


def test_pii_safe_logger():
    """Test PII-safe logger wrapper."""
    base_logger = logging.getLogger("test_pii_safe")
    safe_logger = PIISafeLogger(base_logger)

    # Test methods exist and don't raise errors
    safe_logger.debug("Debug message")
    safe_logger.info("Info message")
    safe_logger.warning("Warning message")
    safe_logger.error("Error message")
    safe_logger.critical("Critical message")

    # Verify it's a wrapper
    assert isinstance(safe_logger, PIISafeLogger)
    assert safe_logger.logger == base_logger
