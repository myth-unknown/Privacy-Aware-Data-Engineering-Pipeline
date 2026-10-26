"""
Evaluation metrics for PII detection performance.
"""

import logging
from dataclasses import dataclass

from src.detection.models import PIIDetection
from src.evaluation.models import GroundTruthAnnotation

logger = logging.getLogger(__name__)


@dataclass
class MetricsResult:
    """Evaluation metrics for detection performance."""

    # Overall metrics
    precision: float = 0.0
    recall: float = 0.0
    f1_score: float = 0.0
    accuracy: float = 0.0

    # Counts
    true_positives: int = 0
    false_positives: int = 0
    false_negatives: int = 0
    true_negatives: int = 0

    # Per-entity metrics
    entity_metrics: dict[str, dict[str, float]] = None

    def __post_init__(self):
        if self.entity_metrics is None:
            self.entity_metrics = {}

    @property
    def total_predictions(self) -> int:
        """Total predictions made."""
        return self.true_positives + self.false_positives

    @property
    def total_ground_truth(self) -> int:
        """Total ground truth entities."""
        return self.true_positives + self.false_negatives


def calculate_metrics(
    ground_truth: list[GroundTruthAnnotation],
    predictions: list[PIIDetection],
    iou_threshold: float = 0.5,
) -> MetricsResult:
    """
    Calculate evaluation metrics comparing predictions to ground truth.

    Args:
        ground_truth: List of ground truth annotations
        predictions: List of predicted PII detections
        iou_threshold: Intersection over union threshold for matching

    Returns:
        MetricsResult with precision, recall, F1, etc.
    """
    # Match predictions to ground truth
    tp, fp, fn = match_predictions_to_ground_truth(
        ground_truth, predictions, iou_threshold
    )

    # Calculate overall metrics
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1_score = (
        2 * (precision * recall) / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )

    # For accuracy, we'd need true negatives (TN)
    # In this context, TN is not well-defined, so we use F1 as main metric
    accuracy = f1_score  # Simplified

    result = MetricsResult(
        precision=precision,
        recall=recall,
        f1_score=f1_score,
        accuracy=accuracy,
        true_positives=tp,
        false_positives=fp,
        false_negatives=fn,
        true_negatives=0,  # Not applicable for entity detection
    )

    # Calculate per-entity-type metrics
    result.entity_metrics = calculate_per_entity_metrics(
        ground_truth, predictions, iou_threshold
    )

    logger.info(
        f"Metrics: P={precision:.3f}, R={recall:.3f}, F1={f1_score:.3f}, "
        f"TP={tp}, FP={fp}, FN={fn}"
    )

    return result


def match_predictions_to_ground_truth(
    ground_truth: list[GroundTruthAnnotation],
    predictions: list[PIIDetection],
    iou_threshold: float = 0.5,
) -> tuple[int, int, int]:
    """
    Match predictions to ground truth entities.

    Args:
        ground_truth: Ground truth annotations
        predictions: Predicted detections
        iou_threshold: IoU threshold for matching

    Returns:
        Tuple of (true_positives, false_positives, false_negatives)
    """
    # Build a map from text to entities
    gt_entities = []
    for annotation in ground_truth:
        for entity in annotation.entities:
            gt_entities.append(
                {
                    "text": annotation.text,
                    "start": entity.start,
                    "end": entity.end,
                    "type": entity.entity_type,
                    "matched": False,
                }
            )

    # Build prediction entities
    pred_entities = []
    for pred in predictions:
        pred_entities.append(
            {
                "row": pred.row_index,
                "column": pred.column,
                "start": pred.start_position,
                "end": pred.end_position,
                "type": pred.pii_type,
                "matched": False,
            }
        )

    # Match predictions to ground truth
    true_positives = 0
    for pred in pred_entities:
        for gt in gt_entities:
            if gt["matched"]:
                continue

            # Check if types match
            if pred["type"] != gt["type"]:
                continue

            # Calculate IoU (Intersection over Union)
            intersection_start = max(pred["start"], gt["start"])
            intersection_end = min(pred["end"], gt["end"])
            intersection = max(0, intersection_end - intersection_start)

            union_start = min(pred["start"], gt["start"])
            union_end = max(pred["end"], gt["end"])
            union = union_end - union_start

            iou = intersection / union if union > 0 else 0

            if iou >= iou_threshold:
                # Match found
                pred["matched"] = True
                gt["matched"] = True
                true_positives += 1
                break

    # Count unmatched
    false_positives = sum(1 for pred in pred_entities if not pred["matched"])
    false_negatives = sum(1 for gt in gt_entities if not gt["matched"])

    return true_positives, false_positives, false_negatives


def calculate_per_entity_metrics(
    ground_truth: list[GroundTruthAnnotation],
    predictions: list[PIIDetection],
    iou_threshold: float = 0.5,
) -> dict[str, dict[str, float]]:
    """
    Calculate metrics per entity type.

    Args:
        ground_truth: Ground truth annotations
        predictions: Predicted detections
        iou_threshold: IoU threshold

    Returns:
        Dict mapping entity type to metrics dict
    """
    # Group by entity type
    entity_types = set()
    for annotation in ground_truth:
        entity_types.update(annotation.entity_types)
    for pred in predictions:
        entity_types.add(pred.pii_type)

    per_entity_metrics = {}

    for entity_type in entity_types:
        # Filter ground truth and predictions for this type
        gt_filtered = []
        for annotation in ground_truth:
            filtered_annotation = GroundTruthAnnotation(
                text=annotation.text, source=annotation.source
            )
            for entity in annotation.entities:
                if entity.entity_type == entity_type:
                    filtered_annotation.add_entity(entity)
            if filtered_annotation.has_pii:
                gt_filtered.append(filtered_annotation)

        pred_filtered = [p for p in predictions if p.pii_type == entity_type]

        # Calculate metrics for this type
        tp, fp, fn = match_predictions_to_ground_truth(
            gt_filtered, pred_filtered, iou_threshold
        )

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1_score = (
            2 * (precision * recall) / (precision + recall)
            if (precision + recall) > 0
            else 0.0
        )

        per_entity_metrics[entity_type] = {
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score,
            "tp": tp,
            "fp": fp,
            "fn": fn,
        }

    return per_entity_metrics


def calculate_confusion_matrix(
    ground_truth: list[GroundTruthAnnotation],
    predictions: list[PIIDetection],
) -> dict[str, dict[str, int]]:
    """
    Calculate confusion matrix for entity types.

    Args:
        ground_truth: Ground truth annotations
        predictions: Predicted detections

    Returns:
        Confusion matrix as nested dict {true_type: {pred_type: count}}
    """
    # Build entity lists
    gt_entities = []
    for annotation in ground_truth:
        for entity in annotation.entities:
            gt_entities.append(
                {"start": entity.start, "end": entity.end, "type": entity.entity_type}
            )

    pred_entities = []
    for pred in predictions:
        pred_entities.append(
            {"start": pred.start_position, "end": pred.end_position, "type": pred.pii_type}
        )

    # Match by position overlap
    confusion = {}
    for gt in gt_entities:
        for pred in pred_entities:
            # Check overlap
            if gt["start"] < pred["end"] and pred["start"] < gt["end"]:
                true_type = gt["type"]
                pred_type = pred["type"]

                if true_type not in confusion:
                    confusion[true_type] = {}
                confusion[true_type][pred_type] = (
                    confusion[true_type].get(pred_type, 0) + 1
                )

    return confusion


def calculate_macro_average(per_entity_metrics: dict[str, dict[str, float]]) -> dict[str, float]:
    """
    Calculate macro-averaged metrics across entity types.

    Args:
        per_entity_metrics: Per-entity-type metrics

    Returns:
        Macro-averaged metrics
    """
    if not per_entity_metrics:
        return {"precision": 0.0, "recall": 0.0, "f1_score": 0.0}

    avg_precision = sum(m["precision"] for m in per_entity_metrics.values()) / len(
        per_entity_metrics
    )
    avg_recall = sum(m["recall"] for m in per_entity_metrics.values()) / len(
        per_entity_metrics
    )
    avg_f1 = sum(m["f1_score"] for m in per_entity_metrics.values()) / len(
        per_entity_metrics
    )

    return {"precision": avg_precision, "recall": avg_recall, "f1_score": avg_f1}
