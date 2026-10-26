"""
Unit tests for validation.cleaner module.
"""

import pandas as pd
import pytest

from src.validation.cleaner import (
    fill_missing_values,
    remove_duplicates,
    remove_outliers,
    standardize_column_names,
)


class TestRemoveDuplicates:
    """Tests for duplicate removal."""

    def test_remove_all_duplicates(self):
        """Test removing all duplicate rows."""
        df = pd.DataFrame({
            "name": ["Alice", "Bob", "Alice"],
            "age": [30, 25, 30],
        })

        df_clean = remove_duplicates(df)

        assert len(df_clean) == 2
        assert "Alice" in df_clean["name"].values

    def test_remove_duplicates_keep_last(self):
        """Test keeping last occurrence."""
        df = pd.DataFrame({
            "name": ["Alice", "Bob", "Alice"],
            "age": [30, 25, 30],
        })

        df_clean = remove_duplicates(df, keep="last")

        assert len(df_clean) == 2

    def test_remove_duplicates_subset(self):
        """Test removing duplicates based on subset of columns."""
        df = pd.DataFrame({
            "name": ["Alice", "Bob", "Alice"],
            "age": [30, 25, 35],  # Different ages
        })

        df_clean = remove_duplicates(df, subset=["name"])

        assert len(df_clean) == 2

    def test_no_duplicates(self):
        """Test DataFrame with no duplicates."""
        df = pd.DataFrame({
            "name": ["Alice", "Bob", "Charlie"],
            "age": [30, 25, 35],
        })

        df_clean = remove_duplicates(df)

        assert len(df_clean) == len(df)


class TestFillMissingValues:
    """Tests for missing value handling."""

    def test_fill_drop_strategy(self):
        """Test dropping rows with missing values."""
        df = pd.DataFrame({
            "col1": [1, None, 3],
            "col2": [4, 5, 6],
        })

        df_clean = fill_missing_values(df, strategy="drop")

        assert len(df_clean) == 2
        assert df_clean["col1"].isna().sum() == 0

    def test_fill_mean_strategy(self):
        """Test filling with mean."""
        df = pd.DataFrame({
            "col1": [1.0, None, 3.0],
        })

        df_clean = fill_missing_values(df, strategy="mean")

        assert df_clean["col1"].isna().sum() == 0
        assert df_clean["col1"].iloc[1] == 2.0  # Mean of 1 and 3

    def test_fill_median_strategy(self):
        """Test filling with median."""
        df = pd.DataFrame({
            "col1": [1.0, None, 5.0],
        })

        df_clean = fill_missing_values(df, strategy="median")

        assert df_clean["col1"].isna().sum() == 0
        assert df_clean["col1"].iloc[1] == 3.0  # Median of 1 and 5

    def test_fill_mode_strategy(self):
        """Test filling with mode."""
        df = pd.DataFrame({
            "col1": ["A", None, "A", "B"],
        })

        df_clean = fill_missing_values(df, strategy="mode")

        assert df_clean["col1"].isna().sum() == 0
        assert df_clean["col1"].iloc[1] == "A"  # Mode

    def test_fill_constant_strategy(self):
        """Test filling with constant value."""
        df = pd.DataFrame({
            "col1": [1, None, 3],
        })

        df_clean = fill_missing_values(df, strategy="constant", fill_value=999)

        assert df_clean["col1"].isna().sum() == 0
        assert df_clean["col1"].iloc[1] == 999

    def test_fill_specific_columns(self):
        """Test filling only specific columns."""
        df = pd.DataFrame({
            "col1": [1, None, 3],
            "col2": [None, 5, 6],
        })

        df_clean = fill_missing_values(df, strategy="constant", fill_value=0, columns=["col1"])

        assert df_clean["col1"].isna().sum() == 0
        assert df_clean["col2"].isna().sum() == 1  # col2 not touched

    def test_fill_invalid_strategy(self):
        """Test error on invalid strategy."""
        df = pd.DataFrame({"col1": [1, None, 3]})

        with pytest.raises(ValueError):
            fill_missing_values(df, strategy="invalid")


class TestRemoveOutliers:
    """Tests for outlier removal."""

    def test_remove_outliers_iqr(self):
        """Test IQR method for outlier removal."""
        # Create data with obvious outlier
        df = pd.DataFrame({
            "values": [1, 2, 3, 4, 5, 100],  # 100 is outlier
        })

        df_clean = remove_outliers(df, method="iqr", threshold=1.5)

        assert len(df_clean) < len(df)
        assert 100 not in df_clean["values"].values

    def test_remove_outliers_zscore(self):
        """Test z-score method for outlier removal."""
        df = pd.DataFrame({
            "values": [1, 2, 3, 4, 5, 100],
        })

        df_clean = remove_outliers(df, method="zscore", threshold=2.0)

        assert len(df_clean) < len(df)

    def test_remove_outliers_specific_columns(self):
        """Test outlier removal on specific columns only."""
        df = pd.DataFrame({
            "col1": [1, 2, 3, 4, 5, 100],
            "col2": [10, 20, 30, 40, 50, 60],
        })

        df_clean = remove_outliers(df, columns=["col1"], method="iqr")

        # col1 should have outliers removed, col2 intact
        assert 100 not in df_clean["col1"].values

    def test_no_outliers(self):
        """Test data without outliers."""
        df = pd.DataFrame({
            "values": [1, 2, 3, 4, 5],
        })

        df_clean = remove_outliers(df, method="iqr")

        assert len(df_clean) == len(df)

    def test_remove_outliers_invalid_method(self):
        """Test error on invalid method."""
        df = pd.DataFrame({"values": [1, 2, 3]})

        with pytest.raises(ValueError):
            remove_outliers(df, method="invalid")


class TestStandardizeColumnNames:
    """Tests for column name standardization."""

    def test_snake_case(self):
        """Test conversion to snake_case."""
        df = pd.DataFrame({
            "First Name": [1],
            "Last Name": [2],
            "User-ID": [3],
        })

        df_clean = standardize_column_names(df, style="snake_case")

        assert "first_name" in df_clean.columns
        assert "last_name" in df_clean.columns
        assert "user_id" in df_clean.columns

    def test_lowercase(self):
        """Test conversion to lowercase."""
        df = pd.DataFrame({
            "FirstName": [1],
            "LASTNAME": [2],
        })

        df_clean = standardize_column_names(df, style="lowercase")

        assert "firstname" in df_clean.columns
        assert "lastname" in df_clean.columns

    def test_camel_case(self):
        """Test conversion to camelCase."""
        df = pd.DataFrame({
            "first name": [1],
            "last_name": [2],
        })

        df_clean = standardize_column_names(df, style="camelCase")

        assert "firstName" in df_clean.columns
        assert "lastName" in df_clean.columns

    def test_pascal_case(self):
        """Test conversion to PascalCase."""
        df = pd.DataFrame({
            "first name": [1],
            "last_name": [2],
        })

        df_clean = standardize_column_names(df, style="PascalCase")

        assert "FirstName" in df_clean.columns
        assert "LastName" in df_clean.columns

    def test_invalid_style(self):
        """Test error on invalid style."""
        df = pd.DataFrame({"col": [1]})

        with pytest.raises(ValueError):
            standardize_column_names(df, style="invalid")
