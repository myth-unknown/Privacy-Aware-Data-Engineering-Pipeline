"""
Unit tests for ingestion.validator module.
"""

import pandas as pd

from src.ingestion.models import IssueSeverity
from src.ingestion.validator import validate_dataframe, validate_file


class TestValidateFile:
    """Tests for file validation."""

    def test_validate_valid_csv(self, tmp_path):
        """Test validation of valid CSV file."""
        csv_path = tmp_path / "test.csv"
        csv_path.write_text("name,age\nAlice,30\n")

        result = validate_file(csv_path)

        assert result.success is True
        assert result.file_name == "test.csv"
        assert result.file_size_bytes > 0

    def test_validate_valid_json(self, tmp_path):
        """Test validation of valid JSON file."""
        json_path = tmp_path / "test.json"
        json_path.write_text('[{"name": "Alice"}]')

        result = validate_file(json_path, allowed_extensions=[".json"])

        assert result.success is True
        assert result.file_name == "test.json"

    def test_validate_nonexistent_file(self):
        """Test validation of non-existent file."""
        result = validate_file("nonexistent.csv")

        assert result.success is False
        assert any("not found" in issue.message.lower() for issue in result.issues)

    def test_validate_wrong_extension(self, tmp_path):
        """Test validation of file with wrong extension."""
        txt_path = tmp_path / "test.txt"
        txt_path.write_text("some text")

        result = validate_file(txt_path, allowed_extensions=[".csv", ".json"])

        assert result.success is False
        assert any("invalid file type" in issue.message.lower() for issue in result.issues)

    def test_validate_file_too_large(self, tmp_path):
        """Test validation of file that exceeds size limit."""
        large_path = tmp_path / "large.csv"
        # Create a 2MB file
        large_path.write_text("x" * (2 * 1024 * 1024))

        result = validate_file(large_path, max_size_mb=1)

        assert result.success is False
        assert any("too large" in issue.message.lower() for issue in result.issues)

    def test_validate_file_size_warning(self, tmp_path):
        """Test warning for file approaching size limit."""
        file_path = tmp_path / "medium.csv"
        # Create a 0.9MB file (90% of 1MB limit)
        file_path.write_text("x" * int(0.9 * 1024 * 1024))

        result = validate_file(file_path, max_size_mb=1)

        # Should succeed but have a warning
        assert result.success is True
        assert any(issue.severity == IssueSeverity.WARNING for issue in result.issues)

    def test_validate_empty_file(self, tmp_path):
        """Test validation of empty file."""
        empty_path = tmp_path / "empty.csv"
        empty_path.write_text("")

        result = validate_file(empty_path)

        assert result.success is False
        assert any("empty" in issue.message.lower() for issue in result.issues)


class TestValidateDataFrame:
    """Tests for DataFrame validation."""

    def test_validate_valid_dataframe(self):
        """Test validation of valid DataFrame."""
        df = pd.DataFrame({"name": ["Alice", "Bob"], "age": [30, 25]})

        result = validate_dataframe(df, file_name="test.csv")

        assert result.success is True
        assert result.num_rows == 2
        assert result.num_columns == 2
        assert result.column_names == ["name", "age"]

    def test_validate_dataframe_too_many_rows(self):
        """Test validation of DataFrame with too many rows."""
        df = pd.DataFrame({"col": range(1000)})

        result = validate_dataframe(df, max_rows=100)

        assert result.success is False
        assert any("too many rows" in issue.message.lower() for issue in result.issues)

    def test_validate_dataframe_too_many_columns(self):
        """Test validation of DataFrame with too many columns."""
        df = pd.DataFrame({f"col{i}": [1] for i in range(100)})

        result = validate_dataframe(df, max_columns=50)

        assert result.success is False
        assert any("too many columns" in issue.message.lower() for issue in result.issues)

    def test_validate_dataframe_insufficient_rows(self):
        """Test validation of DataFrame with insufficient rows."""
        df = pd.DataFrame({"col": []})

        result = validate_dataframe(df, min_rows=1)

        assert result.success is False
        assert any("insufficient rows" in issue.message.lower() for issue in result.issues)

    def test_validate_dataframe_with_nulls(self):
        """Test validation of DataFrame with missing values."""
        df = pd.DataFrame({"name": ["Alice", None, "Bob"], "age": [30, 25, None]})

        result = validate_dataframe(df)

        assert any("missing values" in issue.message.lower() for issue in result.issues)

    def test_validate_dataframe_high_null_percentage(self):
        """Test validation of DataFrame with high percentage of nulls."""
        df = pd.DataFrame({"col": [None] * 60 + [1] * 40})

        result = validate_dataframe(df)

        # Should fail if >50% nulls
        assert result.success is False
        assert any(
            issue.severity == IssueSeverity.ERROR
            and "missing values" in issue.message.lower()
            for issue in result.issues
        )

    def test_validate_dataframe_with_duplicates(self):
        """Test validation of DataFrame with duplicate rows."""
        df = pd.DataFrame({"name": ["Alice", "Bob", "Alice"], "age": [30, 25, 30]})

        result = validate_dataframe(df)

        assert any("duplicate" in issue.message.lower() for issue in result.issues)

    def test_validate_dataframe_unnamed_columns(self):
        """Test validation of DataFrame with unnamed columns."""
        df = pd.DataFrame([[1, 2], [3, 4]], columns=["Unnamed: 0", "col1"])

        result = validate_dataframe(df)

        assert any("unnamed column" in issue.message.lower() for issue in result.issues)

    def test_validate_dataframe_duplicate_column_names(self):
        """Test validation of DataFrame with duplicate column names."""
        df = pd.DataFrame([[1, 2], [3, 4]])
        df.columns = ["col", "col"]

        result = validate_dataframe(df)

        assert any("duplicate column" in issue.message.lower() for issue in result.issues)

    def test_validate_dataframe_fully_null_column(self):
        """Test validation of DataFrame with fully null columns."""
        df = pd.DataFrame({"name": ["Alice", "Bob"], "empty": [None, None]})

        result = validate_dataframe(df)

        assert any("all null" in issue.message.lower() for issue in result.issues)

    def test_validate_empty_dataframe(self):
        """Test validation of empty DataFrame."""
        df = pd.DataFrame(columns=["name", "age"])

        result = validate_dataframe(df)

        assert any("empty" in issue.message.lower() for issue in result.issues)

    def test_validate_dataframe_metadata(self):
        """Test that validation includes metadata."""
        df = pd.DataFrame({"name": ["Alice", "Bob"], "age": [30, 25]})

        result = validate_dataframe(df)

        assert "dtypes" in result.metadata
        assert "memory_usage_bytes" in result.metadata
        # Pandas 2.0+ uses 'str' instead of 'object' for string dtype
        assert result.metadata["dtypes"]["name"] in ["object", "str", "string"]
        assert result.metadata["dtypes"]["age"] == "int64"
