"""
Anonymization strategy implementations.
"""

import hashlib
import logging
import re
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class AnonymizationStrategy(ABC):
    """Abstract base class for anonymization strategies."""

    @abstractmethod
    def transform(self, value: str, pii_type: str, **kwargs) -> str:
        """
        Transform a PII value.

        Args:
            value: Original PII value
            pii_type: Type of PII
            **kwargs: Strategy-specific parameters

        Returns:
            Transformed value
        """
        pass


class MaskStrategy(AnonymizationStrategy):
    """Mask PII with specified character."""

    def transform(
        self,
        value: str,
        pii_type: str,
        mask_char: str = "*",
        mask_percentage: float = 0.75,
        preserve_format: bool = True,
    ) -> str:
        """
        Mask PII value.

        Args:
            value: Original value
            pii_type: PII type
            mask_char: Character to use for masking
            mask_percentage: Percentage of characters to mask
            preserve_format: Keep format chars (-, @, etc.)

        Returns:
            Masked value
        """
        if not value:
            return value

        # Special handling for different PII types
        if pii_type == "EMAIL":
            return self._mask_email(value, mask_char)
        elif pii_type in ("PHONE", "PHONE_NUMBER"):
            return self._mask_phone(value, mask_char)
        elif pii_type in ("SSN", "US_SSN"):
            return self._mask_ssn(value, mask_char)
        elif pii_type == "CREDIT_CARD":
            return self._mask_credit_card(value, mask_char)
        else:
            return self._mask_generic(value, mask_char, mask_percentage, preserve_format)

    def _mask_email(self, email: str, mask_char: str) -> str:
        """Mask email: user@domain.com → u***@domain.com"""
        if "@" not in email:
            return mask_char * len(email)

        local, domain = email.split("@", 1)
        if len(local) <= 1:
            masked_local = mask_char
        else:
            masked_local = local[0] + mask_char * (len(local) - 1)

        return f"{masked_local}@{domain}"

    def _mask_phone(self, phone: str, mask_char: str) -> str:
        """Mask phone: 555-123-4567 → 555-***-****"""
        digits = re.sub(r"\D", "", phone)
        if len(digits) < 4:
            return mask_char * len(phone)

        # Keep first 3 digits, mask rest
        masked_digits = digits[:3] + mask_char * (len(digits) - 3)

        # Restore format
        original_format = re.sub(r"\d", "#", phone)
        result = []
        digit_idx = 0

        for char in original_format:
            if char == "#":
                result.append(masked_digits[digit_idx])
                digit_idx += 1
            else:
                result.append(char)

        return "".join(result)

    def _mask_ssn(self, ssn: str, mask_char: str) -> str:
        """Mask SSN: 123-45-6789 → ***-**-6789"""
        digits = re.sub(r"\D", "", ssn)
        if len(digits) < 4:
            return mask_char * len(ssn)

        # Keep last 4 digits
        masked_digits = mask_char * (len(digits) - 4) + digits[-4:]

        # Restore format
        if "-" in ssn:
            return f"{masked_digits[:3]}-{masked_digits[3:5]}-{masked_digits[5:]}"
        return masked_digits

    def _mask_credit_card(self, card: str, mask_char: str) -> str:
        """Mask credit card: 1234-5678-9012-3456 → ****-****-****-3456"""
        digits = re.sub(r"\D", "", card)
        if len(digits) < 4:
            return mask_char * len(card)

        # Keep last 4 digits
        masked_digits = mask_char * (len(digits) - 4) + digits[-4:]

        # Restore format
        original_format = re.sub(r"\d", "#", card)
        result = []
        digit_idx = 0

        for char in original_format:
            if char == "#":
                result.append(masked_digits[digit_idx])
                digit_idx += 1
            else:
                result.append(char)

        return "".join(result)

    def _mask_generic(
        self, value: str, mask_char: str, mask_percentage: float, preserve_format: bool
    ) -> str:
        """Generic masking for other PII types."""
        if preserve_format:
            # Mask letters and digits, preserve special chars
            result = []
            chars_to_mask = int(len(value) * mask_percentage)
            masked_count = 0

            for char in value:
                if char.isalnum() and masked_count < chars_to_mask:
                    result.append(mask_char)
                    masked_count += 1
                else:
                    result.append(char)

            return "".join(result)
        else:
            # Mask everything
            chars_to_mask = int(len(value) * mask_percentage)
            return mask_char * chars_to_mask + value[chars_to_mask:]


class RedactStrategy(AnonymizationStrategy):
    """Completely remove PII."""

    def transform(self, value: str, pii_type: str, **kwargs) -> str:
        """
        Redact PII value.

        Args:
            value: Original value
            pii_type: PII type

        Returns:
            Redacted placeholder
        """
        placeholder = kwargs.get("placeholder", "[REDACTED]")
        return placeholder


class PseudonymizeStrategy(AnonymizationStrategy):
    """Replace PII with consistent pseudonym."""

    def __init__(self, seed: str | None = None):
        """
        Initialize pseudonymizer.

        Args:
            seed: Seed for consistent hashing
        """
        self.seed = seed or "default_seed"

    def transform(self, value: str, pii_type: str, **kwargs) -> str:
        """
        Pseudonymize PII value using hashing.

        Args:
            value: Original value
            pii_type: PII type

        Returns:
            Pseudonymized value
        """
        if not value:
            return value

        # Hash with seed for consistency
        hash_input = f"{self.seed}:{value}".encode()
        hash_value = hashlib.sha256(hash_input).hexdigest()[:12]

        # Format based on PII type
        if pii_type == "EMAIL":
            return f"user_{hash_value}@example.com"
        elif pii_type in ("PHONE", "PHONE_NUMBER"):
            # Generate phone-like format
            return f"555-{hash_value[:3]}-{hash_value[3:7]}"
        elif pii_type in ("SSN", "US_SSN"):
            # Generate SSN-like format
            return f"{hash_value[:3]}-{hash_value[3:5]}-{hash_value[5:9]}"
        elif pii_type == "CREDIT_CARD":
            # Generate card-like format
            return f"****-****-****-{hash_value[:4]}"
        else:
            return f"{pii_type}_{hash_value}"


class GeneralizeStrategy(AnonymizationStrategy):
    """Generalize PII to broader category."""

    def transform(
        self, value: str, pii_type: str, level: str = "medium", **kwargs
    ) -> str:
        """
        Generalize PII value.

        Args:
            value: Original value
            pii_type: PII type
            level: Generalization level ("low", "medium", "high")

        Returns:
            Generalized value
        """
        if pii_type == "EMAIL":
            return self._generalize_email(value, level)
        elif pii_type in ("PHONE", "PHONE_NUMBER"):
            return self._generalize_phone(value, level)
        elif pii_type == "IP_ADDRESS":
            return self._generalize_ip(value, level)
        elif pii_type == "ZIP_CODE":
            return self._generalize_zip(value, level)
        else:
            return f"[{pii_type}]"

    def _generalize_email(self, email: str, level: str) -> str:
        """Generalize email address."""
        if "@" not in email:
            return "[EMAIL]"

        local, domain = email.split("@", 1)

        if level == "low":
            # Keep domain
            return f"[USER]@{domain}"
        elif level == "medium":
            # Keep domain TLD
            parts = domain.split(".")
            if len(parts) > 1:
                return f"[USER]@[DOMAIN].{parts[-1]}"
            return "[USER]@[DOMAIN]"
        else:  # high
            return "[EMAIL]"

    def _generalize_phone(self, phone: str, level: str) -> str:
        """Generalize phone number."""
        digits = re.sub(r"\D", "", phone)

        if level == "low":
            # Keep area code
            if len(digits) >= 3:
                return f"{digits[:3]}-XXX-XXXX"
            return "XXX-XXX-XXXX"
        elif level == "medium":
            # Keep country code only
            return "+X-XXX-XXX-XXXX"
        else:  # high
            return "[PHONE]"

    def _generalize_ip(self, ip: str, level: str) -> str:
        """Generalize IP address."""
        parts = ip.split(".")

        if level == "low":
            # Keep first two octets
            if len(parts) >= 2:
                return f"{parts[0]}.{parts[1]}.X.X"
            return "X.X.X.X"
        elif level == "medium":
            # Keep first octet
            if len(parts) >= 1:
                return f"{parts[0]}.X.X.X"
            return "X.X.X.X"
        else:  # high
            return "X.X.X.X"

    def _generalize_zip(self, zip_code: str, level: str) -> str:
        """Generalize ZIP code."""
        digits = re.sub(r"\D", "", zip_code)

        if level == "low":
            # Keep first 3 digits
            if len(digits) >= 3:
                return f"{digits[:3]}XX"
            return "XXXXX"
        elif level == "medium":
            # Keep first 2 digits
            if len(digits) >= 2:
                return f"{digits[:2]}XXX"
            return "XXXXX"
        else:  # high
            return "XXXXX"
