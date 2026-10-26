"""
Data ingestion module for file loading and validation.
"""

from src.ingestion.loader import detect_encoding, load_csv, load_json
from src.ingestion.models import IngestionResult, ValidationIssue
from src.ingestion.validator import validate_dataframe, validate_file

__all__ = [
    "IngestionResult",
    "ValidationIssue",
    "load_csv",
    "load_json",
    "detect_encoding",
    "validate_file",
    "validate_dataframe",
]
