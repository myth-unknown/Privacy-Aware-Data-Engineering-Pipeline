"""
Evaluation module for experimental analysis.
"""

from src.evaluation.dataset_generator import generate_synthetic_dataset
from src.evaluation.metrics import MetricsResult, calculate_metrics
from src.evaluation.models import Entity, GroundTruthAnnotation

__all__ = [
    "generate_synthetic_dataset",
    "GroundTruthAnnotation",
    "Entity",
    "calculate_metrics",
    "MetricsResult",
]
