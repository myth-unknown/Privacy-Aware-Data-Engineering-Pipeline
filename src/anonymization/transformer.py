"""
Apply anonymization transformations to DataFrames.
"""

import logging
from datetime import datetime

import pandas as pd

from src.anonymization.models import (
    AnonymizationConfig,
    AnonymizationResult,
    TransformationAudit,
    TransformationRecord,
)
from src.anonymization.strategies import (
    GeneralizeStrategy,
    MaskStrategy,
    PseudonymizeStrategy,
    RedactStrategy,
)
from src.detection.models import PIIDetection

logger = logging.getLogger(__name__)


class DataTransformer:
    """Apply anonymization transformations to DataFrame."""

    def __init__(self):
        """Initialize transformer with strategies."""
        self.strategies = {
            "mask": MaskStrategy(),
            "redact": RedactStrategy(),
            "generalize": GeneralizeStrategy(),
        }

    def transform(
        self,
        df: pd.DataFrame,
        detections: list[PIIDetection],
        config: AnonymizationConfig,
    ) -> AnonymizationResult:
        """
        Apply anonymization to DataFrame based on detections.

        Args:
            df: Original DataFrame
            detections: List of PII detections
            config: Anonymization configuration

        Returns:
            AnonymizationResult with transformed data and audit
        """
        logger.info(f"Starting anonymization with strategy: {config.strategy}")

        # Initialize audit
        audit = TransformationAudit(start_time=datetime.now())

        # Create copy of DataFrame
        df_anonymized = df.copy()

        # Get strategy
        if config.strategy == "pseudonymize":
            strategy = PseudonymizeStrategy(seed=config.pseudonym_seed)
        else:
            strategy = self.strategies.get(config.strategy)

        if strategy is None:
            return AnonymizationResult(
                success=False,
                data=df,
                audit=audit,
                errors=[f"Unknown strategy: {config.strategy}"],
            )

        # Filter detections by PII type and columns
        filtered_detections = self._filter_detections(detections, config)

        # Group detections by (column, row) for batch processing
        detection_map = {}
        for detection in filtered_detections:
            key = (detection.column, detection.row_index)
            if key not in detection_map:
                detection_map[key] = []
            detection_map[key].append(detection)

        # Apply transformations
        errors = []
        warnings = []

        for (column, row_idx), cell_detections in detection_map.items():
            try:
                original_value = str(df.at[row_idx, column])
                transformed_value = original_value

                # Apply transformation to each detection in the cell
                # Sort by position (descending) to avoid index shifting
                sorted_detections = sorted(
                    cell_detections, key=lambda d: d.start_position, reverse=True
                )

                for detection in sorted_detections:
                    # Extract the detected PII substring
                    pii_substring = detection.value

                    # Transform the substring with strategy-specific kwargs
                    transform_kwargs = {
                        "pii_type": detection.pii_type,
                    }

                    if config.strategy == "mask":
                        transform_kwargs.update({
                            "mask_char": config.mask_char,
                            "mask_percentage": config.mask_percentage,
                            "preserve_format": config.preserve_format,
                        })
                    elif config.strategy == "generalize":
                        transform_kwargs.update({
                            "level": config.generalization_level,
                        })

                    transformed_substring = strategy.transform(
                        pii_substring,
                        **transform_kwargs,
                    )

                    # Replace in the full value
                    start = detection.start_position
                    end = detection.end_position
                    transformed_value = (
                        transformed_value[:start]
                        + transformed_substring
                        + transformed_value[end:]
                    )

                    # Record transformation
                    record = TransformationRecord(
                        column=column,
                        row_index=row_idx,
                        pii_type=detection.pii_type,
                        original_value=pii_substring,
                        transformed_value=transformed_substring,
                        strategy=config.strategy,
                    )
                    audit.add_record(record)

                # Update DataFrame with proper type handling
                try:
                    # For numeric columns, try to convert back to numeric
                    if pd.api.types.is_numeric_dtype(df[column]):
                        # Try to convert transformed value to numeric
                        try:
                            # Remove non-numeric characters if masking
                            if config.strategy == "mask":
                                # Keep only digits and decimal point
                                numeric_str = ''.join(c for c in transformed_value if c.isdigit() or c == '.')
                                if numeric_str:
                                    transformed_value = float(numeric_str) if '.' in numeric_str else int(numeric_str)
                                else:
                                    # If no digits remain, set to 0 or keep as string
                                    transformed_value = 0
                            else:
                                # For other strategies on numeric columns, convert column to string type
                                if column not in df_anonymized.select_dtypes(include=['object', 'string']).columns:
                                    df_anonymized[column] = df_anonymized[column].astype(str)
                        except (ValueError, TypeError):
                            # If conversion fails, convert entire column to string
                            df_anonymized[column] = df_anonymized[column].astype(str)

                    df_anonymized.at[row_idx, column] = transformed_value

                except Exception as type_error:
                    # Last resort: convert column to object type
                    logger.warning(f"Type conversion issue for {column}, converting to string: {type_error}")
                    df_anonymized[column] = df_anonymized[column].astype(str)
                    df_anonymized.at[row_idx, column] = transformed_value

            except Exception as e:
                error_msg = f"Failed to transform {column}[{row_idx}]: {e}"
                logger.error(error_msg, exc_info=True)
                errors.append(error_msg)

        audit.end_time = datetime.now()

        logger.info(
            f"Anonymization complete: {audit.total_transformations} transformations "
            f"in {audit.duration_seconds:.2f}s"
        )

        return AnonymizationResult(
            success=len(errors) == 0,
            data=df_anonymized,
            audit=audit,
            errors=errors,
            warnings=warnings,
        )

    def _filter_detections(
        self, detections: list[PIIDetection], config: AnonymizationConfig
    ) -> list[PIIDetection]:
        """Filter detections based on configuration."""
        filtered = []

        for detection in detections:
            # Filter by PII type (if "ALL", accept all types)
            if config.pii_type != "ALL" and detection.pii_type != config.pii_type:
                continue

            # Filter by columns
            if config.apply_to_columns and detection.column not in config.apply_to_columns:
                continue

            filtered.append(detection)

        return filtered


def anonymize_dataframe(
    df: pd.DataFrame,
    detections: list[PIIDetection],
    strategy: str = "mask",
    pii_type: str = "ALL",
    **kwargs,
) -> AnonymizationResult:
    """
    Convenience function to anonymize DataFrame.

    Args:
        df: Original DataFrame
        detections: PII detections
        strategy: Anonymization strategy
        pii_type: PII type to anonymize ("ALL" for all types)
        **kwargs: Strategy-specific parameters

    Returns:
        AnonymizationResult
    """
    config = AnonymizationConfig(
        strategy=strategy,
        pii_type=pii_type,
        **kwargs,
    )

    transformer = DataTransformer()
    return transformer.transform(df, detections, config)
