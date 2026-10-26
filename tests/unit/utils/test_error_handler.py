"""
Tests for error handling utilities.
"""


from src.utils.error_handler import (
    ANONYMIZATION_ERROR,
    FILE_LOAD_ERROR,
    PII_DETECTION_ERROR,
    QUALITY_PROFILING_ERROR,
    UNEXPECTED_ERROR,
    get_safe_error_details,
    get_user_friendly_error,
    sanitize_error_message,
)


class TestGetUserFriendlyError:
    """Tests for get_user_friendly_error function."""

    def test_file_load_error(self):
        """Test file load error message."""
        error = FileNotFoundError("File not found at /path/to/file.csv")
        message = get_user_friendly_error(error, FILE_LOAD_ERROR)

        # Should contain friendly message
        assert "Unable to load the file" in message
        # Should not contain file path
        assert "/path/to/file.csv" not in message
        # Should indicate error type
        assert "File not found" in message

    def test_quality_profiling_error(self):
        """Test quality profiling error message."""
        error = ValueError("Invalid data type in column 'age'")
        message = get_user_friendly_error(error, QUALITY_PROFILING_ERROR)

        assert "Unable to analyze data quality" in message
        assert "Invalid data value" in message

    def test_pii_detection_error(self):
        """Test PII detection error message."""
        error = RuntimeError("NLP model not loaded")
        message = get_user_friendly_error(error, PII_DETECTION_ERROR)

        assert "PII detection encountered an issue" in message
        # Should not expose internal error details
        assert "NLP model not loaded" not in message

    def test_anonymization_error(self):
        """Test anonymization error message."""
        error = KeyError("strategy")
        message = get_user_friendly_error(error, ANONYMIZATION_ERROR)

        assert "Anonymization process failed" in message
        assert "Missing required data field" in message

    def test_unexpected_error(self):
        """Test unexpected error message."""
        error = Exception("Something went wrong")
        message = get_user_friendly_error(error, UNEXPECTED_ERROR)

        assert "unexpected error" in message.lower()
        # Should not expose internal details
        assert "Something went wrong" not in message

    def test_permission_error(self):
        """Test permission error is handled."""
        error = PermissionError("Access denied to file")
        message = get_user_friendly_error(error, FILE_LOAD_ERROR)

        assert "Permission denied" in message

    def test_memory_error(self):
        """Test memory error is handled."""
        error = MemoryError("Out of memory")
        message = get_user_friendly_error(error, FILE_LOAD_ERROR)

        assert "Insufficient memory" in message


class TestSanitizeErrorMessage:
    """Tests for sanitize_error_message function."""

    def test_sanitize_windows_path(self):
        """Test Windows file path is sanitized."""
        message = "Error in C:\\Users\\User\\project\\file.py"
        sanitized = sanitize_error_message(message)

        assert "C:\\Users\\User\\project\\file.py" not in sanitized
        assert "[PATH]" in sanitized

    def test_sanitize_unix_path(self):
        """Test Unix file path is sanitized."""
        message = "Error in /home/user/project/file.py"
        sanitized = sanitize_error_message(message)

        assert "/home/user/project/file.py" not in sanitized
        assert "[PATH]" in sanitized

    def test_sanitize_line_numbers(self):
        """Test line numbers are sanitized."""
        message = "Error at line 123 in file.py:456:"
        sanitized = sanitize_error_message(message)

        assert "line 123" not in sanitized
        assert ":456:" not in sanitized
        assert "line [N]" in sanitized
        assert ":[N]:" in sanitized

    def test_sanitize_module_paths(self):
        """Test module paths are sanitized."""
        message = "Error in src.detection.rule_based_detector"
        sanitized = sanitize_error_message(message)

        assert "src.detection.rule_based_detector" not in sanitized
        assert "[MODULE]" in sanitized

    def test_no_sensitive_info_remains(self):
        """Test comprehensive sanitization."""
        message = (
            "File not found: D:\\Projects\\pipeline\\src\\ui\\pages\\quality.py "
            "at line 97 in src.ui.pages.quality module"
        )
        sanitized = sanitize_error_message(message)

        # No paths
        assert "D:\\Projects\\pipeline" not in sanitized
        assert "src\\ui\\pages\\quality.py" not in sanitized
        # No line numbers
        assert "line 97" not in sanitized
        # No module paths
        assert "src.ui.pages.quality" not in sanitized


class TestGetSafeErrorDetails:
    """Tests for get_safe_error_details function."""

    def test_includes_error_type(self):
        """Test error type is included."""
        error = ValueError("Test error")
        details = get_safe_error_details(error, include_type=True)

        assert "type" in details
        assert details["type"] == "ValueError"

    def test_excludes_error_type(self):
        """Test error type can be excluded."""
        error = ValueError("Test error")
        details = get_safe_error_details(error, include_type=False)

        assert "type" not in details

    def test_includes_sanitized_message(self):
        """Test message is sanitized."""
        error = FileNotFoundError("File not found at C:\\Users\\User\\file.csv")
        details = get_safe_error_details(error)

        assert "message" in details
        assert "C:\\Users\\User\\file.csv" not in details["message"]
        assert "[PATH]" in details["message"]

    def test_truncates_long_messages(self):
        """Test long messages are truncated."""
        long_message = "Error: " + "x" * 300
        error = ValueError(long_message)
        details = get_safe_error_details(error)

        assert len(details["message"]) <= 204  # 200 + "..."
        assert details["message"].endswith("...")

    def test_handles_empty_message(self):
        """Test empty error messages are handled."""
        error = ValueError()
        details = get_safe_error_details(error)

        assert "message" in details
        assert isinstance(details["message"], str)
