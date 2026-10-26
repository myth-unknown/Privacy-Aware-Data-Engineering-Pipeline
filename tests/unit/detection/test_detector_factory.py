"""
Unit tests for detection.detector_factory module.
"""

import pandas as pd
import pytest

from src.detection.base_detector import PIIDetector
from src.detection.detector_factory import create_detector, detect_pii
from src.detection.rule_based_detector import RuleBasedPIIDetector


class TestCreateDetector:
    """Tests for detector factory."""

    def test_create_rule_based_detector(self):
        """Test creating rule-based detector."""
        detector = create_detector("rule_based", confidence_threshold=0.7)

        assert isinstance(detector, RuleBasedPIIDetector)
        assert detector.confidence_threshold == 0.7

    def test_create_rule_based_with_types(self):
        """Test creating rule-based with specific types."""
        detector = create_detector(
            "rule_based", confidence_threshold=0.5, enabled_types=["EMAIL", "PHONE"]
        )

        assert isinstance(detector, RuleBasedPIIDetector)
        assert set(detector.get_supported_types()) == {"EMAIL", "PHONE"}

    @pytest.mark.skip(reason="spaCy initialization issue on some systems")
    def test_create_hybrid_detector(self):
        """Test creating hybrid detector."""
        result = create_detector("hybrid", confidence_threshold=0.6)

        assert isinstance(result, dict)
        assert "rule_based" in result
        assert isinstance(result["rule_based"], PIIDetector)

        # NLP detector may fail to initialize due to spaCy issues
        # This is acceptable - hybrid degrades to rule-based only

    def test_invalid_method(self):
        """Test error on invalid method."""
        with pytest.raises(ValueError):
            create_detector("invalid_method")


class TestDetectPII:
    """Tests for convenience function."""

    def test_detect_pii_rule_based(self):
        """Test detecting PII with rule-based method."""
        df = pd.DataFrame({"email": ["test@example.com", "another@test.com"]})

        detections = detect_pii(df, method="rule_based", confidence_threshold=0.5)

        assert len(detections) >= 2
        assert all(hasattr(d, "pii_type") for d in detections)

    def test_detect_pii_with_column_filter(self):
        """Test detecting PII with column filter."""
        df = pd.DataFrame(
            {
                "col1": ["test@example.com"],
                "col2": ["another@example.com"],
            }
        )

        detections = detect_pii(
            df, method="rule_based", confidence_threshold=0.5, columns=["col1"]
        )

        assert all(d.column == "col1" for d in detections)

    def test_detect_pii_empty_dataframe(self):
        """Test detecting PII in empty DataFrame."""
        df = pd.DataFrame({"text": []})

        detections = detect_pii(df, method="rule_based")

        assert len(detections) == 0

    def test_detect_pii_no_pii(self):
        """Test detecting PII when none exists."""
        df = pd.DataFrame({"text": ["This is clean text", "No PII here"]})

        detections = detect_pii(df, method="rule_based", confidence_threshold=0.5)

        assert len(detections) == 0
