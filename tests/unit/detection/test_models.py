"""
Unit tests for detection.models module.
"""

import pytest

from src.detection.models import DetectionSummary, PIIDetection, create_detection_summary


class TestPIIDetection:
    """Tests for PIIDetection dataclass."""

    def test_create_detection(self):
        """Test creating a PIIDetection."""
        detection = PIIDetection(
            column="email",
            row_index=0,
            pii_type="EMAIL",
            value="test@example.com",
            start_position=0,
            end_position=16,
            confidence=0.95,
            detection_method="rule_based",
        )

        assert detection.column == "email"
        assert detection.pii_type == "EMAIL"
        assert detection.confidence == 0.95

    def test_invalid_confidence(self):
        """Test that invalid confidence raises error."""
        with pytest.raises(ValueError):
            PIIDetection(
                column="test",
                row_index=0,
                pii_type="EMAIL",
                value="test",
                start_position=0,
                end_position=4,
                confidence=1.5,  # Invalid
                detection_method="rule_based",
            )

    def test_detection_with_metadata(self):
        """Test detection with metadata."""
        detection = PIIDetection(
            column="test",
            row_index=0,
            pii_type="EMAIL",
            value="test",
            start_position=0,
            end_position=4,
            confidence=0.8,
            detection_method="nlp",
            metadata={"key": "value"},
        )

        assert "key" in detection.metadata
        assert detection.metadata["key"] == "value"


class TestDetectionSummary:
    """Tests for DetectionSummary."""

    def test_empty_summary(self):
        """Test empty summary."""
        summary = DetectionSummary(total_detections=0)

        assert summary.total_detections == 0
        assert not summary.has_detections
        assert len(summary.detections_by_type) == 0

    def test_add_detection(self):
        """Test adding detections to summary."""
        summary = DetectionSummary(total_detections=0)

        detection = PIIDetection(
            column="email",
            row_index=0,
            pii_type="EMAIL",
            value="test@example.com",
            start_position=0,
            end_position=16,
            confidence=0.95,
            detection_method="rule_based",
        )

        summary.add_detection(detection)

        assert summary.detections_by_type["EMAIL"] == 1
        assert summary.detections_by_column["email"] == 1
        assert summary.detection_methods["rule_based"] == 1
        assert summary.confidence_distribution["high"] == 1

    def test_confidence_distribution(self):
        """Test confidence level classification."""
        summary = DetectionSummary(total_detections=0)

        # High confidence
        detection1 = PIIDetection(
            column="test",
            row_index=0,
            pii_type="EMAIL",
            value="test",
            start_position=0,
            end_position=4,
            confidence=0.9,
            detection_method="rule_based",
        )
        summary.add_detection(detection1)

        # Medium confidence
        detection2 = PIIDetection(
            column="test",
            row_index=1,
            pii_type="PHONE",
            value="test",
            start_position=0,
            end_position=4,
            confidence=0.6,
            detection_method="rule_based",
        )
        summary.add_detection(detection2)

        # Low confidence
        detection3 = PIIDetection(
            column="test",
            row_index=2,
            pii_type="SSN",
            value="test",
            start_position=0,
            end_position=4,
            confidence=0.3,
            detection_method="rule_based",
        )
        summary.add_detection(detection3)

        assert summary.confidence_distribution["high"] == 1
        assert summary.confidence_distribution["medium"] == 1
        assert summary.confidence_distribution["low"] == 1


class TestCreateDetectionSummary:
    """Tests for create_detection_summary function."""

    def test_create_summary_from_list(self):
        """Test creating summary from detection list."""
        detections = [
            PIIDetection(
                column="email",
                row_index=0,
                pii_type="EMAIL",
                value="test1@example.com",
                start_position=0,
                end_position=17,
                confidence=0.95,
                detection_method="rule_based",
            ),
            PIIDetection(
                column="email",
                row_index=1,
                pii_type="EMAIL",
                value="test2@example.com",
                start_position=0,
                end_position=17,
                confidence=0.95,
                detection_method="rule_based",
            ),
            PIIDetection(
                column="phone",
                row_index=0,
                pii_type="PHONE",
                value="555-1234",
                start_position=0,
                end_position=8,
                confidence=0.85,
                detection_method="nlp",
            ),
        ]

        summary = create_detection_summary(detections)

        assert summary.total_detections == 3
        assert summary.detections_by_type["EMAIL"] == 2
        assert summary.detections_by_type["PHONE"] == 1
        assert summary.affected_rows == 2  # rows 0 and 1
        assert summary.affected_columns == 2  # email and phone
        assert summary.detection_methods["rule_based"] == 2
        assert summary.detection_methods["nlp"] == 1

    def test_create_summary_empty_list(self):
        """Test creating summary from empty list."""
        summary = create_detection_summary([])

        assert summary.total_detections == 0
        assert not summary.has_detections
        assert summary.affected_rows == 0
        assert summary.affected_columns == 0
