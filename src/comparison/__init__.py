"""
Method comparison module for PII detection.
"""

from src.comparison.comparator import compare_detection_methods
from src.comparison.models import ComparisonResult, MethodMetrics

__all__ = [
    "compare_detection_methods",
    "ComparisonResult",
    "MethodMetrics",
]
