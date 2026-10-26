"""
Tests for evaluation metrics.
"""

import pytest

from src.detection.models import PIIDetection
from src.evaluation import calculate_metrics
from src.evaluation.metrics import MetricsResult


@pytest.fixture
def sample_ground_truth():
    """Sample ground truth annotations."""
    from src.evaluation.models import Entity, GroundTruthAnnotation
    annotation = GroundTruthAnnotation(text="Email: test@example.com Phone: 555-1234")
    annotation.add_entity(Entity(7, 23, "EMAIL", "test@example.com"))
    annotation.add_entity(Entity(31, 39, "PHONE", "555-1234"))
    return [annotation]


@pytest.fixture
def sample_predictions():
    """Sample predictions."""
    return [
        PIIDetection(
            row_index=0,
            column="text",
            pii_type="EMAIL",
            value="test@example.com",
            start_position=7,
            end_position=23,
            confidence=0.95,
            detection_method="rule_based",
        ),
        PIIDetection(
            row_index=0,
            column="text",
            pii_type="PHONE",
            value="555-1234",
            start_position=31,
            end_position=39,
            confidence=0.90,
            detection_method="rule_based",
        ),
    ]


class TestCalculateMetrics:
    """Tests for calculate_metrics function."""

    def test_perfect_predictions(self, sample_ground_truth, sample_predictions):
        """Test metrics with perfect predictions."""
        metrics = calculate_metrics(sample_ground_truth, sample_predictions)

        assert isinstance(metrics, MetricsResult)
        assert metrics.precision == 1.0
        assert metrics.recall == 1.0
        assert metrics.f1_score == 1.0
        assert metrics.true_positives == 2
        assert metrics.false_positives == 0
        assert metrics.false_negatives == 0

    def test_no_predictions(self, sample_ground_truth):
        """Test metrics with no predictions."""
        metrics = calculate_metrics(sample_ground_truth, [])

        assert metrics.precision == 0.0
        assert metrics.recall == 0.0
        assert metrics.f1_score == 0.0

    def test_no_ground_truth(self, sample_predictions):
        """Test metrics with no ground truth."""
        metrics = calculate_metrics([], sample_predictions)

        assert metrics.precision == 0.0
        assert metrics.false_positives == 2


class TestMetricsResult:
    """Tests for MetricsResult model."""

    def test_metrics_result_creation(self):
        """Test creating MetricsResult."""
        result = MetricsResult(
            precision=0.9,
            recall=0.85,
            f1_score=0.87,
            true_positives=10,
            false_positives=1,
            false_negatives=2
        )

        assert result.precision == 0.9
        assert result.recall == 0.85
        assert result.f1_score == 0.87

    def test_total_predictions_property(self):
        """Test total predictions property."""
        result = MetricsResult(true_positives=10, false_positives=3)
        assert result.total_predictions == 13

    def test_total_ground_truth_property(self):
        """Test total ground truth property."""
        result = MetricsResult(true_positives=10, false_negatives=2)
        assert result.total_ground_truth == 12
