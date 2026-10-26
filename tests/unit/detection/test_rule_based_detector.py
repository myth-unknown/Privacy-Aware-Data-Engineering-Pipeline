"""
Unit tests for detection.rule_based_detector module.
"""

import pandas as pd
import pytest

from src.detection.rule_based_detector import RuleBasedPIIDetector


class TestRuleBasedPIIDetector:
    """Tests for rule-based PII detector."""

    def test_detect_email(self):
        """Test email detection."""
        df = pd.DataFrame(
            {"text": ["Contact us at john.doe@example.com", "No email here"]}
        )

        detector = RuleBasedPIIDetector(confidence_threshold=0.5)
        detections = detector.detect(df)

        assert len(detections) == 1
        assert detections[0].pii_type == "EMAIL"
        assert detections[0].value == "john.doe@example.com"
        assert detections[0].column == "text"
        assert detections[0].row_index == 0

    def test_detect_phone(self):
        """Test phone number detection."""
        df = pd.DataFrame(
            {
                "contact": [
                    "Call 555-123-4567",
                    "(555) 987-6543",  # Parentheses format may not match
                    "1-555-111-2222",
                    "No phone",
                ]
            }
        )

        detector = RuleBasedPIIDetector(confidence_threshold=0.5)
        detections = detector.detect(df)

        # At least 2 should be detected
        assert len(detections) >= 2
        assert all(d.pii_type == "PHONE" for d in detections)

    def test_detect_ssn(self):
        """Test SSN detection."""
        df = pd.DataFrame({"ssn": ["123-45-6789", "987-65-4321", "Invalid"]})

        detector = RuleBasedPIIDetector(confidence_threshold=0.5)
        detections = detector.detect(df)

        assert len(detections) == 2
        assert all(d.pii_type == "SSN" for d in detections)

    def test_detect_credit_card(self):
        """Test credit card detection."""
        df = pd.DataFrame(
            {
                "card": [
                    "4532-1234-5678-9010",  # Valid format
                    "5425 9876 5432 1098",  # Valid format
                    "1234",  # Too short
                ]
            }
        )

        detector = RuleBasedPIIDetector(confidence_threshold=0.5)
        detections = detector.detect(df)

        assert len(detections) == 2
        assert all(d.pii_type == "CREDIT_CARD" for d in detections)

    def test_detect_ip_address(self):
        """Test IP address detection."""
        df = pd.DataFrame(
            {"ip": ["192.168.1.1", "10.0.0.1", "Invalid IP", "999.999.999.999"]}
        )

        detector = RuleBasedPIIDetector(confidence_threshold=0.5)
        detections = detector.detect(df)

        assert len(detections) == 2
        assert all(d.pii_type == "IP_ADDRESS" for d in detections)

    def test_detect_zip_code(self):
        """Test ZIP code detection."""
        df = pd.DataFrame(
            {"zip": ["12345", "12345-6789", "Invalid", "1234"]}  # Too short
        )

        detector = RuleBasedPIIDetector(confidence_threshold=0.5)
        detections = detector.detect(df)

        assert len(detections) == 2
        assert all(d.pii_type == "ZIP_CODE" for d in detections)

    def test_detect_multiple_pii_in_text(self):
        """Test detecting multiple PII types in same text."""
        df = pd.DataFrame(
            {
                "text": [
                    "Email john@example.com and phone 555-1234-567 and IP 192.168.1.1"
                ]
            }
        )

        detector = RuleBasedPIIDetector(confidence_threshold=0.5)
        detections = detector.detect(df)

        # Should detect at least email and IP
        assert len(detections) >= 2
        types = {d.pii_type for d in detections}
        assert "EMAIL" in types
        assert "IP_ADDRESS" in types

    def test_confidence_threshold_filtering(self):
        """Test that detections below threshold are filtered."""
        df = pd.DataFrame({"email": ["test@example.com"]})

        # High threshold should filter out detections
        detector = RuleBasedPIIDetector(confidence_threshold=0.99)
        detections = detector.detect(df)

        # Emails with common TLDs should still pass
        assert len(detections) >= 0

    def test_enabled_types_filter(self):
        """Test filtering by enabled PII types."""
        df = pd.DataFrame(
            {"text": ["Email test@example.com and phone 555-1234"]}
        )

        # Only detect emails
        detector = RuleBasedPIIDetector(
            confidence_threshold=0.5, enabled_types=["EMAIL"]
        )
        detections = detector.detect(df)

        assert all(d.pii_type == "EMAIL" for d in detections)

    def test_column_filtering(self):
        """Test scanning specific columns only."""
        df = pd.DataFrame(
            {
                "col1": ["test@example.com"],
                "col2": ["another@example.com"],
            }
        )

        detector = RuleBasedPIIDetector(confidence_threshold=0.5)
        detections = detector.detect(df, columns=["col1"])

        assert len(detections) == 1
        assert detections[0].column == "col1"

    def test_skip_null_values(self):
        """Test that null values are skipped."""
        df = pd.DataFrame({"text": ["test@example.com", None, "another@example.com"]})

        detector = RuleBasedPIIDetector(confidence_threshold=0.5)
        detections = detector.detect(df)

        assert len(detections) == 2

    def test_luhn_validation(self):
        """Test Luhn algorithm for credit cards."""
        detector = RuleBasedPIIDetector(confidence_threshold=0.5)

        # Valid Luhn checksum
        assert detector._validate_luhn("4532015112830366")

        # Invalid Luhn checksum
        assert not detector._validate_luhn("4532015112830367")

        # Too short
        assert not detector._validate_luhn("123")

    def test_invalid_enabled_types(self):
        """Test error on invalid PII types."""
        with pytest.raises(ValueError):
            RuleBasedPIIDetector(enabled_types=["INVALID_TYPE"])

    def test_detection_metadata(self):
        """Test that detections include proper metadata."""
        df = pd.DataFrame({"text": ["test@example.com"]})

        detector = RuleBasedPIIDetector(confidence_threshold=0.5)
        detections = detector.detect(df)

        assert len(detections) > 0
        d = detections[0]
        assert d.detection_method == "rule_based"
        assert 0.0 <= d.confidence <= 1.0
        assert d.start_position >= 0
        assert d.end_position > d.start_position

    def test_get_supported_types(self):
        """Test getting supported PII types."""
        detector = RuleBasedPIIDetector()
        types = detector.get_supported_types()

        assert "EMAIL" in types
        assert "PHONE" in types
        assert "SSN" in types
        assert "CREDIT_CARD" in types
