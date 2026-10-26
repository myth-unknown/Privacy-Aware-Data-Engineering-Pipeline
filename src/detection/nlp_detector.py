"""
NLP-based PII detector using Microsoft Presidio and spaCy.
"""

import logging

import pandas as pd

from src.detection.base_detector import PIIDetector
from src.detection.models import PIIDetection

logger = logging.getLogger(__name__)

# Import Presidio (optional - will gracefully degrade if not available)
try:
    from presidio_analyzer import AnalyzerEngine
    from presidio_analyzer.nlp_engine import NlpEngineProvider

    PRESIDIO_AVAILABLE = True
except ImportError:
    logger.warning("Presidio not available. NLP detection will be disabled.")
    PRESIDIO_AVAILABLE = False


class PresidioDetector(PIIDetector):
    """PII detector using Microsoft Presidio with spaCy NLP."""

    def __init__(
        self,
        confidence_threshold: float = 0.5,
        language: str = "en",
        entities: list[str] | None = None,
    ):
        """
        Initialize Presidio detector.

        Args:
            confidence_threshold: Minimum confidence to report
            language: Language code (default: "en")
            entities: Entity types to detect (None = all)
        """
        super().__init__(confidence_threshold)

        if not PRESIDIO_AVAILABLE:
            raise RuntimeError(
                "Presidio is not installed. Install with: pip install presidio-analyzer presidio-anonymizer"
            )

        self.language = language
        self.entities = entities

        # Initialize Presidio analyzer
        try:
            # Configure NLP engine to use spaCy
            nlp_configuration = {
                "nlp_engine_name": "spacy",
                "models": [{"lang_code": language, "model_name": "en_core_web_lg"}],
            }

            nlp_engine_provider = NlpEngineProvider(nlp_configuration=nlp_configuration)
            self.analyzer = AnalyzerEngine(nlp_engine=nlp_engine_provider.create_engine())

            logger.info("Presidio analyzer initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize Presidio: {e}")
            raise RuntimeError(f"Presidio initialization failed: {e}") from e

    def get_supported_types(self) -> list[str]:
        """Get supported entity types from Presidio."""
        if self.entities:
            return self.entities
        return [
            "PERSON",
            "EMAIL_ADDRESS",
            "PHONE_NUMBER",
            "CREDIT_CARD",
            "IBAN_CODE",
            "IP_ADDRESS",
            "LOCATION",
            "DATE_TIME",
            "NRP",  # National Registry of Persons
            "US_SSN",
            "US_DRIVER_LICENSE",
            "US_PASSPORT",
            "MEDICAL_LICENSE",
            "URL",
        ]

    def detect(self, df: pd.DataFrame, columns: list[str] | None = None) -> list[PIIDetection]:
        """
        Detect PII using Presidio NLP analysis.

        Args:
            df: DataFrame to scan
            columns: Optional column list

        Returns:
            List of PIIDetection objects
        """
        detections = []
        target_columns = self._get_target_columns(df, columns)

        logger.info(
            f"Scanning {len(target_columns)} columns with Presidio NLP "
            f"(language={self.language})"
        )

        for col in target_columns:
            for row_idx, value in df[col].items():
                if pd.isna(value):
                    continue

                text = str(value)
                col_detections = self._analyze_text(text, col, row_idx)
                detections.extend(col_detections)

        # Filter by confidence
        detections = self._filter_by_confidence(detections)

        logger.info(f"Found {len(detections)} PII instances with Presidio")
        return detections

    def _analyze_text(self, text: str, column: str, row_index: int) -> list[PIIDetection]:
        """Analyze text using Presidio."""
        detections = []

        try:
            # Analyze text
            results = self.analyzer.analyze(
                text=text,
                language=self.language,
                entities=self.entities,
                score_threshold=self.confidence_threshold,
            )

            # Convert Presidio results to PIIDetection objects
            for result in results:
                detection = PIIDetection(
                    column=column,
                    row_index=row_index,
                    pii_type=result.entity_type,
                    value=text[result.start : result.end],
                    start_position=result.start,
                    end_position=result.end,
                    confidence=result.score,
                    detection_method="nlp",
                    metadata={
                        "recognition_metadata": result.recognition_metadata,
                    },
                )
                detections.append(detection)

        except Exception as e:
            logger.error(f"Presidio analysis failed for column {column}, row {row_index}: {e}")

        return detections
