"""
PII detection module with rule-based and NLP detectors.
"""

from src.detection.base_detector import PIIDetector
from src.detection.detector_factory import create_detector, detect_pii
from src.detection.models import DetectionSummary, PIIDetection, create_detection_summary
from src.detection.rule_based_detector import RuleBasedPIIDetector

__all__ = [
    "PIIDetection",
    "DetectionSummary",
    "create_detection_summary",
    "PIIDetector",
    "RuleBasedPIIDetector",
    "create_detector",
    "detect_pii",
]

# Optional NLP detector
try:
    from src.detection.nlp_detector import PresidioDetector

    __all__.append("PresidioDetector")
except (ImportError, RuntimeError):
    pass
