# File and Module Plan
## Privacy-Aware Data Engineering Pipeline

**Version:** 1.0  
**Date:** October 25, 2026

---

## 1. Complete Directory Structure

```
Privacy-Aware-Data-Engineering-Pipeline/
│
├── .git/                          # Git version control
├── .gitignore                     # Git ignore rules
├── .env.example                   # Environment variable template
├── README.md                      # Main project documentation
├── requirements.txt               # Python dependencies
├── pyproject.toml                 # Project metadata and tool config
├── pytest.ini                     # Pytest configuration
├── app.py                         # Streamlit application entry point
│
├── .streamlit/                    # Streamlit configuration
│   ├── config.toml                # Streamlit theme and settings
│   └── secrets.toml.example       # Secrets template (not committed)
│
├── config/                        # Application configuration
│   ├── default.yaml               # Default settings
│   └── experiment.yaml            # Experiment-specific settings
│
├── src/                           # Source code
│   ├── __init__.py
│   │
│   ├── ingestion/                 # Data loading and validation
│   │   ├── __init__.py
│   │   ├── models.py              # IngestionResult dataclass
│   │   ├── loader.py              # CSV/JSON loading
│   │   └── validator.py           # File and DataFrame validation
│   │
│   ├── validation/                # Data quality and schema validation
│   │   ├── __init__.py
│   │   ├── models.py              # QualityProfile, QualityIssue dataclasses
│   │   ├── profiler.py            # Data quality profiling
│   │   ├── schema_validator.py    # Schema and constraint validation
│   │   └── cleaner.py             # Data cleaning operations
│   │
│   ├── detection/                 # PII detection
│   │   ├── __init__.py
│   │   ├── models.py              # PIIDetection dataclass
│   │   ├── base_detector.py       # PIIDetector abstract class
│   │   ├── rule_based_detector.py # Custom rule-based detectors
│   │   ├── nlp_detector.py        # Presidio + spaCy integration
│   │   └── detector_factory.py    # Factory for detector instantiation
│   │
│   ├── anonymization/             # Privacy transformations
│   │   ├── __init__.py
│   │   ├── models.py              # AnonymizationConfig, TransformationAudit
│   │   ├── strategies.py          # Transformation strategy classes
│   │   ├── transformer.py         # Apply transformations
│   │   └── config.py              # Configuration management
│   │
│   ├── pipeline/                  # Pipeline orchestration
│   │   ├── __init__.py
│   │   ├── models.py              # PipelineConfig, PipelineResult
│   │   └── pipeline.py            # DataPipeline class
│   │
│   ├── storage/                   # Data persistence
│   │   ├── __init__.py
│   │   ├── duckdb_manager.py      # DuckDB operations
│   │   └── temp_manager.py        # Temporary file management
│   │
│   ├── evaluation/                # Experimental evaluation
│   │   ├── __init__.py
│   │   ├── models.py              # GroundTruthAnnotation, Entity
│   │   ├── dataset_generator.py   # Synthetic dataset generation
│   │   ├── metrics.py             # Metrics calculation
│   │   └── experiment_runner.py   # Experiment execution
│   │
│   ├── ui/                        # User interface
│   │   ├── __init__.py
│   │   │
│   │   ├── pages/                 # Streamlit pages
│   │   │   ├── __init__.py
│   │   │   ├── home.py            # Home/overview page
│   │   │   ├── upload.py          # File upload page
│   │   │   ├── quality.py         # Data quality page
│   │   │   ├── detection.py       # PII detection page
│   │   │   ├── anonymization.py   # Anonymization page
│   │   │   ├── comparison.py      # Method comparison page
│   │   │   ├── experiments.py     # Experiment results page
│   │   │   └── settings.py        # Settings/history page (optional)
│   │   │
│   │   └── components/            # Reusable UI components
│   │       ├── __init__.py
│   │       ├── metrics.py         # Metric cards, KPI displays
│   │       ├── charts.py          # Plotly chart wrappers
│   │       ├── tables.py          # Formatted DataFrame displays
│   │       ├── feedback.py        # Success/error/warning messages
│   │       └── forms.py           # Configuration forms
│   │
│   └── utils/                     # Utility functions
│       ├── __init__.py
│       ├── config_loader.py       # Configuration loading
│       ├── logger.py              # Logging setup
│       └── helpers.py             # Miscellaneous utilities
│
├── tests/                         # Test suite
│   ├── __init__.py
│   ├── conftest.py                # Pytest fixtures and configuration
│   │
│   ├── unit/                      # Unit tests
│   │   ├── ingestion/
│   │   │   ├── test_loader.py
│   │   │   └── test_validator.py
│   │   ├── validation/
│   │   │   ├── test_profiler.py
│   │   │   ├── test_schema_validator.py
│   │   │   └── test_cleaner.py
│   │   ├── detection/
│   │   │   ├── test_email_detector.py
│   │   │   ├── test_phone_detector.py
│   │   │   ├── test_ssn_detector.py
│   │   │   ├── test_credit_card_detector.py
│   │   │   ├── test_ip_detector.py
│   │   │   ├── test_rule_based_detector.py
│   │   │   └── test_nlp_detector.py
│   │   ├── anonymization/
│   │   │   ├── test_strategies.py
│   │   │   └── test_transformer.py
│   │   ├── evaluation/
│   │   │   ├── test_dataset_generator.py
│   │   │   ├── test_metrics.py
│   │   │   └── test_experiment_runner.py
│   │   └── utils/
│   │       ├── test_config_loader.py
│   │       └── test_logger.py
│   │
│   ├── integration/               # Integration tests
│   │   ├── test_pipeline.py       # Full pipeline execution
│   │   └── test_storage.py        # Database operations
│   │
│   └── fixtures/                  # Test fixtures and sample data
│       ├── sample_data.py         # Generate test DataFrames
│       ├── mock_detections.py     # Mock PII detection results
│       └── ground_truth.json      # Small labeled dataset
│
├── data/                          # Data files (not committed except samples)
│   ├── .gitkeep
│   ├── samples/                   # Sample datasets (committed)
│   │   ├── customers.csv
│   │   ├── orders.json
│   │   ├── malformed.csv
│   │   └── README.md
│   ├── synthetic/                 # Generated synthetic datasets (not committed)
│   │   ├── .gitkeep
│   │   └── eval_dataset.json     # Evaluation dataset
│   └── pipeline.duckdb            # DuckDB database (not committed)
│
├── experiments/                   # Experiment scripts and configuration
│   ├── configs/                   # Experiment configurations
│   │   ├── experiment_config.yaml
│   │   └── dataset_config.yaml
│   ├── scripts/                   # Runnable experiment scripts
│   │   ├── generate_dataset.py    # Generate synthetic dataset CLI
│   │   ├── run_evaluation.py      # Run experiments CLI
│   │   └── generate_report.py     # Generate report CLI
│   └── results/                   # Experiment results (not committed)
│       ├── .gitkeep
│       ├── metrics.json           # Latest metrics
│       └── run_20261025.json      # Timestamped results
│
├── reports/                       # Reports and documentation outputs
│   ├── .gitkeep
│   ├── research_report.md         # Main research report
│   ├── figures/                   # Generated figures
│   │   ├── .gitkeep
│   │   ├── precision_recall_f1_comparison.png
│   │   ├── confusion_matrix_rule_based.png
│   │   ├── confusion_matrix_nlp.png
│   │   ├── processing_time_comparison.png
│   │   └── per_category_performance.png
│   └── results/                   # Exported results
│       ├── .gitkeep
│       ├── metrics.json
│       └── experiment_summary.csv
│
├── docs/                          # Project documentation
│   ├── 01-requirements-specification.md
│   ├── 02-architecture-specification.md
│   ├── 03-ui-ux-specification.md
│   ├── 04-data-research-specification.md
│   ├── 05-development-roadmap.md
│   ├── 06-risk-register.md
│   ├── 07-file-module-plan.md       # This document
│   ├── 08-project-summary.md        # High-level overview
│   ├── ARCHITECTURE.md              # Detailed architecture (Milestone 11)
│   ├── API.md                       # Module/function documentation (Milestone 11)
│   ├── CONTRIBUTING.md              # Development guidelines (optional)
│   ├── DEPLOYMENT.md                # Deployment instructions (Milestone 12)
│   └── screenshots/                 # UI screenshots
│       ├── home_page.png
│       ├── upload_page.png
│       ├── quality_page.png
│       ├── detection_page.png
│       ├── anonymization_page.png
│       ├── comparison_page.png
│       └── experiments_page.png
│
├── logs/                          # Application logs (not committed)
│   ├── .gitkeep
│   └── pipeline.log
│
├── Dockerfile                     # Docker container definition (optional, Milestone 12)
└── .dockerignore                  # Docker ignore rules (optional)
```

---

## 2. Module Responsibilities

### 2.1 Ingestion Module (`src/ingestion/`)

**Purpose**: Load and validate uploaded files

**Files:**
- `models.py`: Data structures for ingestion results
- `loader.py`: CSV and JSON file loading with encoding detection
- `validator.py`: File-level and DataFrame-level validation

**Key Functions:**
- `load_csv(file_path, encoding, delimiter) -> pd.DataFrame`
- `load_json(file_path) -> pd.DataFrame`
- `validate_file(file, max_size, allowed_types) -> bool`
- `validate_dataframe(df, max_rows, max_columns) -> IngestionResult`

**Dependencies:** pandas, chardet (for encoding detection)

**Tested by:** `tests/unit/ingestion/`

---

### 2.2 Validation Module (`src/validation/`)

**Purpose**: Profile data quality and perform cleaning

**Files:**
- `models.py`: QualityProfile, QualityIssue dataclasses
- `profiler.py`: Data quality analysis
- `schema_validator.py`: Schema and constraint checking
- `cleaner.py`: Data cleaning operations

**Key Functions:**
- `profile_dataframe(df) -> QualityProfile`
- `detect_missing_values(df) -> Dict[str, int]`
- `detect_duplicates(df, subset) -> int`
- `calculate_quality_score(profile) -> float`
- `remove_duplicates(df, subset, keep) -> pd.DataFrame`

**Dependencies:** pandas, pandera (optional for schema validation)

**Tested by:** `tests/unit/validation/`

---

### 2.3 Detection Module (`src/detection/`)

**Purpose**: Detect PII using rule-based and NLP methods

**Files:**
- `models.py`: PIIDetection dataclass
- `base_detector.py`: Abstract PIIDetector interface
- `rule_based_detector.py`: Email, phone, SSN, credit card, IP detectors
- `nlp_detector.py`: Presidio + spaCy integration
- `detector_factory.py`: Factory pattern for detector selection

**Key Classes:**
- `PIIDetector` (abstract): `detect(df) -> List[PIIDetection]`
- `RuleBasedPIIDetector`: Combines all rule-based detectors
- `PresidioDetector`: Wraps Microsoft Presidio

**Key Functions:**
- `detect_email(text) -> List[PIIDetection]`
- `detect_phone(text) -> List[PIIDetection]`
- `validate_credit_card_luhn(number) -> bool`
- `create_detector(method: str) -> PIIDetector`

**Dependencies:** regex, presidio-analyzer, presidio-anonymizer, spacy

**Tested by:** `tests/unit/detection/`

---

### 2.4 Anonymization Module (`src/anonymization/`)

**Purpose**: Apply privacy transformations to detected PII

**Files:**
- `models.py`: AnonymizationConfig, TransformationAudit dataclasses
- `strategies.py`: MaskStrategy, RedactStrategy, PseudonymizeStrategy, GeneralizeStrategy
- `transformer.py`: Apply transformations to DataFrame
- `config.py`: Configuration management

**Key Classes:**
- `AnonymizationStrategy` (abstract): `transform(value, pii_type) -> str`
- `MaskStrategy`, `RedactStrategy`, `PseudonymizeStrategy`, `GeneralizeStrategy`

**Key Functions:**
- `apply_transformations(df, detections, config) -> pd.DataFrame`
- `handle_overlaps(detections) -> List[PIIDetection]`
- `generate_audit(transformations) -> TransformationAudit`

**Dependencies:** hashlib, hmac (for pseudonymization)

**Tested by:** `tests/unit/anonymization/`

---

### 2.5 Pipeline Module (`src/pipeline/`)

**Purpose**: Orchestrate end-to-end data processing

**Files:**
- `models.py`: PipelineConfig, PipelineResult dataclasses
- `pipeline.py`: DataPipeline class

**Key Classes:**
- `DataPipeline`: Main orchestrator
  - `run(file_path, config) -> PipelineResult`

**Stages:**
1. Ingestion
2. Profiling
3. Validation
4. Detection
5. Transformation
6. Post-validation
7. Storage
8. Reporting

**Dependencies:** All other modules (ingestion, validation, detection, anonymization, storage)

**Tested by:** `tests/integration/test_pipeline.py`

---

### 2.6 Storage Module (`src/storage/`)

**Purpose**: Persist results and manage temporary files

**Files:**
- `duckdb_manager.py`: DuckDB database operations
- `temp_manager.py`: Temporary file lifecycle management

**Key Functions:**
- `initialize_database(db_path) -> Connection`
- `save_dataset(conn, metadata) -> str`
- `save_processing_run(conn, run_result) -> None`
- `query_history(conn, limit) -> List[Dict]`
- `create_temp_file(suffix) -> str`
- `cleanup_temp_files(session_id) -> None`

**Dependencies:** duckdb, tempfile

**Tested by:** `tests/integration/test_storage.py`

---

### 2.7 Evaluation Module (`src/evaluation/`)

**Purpose**: Generate datasets, run experiments, calculate metrics

**Files:**
- `models.py`: GroundTruthAnnotation, Entity dataclasses
- `dataset_generator.py`: Synthetic dataset generation with Faker
- `metrics.py`: Precision, recall, F1, confusion matrix
- `experiment_runner.py`: Experiment execution and timing

**Key Functions:**
- `generate_synthetic_dataset(config) -> List[GroundTruthAnnotation]`
- `match_predictions(ground_truth, predictions) -> Tuple[int, int, int]`  # TP, FP, FN
- `calculate_metrics(y_true, y_pred) -> Dict[str, float]`
- `run_experiment(dataset, method, config) -> Dict`

**Dependencies:** faker, scikit-learn

**Tested by:** `tests/unit/evaluation/`

---

### 2.8 UI Module (`src/ui/`)

**Purpose**: User interface and visualization

**Structure:**
- `pages/`: Streamlit pages (one file per page)
- `components/`: Reusable UI components

**Pages:**
- `home.py`: Landing page with overview
- `upload.py`: File upload and preview
- `quality.py`: Data quality dashboard
- `detection.py`: PII detection results
- `anonymization.py`: Transformation configuration
- `comparison.py`: Method comparison
- `experiments.py`: Experiment results
- `settings.py`: Configuration and history (optional)

**Components:**
- `metrics.py`: Metric cards for KPIs
- `charts.py`: Plotly chart wrappers (bar, line, pie, heatmap)
- `tables.py`: Formatted DataFrame displays
- `feedback.py`: Success/error/warning messages
- `forms.py`: Configuration forms

**Dependencies:** streamlit, plotly

**Tested by:** Manual UI testing (automated UI tests optional)

---

### 2.9 Utils Module (`src/utils/`)

**Purpose**: Shared utilities and helpers

**Files:**
- `config_loader.py`: Load and merge YAML configuration
- `logger.py`: Configure Python logging
- `helpers.py`: Miscellaneous utility functions

**Key Functions:**
- `load_config(config_path) -> Dict`
- `get_config_value(key, default) -> Any`
- `setup_logging(level, log_file) -> None`

**Dependencies:** pyyaml, logging

**Tested by:** `tests/unit/utils/`

---

## 3. Naming Conventions

### 3.1 Files and Directories

- **Directories**: lowercase with underscores (`src/detection/`)
- **Python files**: lowercase with underscores (`rule_based_detector.py`)
- **Test files**: prefix with `test_` (`test_loader.py`)
- **Configuration files**: lowercase with extension (`.yaml`, `.toml`, `.json`)
- **Documentation**: Title case with hyphens (`01-requirements-specification.md`)

### 3.2 Python Code

**Modules and Packages:**
- Lowercase with underscores
- Short, descriptive names
- Examples: `ingestion`, `detection`, `anonymization`

**Classes:**
- PascalCase
- Nouns or noun phrases
- Examples: `PIIDetector`, `DataPipeline`, `QualityProfile`

**Functions and Methods:**
- lowercase_with_underscores
- Verbs or verb phrases
- Examples: `load_csv()`, `detect_email()`, `calculate_metrics()`

**Variables:**
- lowercase_with_underscores
- Descriptive names (avoid abbreviations unless common)
- Examples: `quality_score`, `detection_results`, `df`

**Constants:**
- UPPERCASE_WITH_UNDERSCORES
- Defined at module level
- Examples: `MAX_FILE_SIZE_MB`, `DEFAULT_CONFIDENCE_THRESHOLD`

**Private Members:**
- Prefix with single underscore `_`
- Examples: `_validate_input()`, `_internal_cache`

**Dataclasses:**
- PascalCase
- Suffix with descriptive noun
- Examples: `IngestionResult`, `PIIDetection`, `AnonymizationConfig`

---

## 4. Import Organization

**Order (per PEP 8):**
1. Standard library imports
2. Related third-party imports
3. Local application imports

**Example:**
```python
# Standard library
import os
import logging
from typing import List, Dict, Optional
from dataclasses import dataclass

# Third-party
import pandas as pd
import numpy as np
from presidio_analyzer import AnalyzerEngine

# Local
from src.detection.models import PIIDetection
from src.detection.base_detector import PIIDetector
from src.utils.logger import get_logger
```

**Rules:**
- Group imports by category, separated by blank lines
- Use absolute imports (not relative) for clarity
- Avoid wildcard imports (`from module import *`)
- Import only what's needed

---

## 5. Configuration Strategy

### 5.1 Configuration Files

**config/default.yaml:**
- Default application settings
- Ingestion limits (max file size, max rows)
- Detection configuration (enabled categories, thresholds)
- Anonymization defaults (strategies per PII type)
- Storage settings (database path, retention policy)

**config/experiment.yaml:**
- Experiment-specific settings
- Dataset generation parameters (size, seed, positive ratio)
- Evaluation parameters (metrics, matching strategy)

**.env (not committed):**
- Environment-specific settings
- Secrets (pseudonymization keys, API keys if any)
- Paths (database path, log file path)

**.streamlit/config.toml:**
- Streamlit theme and UI settings
- Server configuration (port, headless mode)

### 5.2 Configuration Access

**Loading:**
```python
from src.utils.config_loader import load_config, get_config_value

config = load_config('config/default.yaml')
max_file_size = get_config_value('ingestion.max_file_size_mb', default=50)
```

**Precedence (highest to lowest):**
1. Environment variables (`.env`)
2. User-provided configuration (CLI arguments, UI inputs)
3. Configuration files (`config/default.yaml`)
4. Hardcoded defaults (in code)

---

## 6. Logging Strategy

### 6.1 Log Levels

- **DEBUG**: Detailed diagnostic information (not in production)
- **INFO**: General informational messages (stage start/end, counts)
- **WARNING**: Unexpected but handled situations (low quality score, missing values)
- **ERROR**: Error conditions that don't crash the app (file validation failure, detection error)
- **CRITICAL**: Severe errors that may cause app failure (database corruption, model not found)

### 6.2 Log Format

```
[2026-10-25 14:32:15] [INFO] [src.pipeline.pipeline] Starting pipeline execution: run_id=abc123
[2026-10-25 14:32:16] [INFO] [src.ingestion.loader] Loaded CSV file: 10523 rows, 12 columns
[2026-10-25 14:32:20] [WARNING] [src.validation.profiler] Data quality score: 85/100 (warnings present)
[2026-10-25 14:32:25] [INFO] [src.detection.rule_based_detector] Detected 1234 PII instances
[2026-10-25 14:32:30] [INFO] [src.pipeline.pipeline] Pipeline completed in 15.2 seconds
```

### 6.3 Logging Rules

**DO:**
- Log stage boundaries (start, end, duration)
- Log configuration changes
- Log errors with context
- Log aggregated metrics (counts, scores)
- Use appropriate log levels

**DO NOT:**
- Log raw PII values (emails, phone numbers, SSNs)
- Log sensitive configuration (secrets, keys)
- Log personal information
- Use print() statements (use logger instead)

**Example:**
```python
import logging
logger = logging.getLogger(__name__)

# Good
logger.info(f"Detected {len(detections)} PII instances of types: {set(d.pii_type for d in detections)}")
logger.warning(f"Column 'email' has {missing_count} missing values ({missing_pct:.1f}%)")

# Bad - DO NOT DO THIS
logger.info(f"Detected email: {email_value}")
logger.debug(f"Processing row: {row_data}")
```

---

## 7. Testing Strategy

### 7.1 Test Organization

**Unit Tests** (`tests/unit/`):
- One test file per source module
- Test individual functions and classes in isolation
- Use mocking for external dependencies
- Fast execution (<1 second per test)

**Integration Tests** (`tests/integration/`):
- Test interactions between modules
- Test full pipeline execution
- Test database operations
- Slower execution (seconds to minutes)

**Fixtures** (`tests/fixtures/`):
- Reusable test data and mock objects
- Ground truth datasets for evaluation tests
- Helper functions for test setup

### 7.2 Test Naming

**Test Files:**
- `test_<module_name>.py`
- Examples: `test_loader.py`, `test_rule_based_detector.py`

**Test Functions:**
- `test_<function_name>_<scenario>`
- Examples: `test_load_csv_valid_file()`, `test_detect_email_with_missing_domain()`

**Test Classes** (optional, for grouping):
- `Test<ClassName>`
- Example: `TestRuleBasedDetector`

### 7.3 Test Coverage Targets

- **Core modules** (ingestion, validation, detection, anonymization, pipeline): **>70%**
- **Evaluation module**: **>70%**
- **UI components**: Manual testing (automated optional)
- **Utils**: **>80%**

---

## 8. Documentation Strategy

### 8.1 Code Documentation

**Module Docstrings:**
```python
"""
Module: src.detection.rule_based_detector

Implements custom rule-based PII detectors using regex patterns
and validation logic. Includes detectors for email, phone, SSN,
credit card, and IP address.
"""
```

**Class Docstrings:**
```python
class EmailDetector(PIIDetector):
    """
    Detects email addresses using RFC 5322 subset pattern.
    
    Validates domain structure and rejects malformed emails
    like 'user@localhost' or 'user@.com'.
    """
```

**Function Docstrings:**
```python
def detect_email(text: str) -> List[PIIDetection]:
    """
    Detect email addresses in text using pattern matching.
    
    Args:
        text: Input text to scan for emails.
        
    Returns:
        List of PIIDetection objects with locations and confidence.
        
    Examples:
        >>> detect_email("Contact john.doe@example.com")
        [PIIDetection(start=8, end=31, pii_type='email', confidence=1.0)]
    """
```

### 8.2 Project Documentation

**README.md:**
- Project overview and motivation
- Features and capabilities
- Installation instructions (step-by-step for Windows)
- Usage guide (how to run application, tests, experiments)
- Sample datasets and results
- Limitations and disclaimers
- Troubleshooting
- Contributing guidelines (optional)
- License

**docs/ Documentation:**
- Planning and specifications (Milestones 0-1)
- Architecture deep-dive (Milestone 11)
- API/module reference (Milestone 11, optional)
- Deployment guide (Milestone 12, optional)

**Research Report:**
- Standalone Markdown or PDF
- Located in `reports/research_report.md`
- Structured as academic/technical report
- 10-15 pages with figures and references

---

## 9. Dependency Management

### 9.1 Requirements File

**requirements.txt:**
```txt
# Core dependencies
streamlit==1.28.0
pandas==2.1.0
numpy==1.25.0
plotly==5.17.0

# PII Detection
presidio-analyzer==2.2.33
presidio-anonymizer==2.2.33
spacy==3.6.1
# Note: spaCy model installed separately via: python -m spacy download en_core_web_lg

# Data Quality and Validation
pandera==0.17.0  # Optional for schema validation

# Storage
duckdb==0.9.0

# Evaluation and Metrics
faker==19.6.0
scikit-learn==1.3.0

# Testing
pytest==7.4.0
pytest-cov==4.1.0
pytest-mock==3.11.1

# Code Quality
ruff==0.0.292

# Utilities
pyyaml==6.0.1
python-dotenv==1.0.0
```

**Installation:**
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_lg
```

### 9.2 Dependency Rules

- **Pin exact versions** for reproducibility
- **Test all dependencies** for compatibility
- **Minimize dependencies** (avoid unnecessary libraries)
- **Document installation** for any special dependencies (spaCy model)
- **Review licenses** (ensure compatibility with project license)

---

## 10. Git Workflow

### 10.1 Branch Strategy

**Main Branches:**
- `main`: Production-ready code, tagged releases
- `develop`: Integration branch for completed features (optional)

**Feature Branches:**
- `milestone-N-description`: One branch per milestone
- Examples: `milestone-1-foundation`, `milestone-2-ingestion`

### 10.2 Commit Messages

**Format:**
```
<type>: <subject>

<body (optional)>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test additions or modifications
- `refactor`: Code refactoring
- `style`: Code style changes (formatting, no logic change)
- `chore`: Maintenance tasks (dependencies, config)

**Examples:**
```
feat: implement CSV and JSON file loading

Add load_csv() and load_json() functions with encoding detection
and error handling. Includes unit tests.

fix: handle duplicate column names in validation

Validator now rejects DataFrames with duplicate column names.

docs: update README with installation instructions

Add step-by-step setup guide for Windows users.
```

### 10.3 What to Commit

**DO commit:**
- Source code
- Tests
- Configuration files (without secrets)
- Sample datasets (small files)
- Documentation
- README, .gitignore, requirements.txt

**DO NOT commit:**
- `.env` files (use `.env.example` instead)
- DuckDB database files (`*.duckdb`, `*.db`)
- Generated datasets (except evaluation dataset for reproducibility)
- Logs (`*.log`)
- Temporary files
- Large files (>10 MB)
- IDE-specific files (unless needed for team)
- Secrets, API keys, tokens

---

## 11. Code Quality Checklist

**Before Committing:**
- [ ] Code linted with Ruff (no critical errors)
- [ ] All tests pass (`pytest tests/`)
- [ ] New code has unit tests (if applicable)
- [ ] Docstrings added for new functions/classes
- [ ] No commented-out code (remove or explain)
- [ ] No hardcoded secrets or paths
- [ ] No PII in logs or debug output
- [ ] Imports organized and minimal
- [ ] Type hints for public functions (optional but recommended)

**Before Milestone Completion:**
- [ ] All acceptance criteria met
- [ ] Integration tests pass
- [ ] README updated (if applicable)
- [ ] Configuration files updated (if settings changed)
- [ ] Milestone report prepared

---

## 12. Development Environment Setup

### 12.1 Initial Setup (Windows)

```powershell
# 1. Clone repository
git clone https://github.com/myth-unknown/Privacy-Aware-Data-Engineering-Pipeline.git
cd Privacy-Aware-Data-Engineering-Pipeline

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Download spaCy model
python -m spacy download en_core_web_lg

# 6. Run tests to verify setup
pytest tests/

# 7. Launch application
streamlit run app.py
```

### 12.2 IDE Configuration (VS Code Example)

**Recommended Extensions:**
- Python (Microsoft)
- Pylance (Microsoft)
- Ruff (Astral Software)
- GitLens
- Markdown All in One

**VS Code settings.json:**
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/Scripts/python.exe",
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests/"],
  "python.linting.enabled": false,  // Use Ruff instead
  "ruff.enable": true,
  "editor.formatOnSave": true,
  "python.analysis.typeCheckingMode": "basic"
}
```

---

**Document Status**: Final  
**Last Updated**: October 25, 2026  
**Ready for Implementation**: Yes
