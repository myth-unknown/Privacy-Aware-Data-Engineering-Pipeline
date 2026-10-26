"""
Unit tests for anonymization.strategies module.
"""


from src.anonymization.strategies import (
    GeneralizeStrategy,
    MaskStrategy,
    PseudonymizeStrategy,
    RedactStrategy,
)


class TestMaskStrategy:
    """Tests for MaskStrategy."""

    def test_mask_email(self):
        """Test email masking."""
        strategy = MaskStrategy()
        result = strategy.transform("john.doe@example.com", "EMAIL")

        assert result == "j*******@example.com"
        assert "@" in result
        assert "example.com" in result

    def test_mask_phone(self):
        """Test phone number masking."""
        strategy = MaskStrategy()
        result = strategy.transform("555-123-4567", "PHONE")

        assert result.startswith("555")
        assert "*" in result
        assert "-" in result  # Format preserved

    def test_mask_ssn(self):
        """Test SSN masking."""
        strategy = MaskStrategy()
        result = strategy.transform("123-45-6789", "SSN")

        assert result == "***-**-6789"
        assert result.endswith("6789")

    def test_mask_credit_card(self):
        """Test credit card masking."""
        strategy = MaskStrategy()
        result = strategy.transform("1234-5678-9012-3456", "CREDIT_CARD")

        assert result == "****-****-****-3456"
        assert result.endswith("3456")

    def test_mask_generic(self):
        """Test generic masking."""
        strategy = MaskStrategy()
        result = strategy.transform("SensitiveData123", "OTHER", mask_percentage=0.5)

        assert "*" in result
        assert len(result) == len("SensitiveData123")

    def test_custom_mask_char(self):
        """Test custom mask character."""
        strategy = MaskStrategy()
        result = strategy.transform("test@example.com", "EMAIL", mask_char="#")

        assert "#" in result
        assert "*" not in result


class TestRedactStrategy:
    """Tests for RedactStrategy."""

    def test_redact_default(self):
        """Test default redaction."""
        strategy = RedactStrategy()
        result = strategy.transform("sensitive@example.com", "EMAIL")

        assert result == "[REDACTED]"

    def test_redact_custom_placeholder(self):
        """Test custom placeholder."""
        strategy = RedactStrategy()
        result = strategy.transform("123-45-6789", "SSN", placeholder="[REMOVED]")

        assert result == "[REMOVED]"

    def test_redact_any_type(self):
        """Test redaction works for any PII type."""
        strategy = RedactStrategy()

        for pii_type in ["EMAIL", "PHONE", "SSN", "CREDIT_CARD"]:
            result = strategy.transform("test_value", pii_type)
            assert result == "[REDACTED]"


class TestPseudonymizeStrategy:
    """Tests for PseudonymizeStrategy."""

    def test_pseudonymize_email(self):
        """Test email pseudonymization."""
        strategy = PseudonymizeStrategy(seed="test")
        result = strategy.transform("john@example.com", "EMAIL")

        assert "@example.com" in result
        assert "user_" in result
        assert result != "john@example.com"

    def test_pseudonymize_phone(self):
        """Test phone pseudonymization."""
        strategy = PseudonymizeStrategy(seed="test")
        result = strategy.transform("555-123-4567", "PHONE")

        assert result.startswith("555-")
        assert "-" in result
        assert result != "555-123-4567"

    def test_pseudonymize_ssn(self):
        """Test SSN pseudonymization."""
        strategy = PseudonymizeStrategy(seed="test")
        result = strategy.transform("123-45-6789", "SSN")

        assert "-" in result
        assert len(result.replace("-", "")) == 9
        assert result != "123-45-6789"

    def test_pseudonymize_consistency(self):
        """Test that pseudonymization is consistent."""
        strategy = PseudonymizeStrategy(seed="test")

        result1 = strategy.transform("john@example.com", "EMAIL")
        result2 = strategy.transform("john@example.com", "EMAIL")

        assert result1 == result2

    def test_pseudonymize_different_seeds(self):
        """Test different seeds produce different results."""
        strategy1 = PseudonymizeStrategy(seed="seed1")
        strategy2 = PseudonymizeStrategy(seed="seed2")

        result1 = strategy1.transform("john@example.com", "EMAIL")
        result2 = strategy2.transform("john@example.com", "EMAIL")

        assert result1 != result2


class TestGeneralizeStrategy:
    """Tests for GeneralizeStrategy."""

    def test_generalize_email_low(self):
        """Test email generalization (low level)."""
        strategy = GeneralizeStrategy()
        result = strategy.transform("john@example.com", "EMAIL", level="low")

        assert "@example.com" in result
        assert "john" not in result

    def test_generalize_email_medium(self):
        """Test email generalization (medium level)."""
        strategy = GeneralizeStrategy()
        result = strategy.transform("john@example.com", "EMAIL", level="medium")

        assert ".com" in result
        assert "example" not in result

    def test_generalize_email_high(self):
        """Test email generalization (high level)."""
        strategy = GeneralizeStrategy()
        result = strategy.transform("john@example.com", "EMAIL", level="high")

        assert result == "[EMAIL]"

    def test_generalize_phone_low(self):
        """Test phone generalization (low level)."""
        strategy = GeneralizeStrategy()
        result = strategy.transform("555-123-4567", "PHONE", level="low")

        assert result.startswith("555")
        assert "XXX" in result

    def test_generalize_ip_low(self):
        """Test IP generalization (low level)."""
        strategy = GeneralizeStrategy()
        result = strategy.transform("192.168.1.1", "IP_ADDRESS", level="low")

        assert result.startswith("192.168")
        assert result.endswith(".X.X")

    def test_generalize_ip_high(self):
        """Test IP generalization (high level)."""
        strategy = GeneralizeStrategy()
        result = strategy.transform("192.168.1.1", "IP_ADDRESS", level="high")

        assert result == "X.X.X.X"

    def test_generalize_zip_low(self):
        """Test ZIP generalization (low level)."""
        strategy = GeneralizeStrategy()
        result = strategy.transform("12345", "ZIP_CODE", level="low")

        assert result.startswith("123")
        assert result.endswith("XX")

    def test_generalize_zip_high(self):
        """Test ZIP generalization (high level)."""
        strategy = GeneralizeStrategy()
        result = strategy.transform("12345", "ZIP_CODE", level="high")

        assert result == "XXXXX"
