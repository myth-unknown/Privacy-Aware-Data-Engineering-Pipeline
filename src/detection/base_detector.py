"""
Abstract base class for PII detectors.
"""

from abc import ABC, abstractmethod

import pandas as pd

from src.detection.models import PIIDetection


class PIIDetector(ABC):
    """Abstract base class for all PII detectors."""

    def __init__(self, confidence_threshold: float = 0.5):
        """
        Initialize detector.

        Args:
            confidence_threshold: Minimum confidence score to report detection (0.0-1.0)
        """
        if not 0.0 <= confidence_threshold <= 1.0:
            raise ValueError("confidence_threshold must be between 0.0 and 1.0")
        self.confidence_threshold = confidence_threshold

    @abstractmethod
    def detect(self, df: pd.DataFrame, columns: list[str] | None = None) -> list[PIIDetection]:
        """
        Detect PII in DataFrame.

        Args:
            df: DataFrame to scan for PII
            columns: Optional list of columns to check (None = all columns)

        Returns:
            List of PIIDetection objects
        """
        pass

    @abstractmethod
    def get_supported_types(self) -> list[str]:
        """
        Get list of PII types this detector can find.

        Returns:
            List of PII type strings (e.g., ["EMAIL", "PHONE"])
        """
        pass

    def _filter_by_confidence(self, detections: list[PIIDetection]) -> list[PIIDetection]:
        """Filter detections by confidence threshold."""
        return [d for d in detections if d.confidence >= self.confidence_threshold]

    def _get_target_columns(self, df: pd.DataFrame, columns: list[str] | None) -> list[str]:
        """
        Get list of columns to scan.

        Args:
            df: DataFrame
            columns: Optional column list

        Returns:
            List of column names to scan
        """
        if columns is None:
            # Only scan string/object columns
            return df.select_dtypes(include=["object", "string"]).columns.tolist()
        return [col for col in columns if col in df.columns]
