"""
File loading utilities for CSV and JSON files.
"""

import logging
from pathlib import Path

import chardet
import pandas as pd

logger = logging.getLogger(__name__)


def detect_encoding(file_path: str | Path, sample_size: int = 10000) -> str:
    """
    Detect file encoding using chardet.

    Args:
        file_path: Path to the file
        sample_size: Number of bytes to sample for detection

    Returns:
        Detected encoding string (e.g., 'utf-8', 'ISO-8859-1')
    """
    file_path = Path(file_path)

    try:
        with open(file_path, "rb") as f:
            raw_data = f.read(sample_size)
            result = chardet.detect(raw_data)
            encoding = result.get("encoding", "utf-8")
            confidence = result.get("confidence", 0.0)

            logger.info(
                f"Detected encoding: {encoding} (confidence: {confidence:.2%})"
            )

            # Fallback to utf-8 if confidence is too low
            if confidence < 0.5:
                logger.warning(
                    f"Low confidence ({confidence:.2%}), falling back to utf-8"
                )
                return "utf-8"

            return encoding

    except Exception as e:
        logger.warning(f"Encoding detection failed: {e}. Defaulting to utf-8")
        return "utf-8"


def load_csv(
    file_path: str | Path,
    encoding: str | None = None,
    delimiter: str = ",",
    **kwargs,
) -> pd.DataFrame:
    """
    Load CSV file into pandas DataFrame with automatic encoding detection.

    Args:
        file_path: Path to CSV file
        encoding: File encoding (auto-detected if None)
        delimiter: CSV delimiter character
        **kwargs: Additional arguments passed to pandas.read_csv()

    Returns:
        Loaded DataFrame

    Raises:
        FileNotFoundError: If file doesn't exist
        pd.errors.ParserError: If CSV parsing fails
        Exception: For other loading errors
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Detect encoding if not provided
    if encoding is None:
        encoding = detect_encoding(file_path)

    logger.info(f"Loading CSV: {file_path.name} (encoding: {encoding})")

    try:
        # Attempt to load with detected/provided encoding
        df = pd.read_csv(file_path, encoding=encoding, delimiter=delimiter, **kwargs)
        logger.info(f"Successfully loaded {len(df)} rows, {len(df.columns)} columns")
        return df

    except UnicodeDecodeError:
        # Fallback to latin-1 which accepts all byte sequences
        logger.warning(f"Failed with {encoding}, trying 'latin-1'")
        df = pd.read_csv(file_path, encoding="latin-1", delimiter=delimiter, **kwargs)
        logger.info(f"Successfully loaded {len(df)} rows, {len(df.columns)} columns")
        return df

    except pd.errors.ParserError as e:
        logger.error(f"CSV parsing error: {e}")
        raise

    except Exception as e:
        logger.error(f"Failed to load CSV: {e}")
        raise


def load_json(
    file_path: str | Path, orient: str = "records", **kwargs
) -> pd.DataFrame:
    """
    Load JSON file into pandas DataFrame.

    Args:
        file_path: Path to JSON file
        orient: JSON orientation ('records', 'columns', 'index', etc.)
        **kwargs: Additional arguments passed to pandas.read_json()

    Returns:
        Loaded DataFrame

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If JSON structure is invalid for DataFrame conversion
        Exception: For other loading errors
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    logger.info(f"Loading JSON: {file_path.name} (orient: {orient})")

    try:
        df = pd.read_json(file_path, orient=orient, **kwargs)
        logger.info(f"Successfully loaded {len(df)} rows, {len(df.columns)} columns")
        return df

    except ValueError as e:
        logger.error(f"JSON structure error: {e}")
        raise

    except Exception as e:
        logger.error(f"Failed to load JSON: {e}")
        raise


def infer_delimiter(file_path: str | Path, sample_lines: int = 5) -> str:
    """
    Infer CSV delimiter by analyzing the first few lines.

    Args:
        file_path: Path to CSV file
        sample_lines: Number of lines to sample

    Returns:
        Inferred delimiter character
    """
    file_path = Path(file_path)
    encoding = detect_encoding(file_path)

    try:
        with open(file_path, encoding=encoding) as f:
            lines = [f.readline() for _ in range(sample_lines)]

        # Count occurrences of common delimiters
        delimiters = [",", ";", "\t", "|"]
        delimiter_counts = {d: sum(line.count(d) for line in lines) for d in delimiters}

        # Return delimiter with highest count
        inferred = max(delimiter_counts, key=delimiter_counts.get)
        logger.info(f"Inferred delimiter: {repr(inferred)}")
        return inferred

    except Exception as e:
        logger.warning(f"Delimiter inference failed: {e}. Defaulting to comma")
        return ","
