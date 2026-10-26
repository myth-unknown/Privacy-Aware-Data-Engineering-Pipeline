"""
Unit tests for anonymization.transformer module.
"""

import pandas as pd

from src.anonymization.models import AnonymizationConfig
from src.anonymization.transformer import DataTransformer, anonymize_dataframe
from src.detection.models import PIIDetection


class TestDataTransformer:
    """Tests for DataTransformer."""

    def test_transform_mask_strategy(self):
        """Test transformation with mask strategy."""
        df = pd.DataFrame({"email": ["test@example.com", "another@test.com"]})

        detections = [
            PIIDetection(
                column="email",
                row_index=0,
                pii_type="EMAIL",
                value="test@example.com",
                start_position=0,
                end_position=16,
                confidence=0.9,
                detection_method="rule_based",
            )
        ]

        config = AnonymizationConfig(strategy="mask", pii_type="EMAIL")
        transformer = DataTransformer()
        result = transformer.transform(df, detections, config)

        assert result.success
        assert result.audit.total_transformations == 1
        assert "test@example.com" not in result.data["email"].values
        assert "@example.com" in result.data.at[0, "email"]  # Domain preserved

    def test_transform_redact_strategy(self):
        """Test transformation with redact strategy."""
        df = pd.DataFrame({"ssn": ["123-45-6789"]})

        detections = [
            PIIDetection(
                column="ssn",
                row_index=0,
                pii_type="SSN",
                value="123-45-6789",
                start_position=0,
                end_position=11,
                confidence=0.95,
                detection_method="rule_based",
            )
        ]

        config = AnonymizationConfig(strategy="redact", pii_type="SSN")
        transformer = DataTransformer()
        result = transformer.transform(df, detections, config)

        assert result.success
        assert result.data.at[0, "ssn"] == "[REDACTED]"

    def test_transform_multiple_detections(self):
        """Test transformation with multiple detections."""
        df = pd.DataFrame(
            {"data": ["Email: test@example.com Phone: 555-1234"]}
        )

        detections = [
            PIIDetection(
                column="data",
                row_index=0,
                pii_type="EMAIL",
                value="test@example.com",
                start_position=7,
                end_position=23,
                confidence=0.9,
                detection_method="rule_based",
            ),
            PIIDetection(
                column="data",
                row_index=0,
                pii_type="PHONE",
                value="555-1234",
                start_position=31,
                end_position=39,
                confidence=0.8,
                detection_method="rule_based",
            ),
        ]

        config = AnonymizationConfig(strategy="redact", pii_type="ALL")
        transformer = DataTransformer()
        result = transformer.transform(df, detections, config)

        assert result.success
        assert result.audit.total_transformations == 2
        assert "test@example.com" not in result.data.at[0, "data"]
        assert "555-1234" not in result.data.at[0, "data"]

    def test_filter_by_pii_type(self):
        """Test filtering detections by PII type."""
        df = pd.DataFrame({"data": ["test@example.com and 555-1234"]})

        detections = [
            PIIDetection(
                column="data",
                row_index=0,
                pii_type="EMAIL",
                value="test@example.com",
                start_position=0,
                end_position=16,
                confidence=0.9,
                detection_method="rule_based",
            ),
            PIIDetection(
                column="data",
                row_index=0,
                pii_type="PHONE",
                value="555-1234",
                start_position=21,
                end_position=29,
                confidence=0.8,
                detection_method="rule_based",
            ),
        ]

        # Only anonymize EMAIL
        config = AnonymizationConfig(strategy="redact", pii_type="EMAIL")
        transformer = DataTransformer()
        result = transformer.transform(df, detections, config)

        assert result.success
        assert result.audit.total_transformations == 1
        assert "test@example.com" not in result.data.at[0, "data"]
        assert "555-1234" in result.data.at[0, "data"]  # Phone unchanged

    def test_unknown_strategy(self):
        """Test error on unknown strategy."""
        df = pd.DataFrame({"col": ["value"]})
        detections = []

        config = AnonymizationConfig(strategy="invalid", pii_type="ALL")
        transformer = DataTransformer()
        result = transformer.transform(df, detections, config)

        assert not result.success
        assert len(result.errors) > 0


class TestAnonymizeDataFrame:
    """Tests for convenience function."""

    def test_anonymize_dataframe_convenience(self):
        """Test convenience function."""
        df = pd.DataFrame({"email": ["test@example.com"]})

        detections = [
            PIIDetection(
                column="email",
                row_index=0,
                pii_type="EMAIL",
                value="test@example.com",
                start_position=0,
                end_position=16,
                confidence=0.9,
                detection_method="rule_based",
            )
        ]

        result = anonymize_dataframe(df, detections, strategy="mask", pii_type="EMAIL")

        assert result.success
        assert result.audit.total_transformations == 1

    def test_anonymize_empty_detections(self):
        """Test anonymization with no detections."""
        df = pd.DataFrame({"data": ["no pii here"]})
        detections = []

        result = anonymize_dataframe(df, detections, strategy="mask")

        assert result.success
        assert result.audit.total_transformations == 0
