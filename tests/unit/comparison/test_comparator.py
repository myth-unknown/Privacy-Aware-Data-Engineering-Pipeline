"""
Tests for detection method comparison.
"""

import pandas as pd
import pytest

from src.comparison import compare_detection_methods
from src.comparison.models import ComparisonResult, MethodMetrics


@pytest.fixture
def sample_df():
    """Sample DataFrame with PII."""
    return pd.DataFrame({
        "name": ["John Doe", "Jane Smith"],
        "email": ["john@example.com", "jane@example.com"],
        "phone": ["555-1234", "555-5678"],
        "age": [30, 25],
    })


class TestCompareDetectionMethods:
    """Tests for compare_detection_methods function."""

    def test_compare_two_methods(self, sample_df):
        """Test comparing two methods."""
        result = compare_detection_methods(
            sample_df,
            methods=["rule_based", "nlp"],
            confidence_threshold=0.5,
        )

        assert isinstance(result, ComparisonResult)
        assert len(result.method_metrics) == 2
        assert "rule_based" in result.method_metrics
        assert "nlp" in result.method_metrics

    def test_compare_single_method(self, sample_df):
        """Test comparing single method."""
        result = compare_detection_methods(
            sample_df,
            methods=["rule_based"],
            confidence_threshold=0.5,
        )

        assert len(result.method_metrics) == 1
        assert "rule_based" in result.method_metrics

    def test_default_methods(self, sample_df):
        """Test with default methods."""
        result = compare_detection_methods(sample_df)

        assert len(result.method_metrics) >= 1  # At least rule_based should work

    def test_dataset_metadata(self, sample_df):
        """Test dataset metadata is captured."""
        result = compare_detection_methods(sample_df, methods=["rule_based"])

        assert result.total_rows == 2
        assert result.total_columns == 4

    def test_method_metrics_populated(self, sample_df):
        """Test method metrics are populated."""
        result = compare_detection_methods(sample_df, methods=["rule_based"])

        metrics = result.method_metrics["rule_based"]
        assert isinstance(metrics, MethodMetrics)
        assert metrics.method_name == "rule_based"
        assert metrics.execution_time_seconds >= 0
        assert metrics.rows_scanned == 2
        assert metrics.columns_scanned == 4

    def test_detections_found(self, sample_df):
        """Test detections are found."""
        result = compare_detection_methods(sample_df, methods=["rule_based"])

        metrics = result.method_metrics["rule_based"]
        # Should find at least emails
        assert metrics.total_detections >= 2

    def test_confidence_threshold_filtering(self, sample_df):
        """Test confidence threshold filters detections."""
        result_low = compare_detection_methods(
            sample_df, methods=["rule_based"], confidence_threshold=0.1
        )
        result_high = compare_detection_methods(
            sample_df, methods=["rule_based"], confidence_threshold=0.9
        )

        # Low threshold should have more or equal detections
        metrics_low = result_low.method_metrics["rule_based"]
        metrics_high = result_high.method_metrics["rule_based"]
        assert metrics_low.total_detections >= metrics_high.total_detections

    def test_column_filtering(self, sample_df):
        """Test column filtering works."""
        result_all = compare_detection_methods(sample_df, methods=["rule_based"])
        result_filtered = compare_detection_methods(
            sample_df, methods=["rule_based"], columns=["email"]
        )

        metrics_all = result_all.method_metrics["rule_based"]
        metrics_filtered = result_filtered.method_metrics["rule_based"]

        assert metrics_filtered.columns_scanned == 1
        assert metrics_filtered.total_detections <= metrics_all.total_detections

    def test_recommendation_generated(self, sample_df):
        """Test recommendation is generated."""
        result = compare_detection_methods(sample_df, methods=["rule_based"])

        assert result.recommended_method != ""
        assert result.recommendation_reason != ""

    def test_fastest_method_property(self, sample_df):
        """Test fastest method property."""
        result = compare_detection_methods(sample_df, methods=["rule_based"])

        assert result.fastest_method != ""

    def test_most_detections_method_property(self, sample_df):
        """Test most detections method property."""
        result = compare_detection_methods(sample_df, methods=["rule_based"])

        assert result.most_detections_method != ""

    def test_highest_confidence_method_property(self, sample_df):
        """Test highest confidence method property."""
        result = compare_detection_methods(sample_df, methods=["rule_based"])

        assert result.highest_confidence_method != ""


class TestMethodMetrics:
    """Tests for MethodMetrics model."""

    def test_method_metrics_creation(self):
        """Test creating MethodMetrics."""
        metrics = MethodMetrics(
            method_name="rule_based",
            total_detections=10,
            execution_time_seconds=1.5,
        )

        assert metrics.method_name == "rule_based"
        assert metrics.total_detections == 10
        assert metrics.execution_time_seconds == 1.5

    def test_detections_by_type(self):
        """Test detections by type dict."""
        metrics = MethodMetrics(method_name="test")
        metrics.detections_by_type = {"email": 5, "phone": 3}

        assert metrics.detections_by_type["email"] == 5
        assert metrics.detections_by_type["phone"] == 3


class TestComparisonResult:
    """Tests for ComparisonResult model."""

    def test_comparison_result_creation(self):
        """Test creating ComparisonResult."""
        result = ComparisonResult(
            dataset_name="test_data",
            total_rows=100,
            total_columns=10,
        )

        assert result.dataset_name == "test_data"
        assert result.total_rows == 100
        assert result.total_columns == 10

    def test_add_method_metrics(self):
        """Test adding method metrics."""
        result = ComparisonResult()
        metrics = MethodMetrics(method_name="rule_based", total_detections=5)

        result.add_method_metrics(metrics)

        assert "rule_based" in result.method_metrics
        assert result.method_metrics["rule_based"].total_detections == 5

    def test_methods_compared_property(self):
        """Test methods compared property."""
        result = ComparisonResult()
        result.add_method_metrics(MethodMetrics(method_name="rule_based"))
        result.add_method_metrics(MethodMetrics(method_name="nlp"))

        assert len(result.methods_compared) == 2
        assert "rule_based" in result.methods_compared
        assert "nlp" in result.methods_compared

    def test_fastest_method_with_multiple_methods(self):
        """Test fastest method selection."""
        result = ComparisonResult()
        result.add_method_metrics(
            MethodMetrics(method_name="rule_based", execution_time_seconds=2.0)
        )
        result.add_method_metrics(
            MethodMetrics(method_name="nlp", execution_time_seconds=1.0)
        )

        assert result.fastest_method == "nlp"

    def test_most_detections_method_with_multiple_methods(self):
        """Test most detections method selection."""
        result = ComparisonResult()
        result.add_method_metrics(
            MethodMetrics(method_name="rule_based", total_detections=10)
        )
        result.add_method_metrics(MethodMetrics(method_name="nlp", total_detections=15))

        assert result.most_detections_method == "nlp"

    def test_highest_confidence_method_with_multiple_methods(self):
        """Test highest confidence method selection."""
        result = ComparisonResult()
        result.add_method_metrics(
            MethodMetrics(method_name="rule_based", avg_confidence=0.8)
        )
        result.add_method_metrics(MethodMetrics(method_name="nlp", avg_confidence=0.9))

        assert result.highest_confidence_method == "nlp"

    def test_empty_result_properties(self):
        """Test properties on empty result."""
        result = ComparisonResult()

        assert result.fastest_method == ""
        assert result.most_detections_method == ""
        assert result.highest_confidence_method == ""
        assert result.methods_compared == []
