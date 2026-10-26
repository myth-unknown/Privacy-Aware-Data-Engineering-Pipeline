"""
Schema validation utilities.
"""

import logging
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)


class SchemaValidator:
    """Validate DataFrame against a schema definition."""

    def __init__(self, schema: dict[str, Any]):
        """
        Initialize validator with schema.

        Schema format:
        {
            "column_name": {
                "dtype": "int64",  # expected data type
                "required": True,  # column must exist
                "nullable": False,  # nulls allowed
                "unique": False,  # values must be unique
                "min": 0,  # min value (numeric only)
                "max": 100,  # max value (numeric only)
                "pattern": r"^[A-Z]",  # regex pattern (string only)
            }
        }
        """
        self.schema = schema
        self.errors: list[str] = []

    def validate(self, df: pd.DataFrame) -> bool:
        """
        Validate DataFrame against schema.

        Returns:
            True if valid, False otherwise (check self.errors for details)
        """
        self.errors = []

        # Check required columns
        for col_name, col_schema in self.schema.items():
            if col_schema.get("required", False) and col_name not in df.columns:
                self.errors.append(f"Required column '{col_name}' is missing")

        # Validate existing columns
        for col_name in df.columns:
            if col_name in self.schema:
                self._validate_column(df[col_name], self.schema[col_name])

        is_valid = len(self.errors) == 0

        if is_valid:
            logger.info("Schema validation passed")
        else:
            logger.warning(f"Schema validation failed: {len(self.errors)} errors")

        return is_valid

    def _validate_column(self, series: pd.Series, col_schema: dict[str, Any]) -> None:
        """Validate a single column against its schema."""
        col_name = series.name

        # Check data type
        if "dtype" in col_schema:
            expected_dtype = col_schema["dtype"]
            actual_dtype = str(series.dtype)
            if actual_dtype != expected_dtype:
                self.errors.append(
                    f"Column '{col_name}' has incorrect type: "
                    f"expected {expected_dtype}, got {actual_dtype}"
                )

        # Check nullability
        if not col_schema.get("nullable", True):
            null_count = series.isna().sum()
            if null_count > 0:
                self.errors.append(
                    f"Column '{col_name}' contains {null_count} null values "
                    f"(not nullable)"
                )

        # Check uniqueness
        if col_schema.get("unique", False):
            duplicate_count = series.duplicated().sum()
            if duplicate_count > 0:
                self.errors.append(
                    f"Column '{col_name}' contains {duplicate_count} duplicate values "
                    f"(must be unique)"
                )

        # Numeric constraints
        if pd.api.types.is_numeric_dtype(series):
            if "min" in col_schema:
                min_val = col_schema["min"]
                violations = (series < min_val).sum()
                if violations > 0:
                    self.errors.append(
                        f"Column '{col_name}' has {violations} values below minimum {min_val}"
                    )

            if "max" in col_schema:
                max_val = col_schema["max"]
                violations = (series > max_val).sum()
                if violations > 0:
                    self.errors.append(
                        f"Column '{col_name}' has {violations} values above maximum {max_val}"
                    )

        # String constraints
        if pd.api.types.is_string_dtype(series) or str(series.dtype) == "object":
            if "pattern" in col_schema:
                pattern = col_schema["pattern"]
                non_null = series.dropna()
                violations = (~non_null.astype(str).str.match(pattern)).sum()
                if violations > 0:
                    self.errors.append(
                        f"Column '{col_name}' has {violations} values not matching pattern '{pattern}'"
                    )


def validate_against_schema(df: pd.DataFrame, schema: dict[str, Any]) -> tuple[bool, list[str]]:
    """
    Convenience function to validate DataFrame against schema.

    Args:
        df: DataFrame to validate
        schema: Schema definition

    Returns:
        Tuple of (is_valid, error_list)
    """
    validator = SchemaValidator(schema)
    is_valid = validator.validate(df)
    return is_valid, validator.errors
