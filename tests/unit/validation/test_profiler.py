"""
Unit tests for validation.profiler module.
"""

import pandas as pd
import pytest

from src.validation.models import QualityProfile
from src.validation.profiler import _calculate_quality_score, _profile_column, profile_dataframe


class TestProfileDataFrame:
    """Tests for DataFrame profiling."""

    def test_profile_simple_dataframe(self):
        """Test profiling a simple DataFrame."""
        df = pd.DataFrame({
            "name": ["Alice", "Bob", "Charlie"],
            "age": [30, 25, 35],
            "score": [85.5, 92.0, 78.5],
        })

        profile = profile_dataframe(df)

        assert profile.num_rows == 3
        assert profile.num_columns == 3
        assert profile.total_nulls == 0
        assert profile.null_percentage == 0.0
        assert profile.duplicate_rows == 0
        assert len(profile.column_profiles) == 3
        assert profile.quality_score > 0

    def test_profile_with_nulls(self):
        """Test profiling DataFrame with missing values."""
        df = pd.DataFrame({
            "col1": [1, None, 3],
            "col2": [None, None, None],
        })

        profile = profile_dataframe(df)

        assert profile.total_nulls == 4
        assert profile.null_percentage > 60.0  # 4/6 = 66.67%
        assert profile.has_issues
        assert any(issue.issue_type == "missing_values" for issue in profile.issues)

    def test_profile_with_duplicates(self):
        """Test profiling DataFrame with duplicate rows."""
        df = pd.DataFrame({
            "name": ["Alice", "Bob", "Alice", "Bob"],
            "age": [30, 25, 30, 25],
        })

        profile = profile_dataframe(df)

        assert profile.duplicate_rows == 2
        assert profile.duplicate_percentage == 50.0

    def test_profile_categorizes_columns(self):
        """Test that profiling categorizes columns by type."""
        df = pd.DataFrame({
            "numeric": [1, 2, 3],
            "string": ["a", "b", "c"],
            "boolean": [True, False, True],
            "datetime": pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"]),
        })

        profile = profile_dataframe(df)

        assert "numeric" in profile.numeric_columns
        assert "string" in profile.string_columns
        assert "boolean" in profile.boolean_columns
        assert "datetime" in profile.datetime_columns

    def test_profile_detects_high_severity_issues(self):
        """Test detection of high severity issues."""
        df = pd.DataFrame({
            "col1": [None] * 60 + [1] * 40,  # >50% nulls
        })

        profile = profile_dataframe(df)

        high_issues = profile.high_severity_issues
        assert len(high_issues) > 0
        assert any(issue.severity == "high" for issue in high_issues)

    def test_profile_empty_dataframe(self):
        """Test profiling empty DataFrame."""
        df = pd.DataFrame()

        profile = profile_dataframe(df)

        assert profile.num_rows == 0
        assert profile.num_columns == 0
        assert profile.total_nulls == 0


class TestProfileColumn:
    """Tests for column profiling."""

    def test_profile_numeric_column(self):
        """Test profiling numeric column."""
        series = pd.Series([1, 2, 3, 4, 5], name="numbers")

        col_profile = _profile_column(series)

        assert col_profile.name == "numbers"
        assert col_profile.null_count == 0
        assert col_profile.unique_count == 5
        assert col_profile.mean == 3.0
        assert col_profile.median == 3.0
        assert col_profile.min_value == 1.0
        assert col_profile.max_value == 5.0

    def test_profile_string_column(self):
        """Test profiling string column."""
        series = pd.Series(["apple", "banana", "cherry"], name="fruits")

        col_profile = _profile_column(series)

        assert col_profile.name == "fruits"
        assert col_profile.unique_count == 3
        assert col_profile.min_length == 5  # "apple"
        assert col_profile.max_length == 6  # "banana" or "cherry"
        assert col_profile.avg_length > 5

    def test_profile_column_with_nulls(self):
        """Test profiling column with nulls."""
        series = pd.Series([1, None, 3, None, 5], name="with_nulls")

        col_profile = _profile_column(series)

        assert col_profile.null_count == 2
        assert col_profile.null_percentage == 40.0
        assert col_profile.non_null_count == 3

    def test_profile_column_with_duplicates(self):
        """Test profiling column with duplicates."""
        series = pd.Series([1, 2, 2, 3, 3, 3], name="duplicates")

        col_profile = _profile_column(series)

        assert col_profile.unique_count == 3
        assert col_profile.duplicate_count == 3  # Three duplicate values

    def test_profile_column_top_values(self):
        """Test top values extraction."""
        series = pd.Series([1, 1, 1, 2, 2, 3], name="values")

        col_profile = _profile_column(series)

        assert len(col_profile.top_values) > 0
        assert "1" in col_profile.top_values
        assert col_profile.top_values["1"] == 3


class TestCalculateQualityScore:
    """Tests for quality score calculation."""

    def test_perfect_score(self):
        """Test perfect quality score."""
        profile = QualityProfile(
            num_rows=100,
            num_columns=5,
            memory_usage_bytes=10000,
            total_nulls=0,
            null_percentage=0.0,
            duplicate_rows=0,
            duplicate_percentage=0.0,
        )

        score = _calculate_quality_score(profile)

        assert score == 100.0

    def test_score_with_nulls(self):
        """Test score penalty for missing values."""
        profile = QualityProfile(
            num_rows=100,
            num_columns=5,
            memory_usage_bytes=10000,
            total_nulls=50,
            null_percentage=10.0,  # 10% nulls
            duplicate_rows=0,
            duplicate_percentage=0.0,
        )

        score = _calculate_quality_score(profile)

        # Should lose 8 points (10% * 0.8)
        assert score == pytest.approx(92.0, abs=1.0)

    def test_score_with_duplicates(self):
        """Test score penalty for duplicates."""
        profile = QualityProfile(
            num_rows=100,
            num_columns=5,
            memory_usage_bytes=10000,
            total_nulls=0,
            null_percentage=0.0,
            duplicate_rows=20,
            duplicate_percentage=20.0,  # 20% duplicates
        )

        score = _calculate_quality_score(profile)

        # Should lose 20 points (20% * 1.0)
        assert score == pytest.approx(80.0, abs=1.0)

    def test_score_cannot_be_negative(self):
        """Test that score doesn't go below zero."""
        profile = QualityProfile(
            num_rows=100,
            num_columns=5,
            memory_usage_bytes=10000,
            total_nulls=450,
            null_percentage=90.0,  # 90% nulls
            duplicate_rows=80,
            duplicate_percentage=80.0,  # 80% duplicates
        )

        score = _calculate_quality_score(profile)

        assert score >= 0.0
        assert score <= 100.0
