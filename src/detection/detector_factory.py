"""
Factory for creating PII detectors.
"""

import logging
from typing import Literal

from src.detection.base_detector import PIIDetector
from src.detection.rule_based_detector import RuleBasedPIIDetector

logger = logging.getLogger(__name__)

# Try to import NLP detector (optional)
try:
    from src.detection.nlp_detector import PresidioDetector

    NLP_AVAILABLE = True
except (ImportError, RuntimeError):
    NLP_AVAILABLE = False
    logger.warning("NLP detector not available")


DetectorType = Literal["rule_based", "nlp", "hybrid"]


def create_detector(
    method: DetectorType,
    confidence_threshold: float = 0.5,
    **kwargs,
) -> PIIDetector | dict[str, PIIDetector]:
    """
    Factory function to create PII detectors.

    Args:
        method: Detection method ("rule_based", "nlp", or "hybrid")
        confidence_threshold: Minimum confidence threshold
        **kwargs: Additional detector-specific arguments

    Returns:
        PIIDetector instance or dict of detectors (for hybrid mode)

    Raises:
        ValueError: If invalid method or NLP not available
    """
    if method == "rule_based":
        logger.info("Creating rule-based detector")
        return RuleBasedPIIDetector(
            confidence_threshold=confidence_threshold,
            enabled_types=kwargs.get("enabled_types"),
        )

    elif method == "nlp":
        if not NLP_AVAILABLE:
            raise ValueError(
                "NLP detector not available. Presidio and spaCy must be installed."
            )

        logger.info("Creating NLP detector (Presidio)")
        return PresidioDetector(
            confidence_threshold=confidence_threshold,
            language=kwargs.get("language", "en"),
            entities=kwargs.get("entities"),
        )

    elif method == "hybrid":
        logger.info("Creating hybrid detector (rule-based + NLP)")

        detectors = {
            "rule_based": RuleBasedPIIDetector(
                confidence_threshold=confidence_threshold,
                enabled_types=kwargs.get("enabled_types"),
            )
        }

        if NLP_AVAILABLE:
            detectors["nlp"] = PresidioDetector(
                confidence_threshold=confidence_threshold,
                language=kwargs.get("language", "en"),
                entities=kwargs.get("entities"),
            )
        else:
            logger.warning("NLP detector not available, hybrid mode will use rule-based only")

        return detectors

    else:
        raise ValueError(f"Unknown detection method: {method}")


def detect_pii(
    df,
    method: DetectorType = "rule_based",
    confidence_threshold: float = 0.5,
    columns: list[str] | None = None,
    **kwargs,
):
    """
    Convenience function to detect PII in DataFrame.

    Args:
        df: DataFrame to scan
        method: Detection method
        confidence_threshold: Minimum confidence
        columns: Optional column list
        **kwargs: Additional detector arguments

    Returns:
        List of PIIDetection objects
    """
    detector_or_dict = create_detector(method, confidence_threshold, **kwargs)

    if isinstance(detector_or_dict, dict):
        # Hybrid mode - combine results
        all_detections = []
        for _detector_name, detector in detector_or_dict.items():
            detections = detector.detect(df, columns)
            all_detections.extend(detections)
        return all_detections
    else:
        # Single detector
        return detector_or_dict.detect(df, columns)
