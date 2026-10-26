"""
Rule-based PII detectors using regular expressions.
"""

import logging
import re

import pandas as pd

from src.detection.base_detector import PIIDetector
from src.detection.models import PIIDetection

logger = logging.getLogger(__name__)

# Regex patterns for common PII types
PATTERNS = {
    "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    "PHONE": r"\b(?:\+?1[-.]?)?\(?([0-9]{3})\)?[-.]?([0-9]{3})[-.]?([0-9]{4})\b",
    "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
    "CREDIT_CARD": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
    "IP_ADDRESS": r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b",
    "ZIP_CODE": r"\b\d{5}(?:-\d{4})?\b",
}


class RuleBasedPIIDetector(PIIDetector):
    """Rule-based PII detector using regular expressions."""

    def __init__(
        self,
        confidence_threshold: float = 0.5,
        enabled_types: list[str] | None = None,
    ):
        """
        Initialize rule-based detector.

        Args:
            confidence_threshold: Minimum confidence to report
            enabled_types: PII types to detect (None = all types)
        """
        super().__init__(confidence_threshold)

        if enabled_types is None:
            self.enabled_types = list(PATTERNS.keys())
        else:
            # Validate types
            invalid = set(enabled_types) - set(PATTERNS.keys())
            if invalid:
                raise ValueError(f"Invalid PII types: {invalid}")
            self.enabled_types = enabled_types

        # Compile patterns
        self.compiled_patterns = {
            pii_type: re.compile(pattern)
            for pii_type, pattern in PATTERNS.items()
            if pii_type in self.enabled_types
        }

    def get_supported_types(self) -> list[str]:
        """Get supported PII types."""
        return self.enabled_types

    def detect(self, df: pd.DataFrame, columns: list[str] | None = None) -> list[PIIDetection]:
        """
        Detect PII using regex patterns.

        Args:
            df: DataFrame to scan
            columns: Optional column list

        Returns:
            List of PIIDetection objects
        """
        detections = []
        target_columns = self._get_target_columns(df, columns)

        logger.info(f"Scanning {len(target_columns)} columns with {len(self.enabled_types)} patterns")

        for col in target_columns:
            for row_idx, value in df[col].items():
                if pd.isna(value):
                    continue

                text = str(value)
                col_detections = self._scan_text(text, col, row_idx)
                detections.extend(col_detections)

        # Filter by confidence
        detections = self._filter_by_confidence(detections)

        logger.info(f"Found {len(detections)} PII instances")
        return detections

    def _scan_text(self, text: str, column: str, row_index: int) -> list[PIIDetection]:
        """Scan text for all PII patterns."""
        detections = []

        for pii_type, pattern in self.compiled_patterns.items():
            matches = pattern.finditer(text)

            for match in matches:
                # Additional validation
                value = match.group(0)
                confidence = self._calculate_confidence(pii_type, value)

                if confidence >= self.confidence_threshold:
                    detection = PIIDetection(
                        column=column,
                        row_index=row_index,
                        pii_type=pii_type,
                        value=value,
                        start_position=match.start(),
                        end_position=match.end(),
                        confidence=confidence,
                        detection_method="rule_based",
                    )
                    detections.append(detection)

        return detections

    def _calculate_confidence(self, pii_type: str, value: str) -> float:
        """
        Calculate confidence score for a detection.

        Args:
            pii_type: Type of PII detected
            value: The detected value

        Returns:
            Confidence score (0.0-1.0)
        """
        # Base confidence for regex match
        confidence = 0.8

        # Additional validation increases confidence
        if pii_type == "CREDIT_CARD":
            if self._validate_luhn(value):
                confidence = 0.95
            else:
                confidence = 0.5  # Might be false positive

        elif pii_type == "EMAIL":
            # Check for common TLDs
            if any(value.endswith(tld) for tld in [".com", ".org", ".net", ".edu", ".gov"]):
                confidence = 0.95

        elif pii_type == "PHONE":
            # US phone numbers with proper formatting
            if re.match(r"^\+?1[-.]?\(\d{3}\)[-.]?\d{3}[-.]?\d{4}$", value):
                confidence = 0.95

        elif pii_type == "SSN":
            # SSNs with proper formatting are highly confident
            confidence = 0.95

        elif pii_type == "IP_ADDRESS":
            # Check if not a reserved IP
            parts = [int(p) for p in value.split(".")]
            if parts[0] in [0, 127, 255]:  # Reserved ranges
                confidence = 0.6
            else:
                confidence = 0.9

        return confidence

    def _validate_luhn(self, card_number: str) -> bool:
        """
        Validate credit card number using Luhn algorithm.

        Args:
            card_number: Card number string (may contain spaces/hyphens)

        Returns:
            True if valid, False otherwise
        """
        # Remove non-digits
        digits = re.sub(r"\D", "", card_number)

        if not digits or len(digits) < 13 or len(digits) > 19:
            return False

        # Luhn algorithm
        checksum = 0
        is_second = False

        for i in range(len(digits) - 1, -1, -1):
            digit = int(digits[i])

            if is_second:
                digit *= 2
                if digit > 9:
                    digit -= 9

            checksum += digit
            is_second = not is_second

        return checksum % 10 == 0
