"""
Unit tests for validation.schema_validator module.
"""

import pandas as pd

from src.validation.schema_validator import SchemaValidator, validate_against_schema


class TestSchemaValidator:
    """Tests for SchemaValidator class."""

    def test_validate_valid_schema(self):
        """Test validation of DataFrame matching schema."""
        df = pd.DataFrame({
            "name": ["Alice", "Bob"],
            "age": [30, 25],
        })

        schema = {
            "name": {"required": True, "dtype": "str"},
            "age": {"required": True, "dtype": "int64"},
        }

        validator = SchemaValidator(schema)
        is_valid = validator.validate(df)

        assert is_valid is True
        assert len(validator.errors) == 0

    def test_validate_missing_required_column(self):
        """Test detection of missing required column."""
        df = pd.DataFrame({
            "name": ["Alice", "Bob"],
        })

        schema = {
            "name": {"required": True},
            "age": {"required": True},
        }

        validator = SchemaValidator(schema)
        is_valid = validator.validate(df)

        assert is_valid is False
        assert any("missing" in error.lower() for error in validator.errors)

    def test_validate_incorrect_dtype(self):
        """Test detection of incorrect data type."""
        df = pd.DataFrame({
            "age": ["30", "25"],  # Strings instead of ints
        })

        schema = {
            "age": {"dtype": "int64"},
        }

        validator = SchemaValidator(schema)
        is_valid = validator.validate(df)

        assert is_valid is False
        assert any("incorrect type" in error.lower() for error in validator.errors)

    def test_validate_nullable_constraint(self):
        """Test nullable constraint validation."""
        df = pd.DataFrame({
            "name": ["Alice", None, "Bob"],
        })

        schema = {
            "name": {"nullable": False},
        }

        validator = SchemaValidator(schema)
        is_valid = validator.validate(df)

        assert is_valid is False
        assert any("null" in error.lower() for error in validator.errors)

    def test_validate_unique_constraint(self):
        """Test unique constraint validation."""
        df = pd.DataFrame({
            "id": [1, 2, 2, 3],
        })

        schema = {
            "id": {"unique": True},
        }

        validator = SchemaValidator(schema)
        is_valid = validator.validate(df)

        assert is_valid is False
        assert any("duplicate" in error.lower() for error in validator.errors)

    def test_validate_numeric_min_constraint(self):
        """Test minimum value constraint for numeric column."""
        df = pd.DataFrame({
            "age": [30, 25, 15],
        })

        schema = {
            "age": {"min": 18},
        }

        validator = SchemaValidator(schema)
        is_valid = validator.validate(df)

        assert is_valid is False
        assert any("below minimum" in error.lower() for error in validator.errors)

    def test_validate_numeric_max_constraint(self):
        """Test maximum value constraint for numeric column."""
        df = pd.DataFrame({
            "score": [85, 92, 105],
        })

        schema = {
            "score": {"max": 100},
        }

        validator = SchemaValidator(schema)
        is_valid = validator.validate(df)

        assert is_valid is False
        assert any("above maximum" in error.lower() for error in validator.errors)

    def test_validate_string_pattern_constraint(self):
        """Test regex pattern constraint for string column."""
        df = pd.DataFrame({
            "code": ["ABC123", "DEF456", "invalid"],
        })

        schema = {
            "code": {"pattern": r"^[A-Z]{3}\d{3}$"},
        }

        validator = SchemaValidator(schema)
        is_valid = validator.validate(df)

        assert is_valid is False
        assert any("not matching pattern" in error.lower() for error in validator.errors)

    def test_validate_optional_column(self):
        """Test that optional columns don't fail validation when missing."""
        df = pd.DataFrame({
            "name": ["Alice", "Bob"],
        })

        schema = {
            "name": {"required": True},
            "age": {"required": False},
        }

        validator = SchemaValidator(schema)
        is_valid = validator.validate(df)

        assert is_valid is True


class TestValidateAgainstSchema:
    """Tests for convenience function."""

    def test_convenience_function(self):
        """Test the convenience function wrapper."""
        df = pd.DataFrame({
            "name": ["Alice", "Bob"],
            "age": [30, 25],
        })

        schema = {
            "name": {"required": True},
            "age": {"required": True, "min": 0, "max": 120},
        }

        is_valid, errors = validate_against_schema(df, schema)

        assert is_valid is True
        assert len(errors) == 0

    def test_convenience_function_with_errors(self):
        """Test convenience function returns errors."""
        df = pd.DataFrame({
            "age": [30, 25, 150],  # 150 exceeds max
        })

        schema = {
            "age": {"max": 120},
        }

        is_valid, errors = validate_against_schema(df, schema)

        assert is_valid is False
        assert len(errors) > 0
