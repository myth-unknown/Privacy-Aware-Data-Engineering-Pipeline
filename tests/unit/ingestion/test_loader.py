"""
Unit tests for ingestion.loader module.
"""

import json

import pandas as pd
import pytest

from src.ingestion.loader import detect_encoding, infer_delimiter, load_csv, load_json


class TestDetectEncoding:
    """Tests for encoding detection."""

    def test_detect_utf8(self, tmp_path):
        """Test UTF-8 encoding detection."""
        file_path = tmp_path / "utf8.txt"
        file_path.write_text("Hello, World! 你好", encoding="utf-8")

        encoding = detect_encoding(file_path)
        assert encoding in ["utf-8", "UTF-8", "ascii"]

    def test_detect_latin1(self, tmp_path):
        """Test Latin-1 encoding detection."""
        file_path = tmp_path / "latin1.txt"
        file_path.write_bytes("Café résumé".encode("latin-1"))

        encoding = detect_encoding(file_path)
        assert encoding is not None

    def test_empty_file(self, tmp_path):
        """Test encoding detection on empty file."""
        file_path = tmp_path / "empty.txt"
        file_path.write_text("")

        encoding = detect_encoding(file_path)
        # Should fallback to utf-8
        assert encoding == "utf-8"


class TestLoadCSV:
    """Tests for CSV loading."""

    def test_load_simple_csv(self, tmp_path):
        """Test loading a simple CSV file."""
        csv_path = tmp_path / "test.csv"
        csv_content = "name,age,city\nAlice,30,NYC\nBob,25,LA\n"
        csv_path.write_text(csv_content)

        df = load_csv(csv_path)

        assert len(df) == 2
        assert list(df.columns) == ["name", "age", "city"]
        assert df["name"].tolist() == ["Alice", "Bob"]

    def test_load_csv_with_encoding(self, tmp_path):
        """Test loading CSV with specified encoding."""
        csv_path = tmp_path / "test.csv"
        csv_content = "name,age\nAlice,30\nBob,25\n"
        csv_path.write_text(csv_content, encoding="utf-8")

        df = load_csv(csv_path, encoding="utf-8")

        assert len(df) == 2
        assert len(df.columns) == 2

    def test_load_csv_with_delimiter(self, tmp_path):
        """Test loading CSV with custom delimiter."""
        csv_path = tmp_path / "test.csv"
        csv_content = "name;age;city\nAlice;30;NYC\nBob;25;LA\n"
        csv_path.write_text(csv_content)

        df = load_csv(csv_path, delimiter=";")

        assert len(df) == 2
        assert list(df.columns) == ["name", "age", "city"]

    def test_load_nonexistent_file(self):
        """Test loading non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_csv("nonexistent.csv")

    def test_load_malformed_csv(self, tmp_path):
        """Test loading malformed CSV raises error."""
        csv_path = tmp_path / "malformed.csv"
        csv_content = "name,age\nAlice,30,extra\nBob\n"
        csv_path.write_text(csv_content)

        # Should raise ParserError with error_bad_lines default behavior
        # or load with warnings depending on pandas version
        try:
            df = load_csv(csv_path)
            # If it loads, check it handles the malformed row
            assert len(df) >= 1
        except pd.errors.ParserError:
            # Expected for strict parsing
            pass

    def test_load_empty_csv(self, tmp_path):
        """Test loading empty CSV."""
        csv_path = tmp_path / "empty.csv"
        csv_content = "name,age\n"
        csv_path.write_text(csv_content)

        df = load_csv(csv_path)

        assert len(df) == 0
        assert list(df.columns) == ["name", "age"]


class TestLoadJSON:
    """Tests for JSON loading."""

    def test_load_json_records(self, tmp_path):
        """Test loading JSON in records format."""
        json_path = tmp_path / "test.json"
        data = [
            {"name": "Alice", "age": 30, "city": "NYC"},
            {"name": "Bob", "age": 25, "city": "LA"},
        ]
        json_path.write_text(json.dumps(data))

        df = load_json(json_path, orient="records")

        assert len(df) == 2
        assert list(df.columns) == ["name", "age", "city"]

    def test_load_json_columns(self, tmp_path):
        """Test loading JSON in columns format."""
        json_path = tmp_path / "test.json"
        data = {
            "name": ["Alice", "Bob"],
            "age": [30, 25],
            "city": ["NYC", "LA"],
        }
        json_path.write_text(json.dumps(data))

        df = load_json(json_path, orient="columns")

        assert len(df) == 2
        assert list(df.columns) == ["name", "age", "city"]

    def test_load_nonexistent_json(self):
        """Test loading non-existent JSON file."""
        with pytest.raises(FileNotFoundError):
            load_json("nonexistent.json")

    def test_load_invalid_json(self, tmp_path):
        """Test loading invalid JSON raises error."""
        json_path = tmp_path / "invalid.json"
        json_path.write_text("{invalid json}")

        with pytest.raises((ValueError, json.JSONDecodeError)):
            load_json(json_path)

    def test_load_empty_json(self, tmp_path):
        """Test loading empty JSON array."""
        json_path = tmp_path / "empty.json"
        json_path.write_text("[]")

        df = load_json(json_path, orient="records")

        assert len(df) == 0


class TestInferDelimiter:
    """Tests for delimiter inference."""

    def test_infer_comma(self, tmp_path):
        """Test inferring comma delimiter."""
        csv_path = tmp_path / "comma.csv"
        csv_content = "name,age,city\nAlice,30,NYC\nBob,25,LA\n"
        csv_path.write_text(csv_content)

        delimiter = infer_delimiter(csv_path)

        assert delimiter == ","

    def test_infer_semicolon(self, tmp_path):
        """Test inferring semicolon delimiter."""
        csv_path = tmp_path / "semicolon.csv"
        csv_content = "name;age;city\nAlice;30;NYC\nBob;25;LA\n"
        csv_path.write_text(csv_content)

        delimiter = infer_delimiter(csv_path)

        assert delimiter == ";"

    def test_infer_tab(self, tmp_path):
        """Test inferring tab delimiter."""
        csv_path = tmp_path / "tab.csv"
        csv_content = "name\tage\tcity\nAlice\t30\tNYC\nBob\t25\tLA\n"
        csv_path.write_text(csv_content)

        delimiter = infer_delimiter(csv_path)

        assert delimiter == "\t"

    def test_infer_pipe(self, tmp_path):
        """Test inferring pipe delimiter."""
        csv_path = tmp_path / "pipe.csv"
        csv_content = "name|age|city\nAlice|30|NYC\nBob|25|LA\n"
        csv_path.write_text(csv_content)

        delimiter = infer_delimiter(csv_path)

        assert delimiter == "|"
