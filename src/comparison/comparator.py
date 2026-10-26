"""
PII detection method comparison logic.
"""

import logging
import time

import pandas as pd

from src.comparison.models import ComparisonResult, MethodMetrics
from src.detection import create_detector
from src.detection.models import PIIDetection

logger = logging.getLogger(__name__)


def compare_detection_methods(
    df: pd.DataFrame,
    methods: list[str] | None = None,
    confidence_threshold: float = 0.5,
    columns: list[str] | None = None,
) -> ComparisonResult:
    """
    Compare multiple PII detection methods on the same dataset.

    Args:
        df: DataFrame to analyze
        methods: List of methods to compare (default: ["rule_based", "nlp"])
        confidence_threshold: Minimum confidence threshold
        columns: Specific columns to scan (None = all)

    Returns:
        ComparisonResult with metrics for each method
    """
    if methods is None:
        methods = ["rule_based", "nlp"]

    logger.info(f"Comparing detection methods: {methods}")

    result = ComparisonResult(
        dataset_name="uploaded_data",
        total_rows=len(df),
        total_columns=len(df.columns),
    )

    # Run each method and collect metrics
    all_detections: dict[str, list[PIIDetection]] = {}

    for method in methods:
        try:
            logger.info(f"Running {method} detection...")
            metrics = _run_method_and_measure(
                df, method, confidence_threshold, columns
            )
            result.add_method_metrics(metrics)
            all_detections[method] = _get_detections_for_method(
                df, method, confidence_threshold, columns
            )
            logger.info(
                f"{method}: {metrics.total_detections} detections in {metrics.execution_time_seconds:.2f}s"
            )
        except Exception as e:
            logger.error(f"Failed to run {method}: {e}", exc_info=True)
            # Add empty metrics for failed method
            result.add_method_metrics(
                MethodMetrics(
                    method_name=method,
                    total_detections=0,
                    execution_time_seconds=0.0,
                )
            )

    # Analyze agreements and disagreements
    if len(all_detections) >= 2:
        _analyze_agreements(result, all_detections)

    # Generate recommendation
    _generate_recommendation(result)

    logger.info(f"Comparison complete: {len(result.method_metrics)} methods")
    return result


def _run_method_and_measure(
    df: pd.DataFrame,
    method: str,
    confidence_threshold: float,
    columns: list[str] | None,
) -> MethodMetrics:
    """Run detection method and measure performance."""
    start_time = time.time()

    # Create detector and run
    detector = create_detector(method)
    detections = detector.detect(df)

    # Filter by confidence and columns
    if columns:
        detections = [d for d in detections if d.column in columns]
    detections = [d for d in detections if d.confidence >= confidence_threshold]

    execution_time = time.time() - start_time

    # Calculate metrics
    metrics = MethodMetrics(
        method_name=method,
        total_detections=len(detections),
        execution_time_seconds=execution_time,
        columns_scanned=len(columns) if columns else len(df.columns),
        rows_scanned=len(df),
    )

    # Throughput
    if execution_time > 0:
        metrics.throughput_rows_per_second = len(df) / execution_time

    # Detections by type
    for detection in detections:
        pii_type = detection.pii_type
        metrics.detections_by_type[pii_type] = (
            metrics.detections_by_type.get(pii_type, 0) + 1
        )

    # Confidence distribution
    for detection in detections:
        if detection.confidence >= 0.8:
            metrics.high_confidence_count += 1
        elif detection.confidence >= 0.5:
            metrics.medium_confidence_count += 1
        else:
            metrics.low_confidence_count += 1

    if detections:
        metrics.avg_confidence = sum(d.confidence for d in detections) / len(
            detections
        )

    # PII coverage
    unique_cells = {(d.row_index, d.column) for d in detections}
    metrics.cells_with_pii = len(unique_cells)
    total_cells = len(df) * (len(columns) if columns else len(df.columns))
    if total_cells > 0:
        metrics.pii_percentage = (metrics.cells_with_pii / total_cells) * 100

    return metrics


def _get_detections_for_method(
    df: pd.DataFrame,
    method: str,
    confidence_threshold: float,
    columns: list[str] | None,
) -> list[PIIDetection]:
    """Get detections for a specific method."""
    detector = create_detector(method)
    detections = detector.detect(df)

    # Filter
    if columns:
        detections = [d for d in detections if d.column in columns]
    detections = [d for d in detections if d.confidence >= confidence_threshold]

    return detections


def _analyze_agreements(
    result: ComparisonResult, all_detections: dict[str, list[PIIDetection]]
) -> None:
    """Analyze agreements and disagreements between methods."""
    # Create sets of detection signatures (row, column, type)
    detection_sets: dict[str, set[tuple[int, str, str]]] = {}
    for method, detections in all_detections.items():
        detection_sets[method] = {
            (d.row_index, d.column, d.pii_type) for d in detections
        }

    # Find agreements (intersection of all)
    if len(detection_sets) >= 2:
        methods_list = list(detection_sets.keys())
        agreement_set = detection_sets[methods_list[0]].copy()
        for method in methods_list[1:]:
            agreement_set &= detection_sets[method]
        result.agreement_count = len(agreement_set)

        # Find unique to each method
        if "rule_based" in detection_sets:
            unique_to_rule = detection_sets["rule_based"].copy()
            for method in methods_list:
                if method != "rule_based":
                    unique_to_rule -= detection_sets[method]
            result.unique_to_rule_based = len(unique_to_rule)

        if "nlp" in detection_sets:
            unique_to_nlp = detection_sets["nlp"].copy()
            for method in methods_list:
                if method != "nlp":
                    unique_to_nlp -= detection_sets[method]
            result.unique_to_nlp = len(unique_to_nlp)

        if "hybrid" in detection_sets:
            unique_to_hybrid = detection_sets["hybrid"].copy()
            for method in methods_list:
                if method != "hybrid":
                    unique_to_hybrid -= detection_sets[method]
            result.unique_to_hybrid = len(unique_to_hybrid)

        # Total disagreements
        all_detections_set = set()
        for det_set in detection_sets.values():
            all_detections_set |= det_set
        result.disagreement_count = len(all_detections_set) - result.agreement_count


def _generate_recommendation(result: ComparisonResult) -> None:
    """Generate method recommendation based on metrics."""
    if not result.method_metrics:
        result.recommended_method = "none"
        result.recommendation_reason = "No methods available"
        return

    # Score each method
    scores: dict[str, float] = {}

    for method_name, metrics in result.method_metrics.items():
        score = 0.0

        # Detection count (40% weight)
        if metrics.total_detections > 0:
            score += 40.0

        # Speed (20% weight)
        if metrics.execution_time_seconds < 5.0:
            score += 20.0
        elif metrics.execution_time_seconds < 10.0:
            score += 10.0

        # Confidence (20% weight)
        if metrics.avg_confidence >= 0.8:
            score += 20.0
        elif metrics.avg_confidence >= 0.5:
            score += 10.0

        # Coverage (20% weight)
        if metrics.pii_percentage >= 5.0:
            score += 20.0
        elif metrics.pii_percentage >= 1.0:
            score += 10.0

        scores[method_name] = score

    # Get best method
    best_method = max(scores.items(), key=lambda x: x[1])[0]
    best_score = scores[best_method]

    result.recommended_method = best_method
    result.recommendation_reason = _get_recommendation_reason(
        best_method, result.method_metrics[best_method], best_score
    )


def _get_recommendation_reason(
    method_name: str, metrics: MethodMetrics, score: float
) -> str:
    """Generate human-readable recommendation reason."""
    reasons = []

    if metrics.total_detections > 0:
        reasons.append(f"found {metrics.total_detections} PII instances")

    if metrics.execution_time_seconds < 5.0:
        reasons.append("fast execution")

    if metrics.avg_confidence >= 0.8:
        reasons.append(f"high confidence (avg {metrics.avg_confidence:.2f})")

    if metrics.pii_percentage >= 5.0:
        reasons.append(f"good coverage ({metrics.pii_percentage:.1f}%)")

    if not reasons:
        return f"{method_name} is the only available method"

    return f"{method_name}: {', '.join(reasons)}"
