# Development Roadmap
## Privacy-Aware Data Engineering Pipeline

**Version:** 1.0  
**Date:** October 25, 2026

---

## Overview

This roadmap breaks down the project into 12 manageable milestones, each with clear objectives, tasks, deliverables, and acceptance criteria. Milestones should be completed sequentially to maintain dependency integrity.

**Total Estimated Duration**: 8-12 weeks (part-time development)

---

## Milestone 0: Requirements and Project Specification

**Duration**: 1 week  
**Status**: ✅ In Progress (this document)

### Objectives
- Define complete project scope and requirements
- Establish architecture and design specifications
- Identify risks and mitigation strategies
- Create detailed implementation plan

### Tasks
- [x] Create requirements specification document
- [x] Create architecture specification document
- [x] Create UI/UX specification document
- [x] Create data and research specification document
- [x] Create development roadmap
- [ ] Create risk register
- [ ] Create file structure and module plan
- [ ] Review and approval of all specifications

### Deliverables
- `docs/01-requirements-specification.md`
- `docs/02-architecture-specification.md`
- `docs/03-ui-ux-specification.md`
- `docs/04-data-research-specification.md`
- `docs/05-development-roadmap.md`
- `docs/06-risk-register.md`
- `docs/07-file-module-plan.md`

### Acceptance Criteria
- [ ] All specifications complete and reviewed
- [ ] Architecture validated against requirements
- [ ] Risks identified with mitigation plans
- [ ] Roadmap approved and ready for implementation
- [ ] No major unresolved questions or conflicts

### Dependencies
- None

---

## Milestone 1: Project Foundation

**Duration**: 1 week  
**Status**: ⏳ Not Started

### Objectives
- Set up Python development environment
- Create project directory structure
- Configure dependencies and tooling
- Establish code quality checks
- Create basic application entry point

### Tasks

#### 1.1 Environment Setup
- [ ] Create Python 3.11 virtual environment
- [ ] Create `requirements.txt` with initial dependencies
- [ ] Create `.env.example` file for configuration
- [ ] Update `.gitignore` for Python artifacts
- [ ] Install and configure Ruff for linting

#### 1.2 Project Structure
- [ ] Create complete directory tree (as per specification)
- [ ] Add `.gitkeep` files to empty directories
- [ ] Create `README.md` with project overview
- [ ] Create `pyproject.toml` for project metadata

#### 1.3 Configuration
- [ ] Create `config/default.yaml` with default settings
- [ ] Create configuration loader (`src/utils/config_loader.py`)
- [ ] Create logging setup (`src/utils/logger.py`)
- [ ] Test configuration loading and validation

#### 1.4 Basic Application
- [ ] Create `app.py` as Streamlit entry point
- [ ] Create simple home page (`src/ui/pages/home.py`)
- [ ] Test Streamlit application launches
- [ ] Verify configuration and logging work

#### 1.5 Testing Foundation
- [ ] Create `pytest.ini` configuration
- [ ] Create test directory structure
- [ ] Write first dummy test to verify pytest works
- [ ] Configure test coverage reporting

### Files to Create
```
├── app.py
├── requirements.txt
├── pyproject.toml
├── pytest.ini
├── .env.example
├── README.md
├── config/
│   └── default.yaml
├── src/
│   ├── __init__.py
│   ├── ui/
│   │   ├── __init__.py
│   │   └── pages/
│   │       ├── __init__.py
│   │       └── home.py
│   └── utils/
│       ├── __init__.py
│       ├── config_loader.py
│       └── logger.py
├── tests/
│   ├── __init__.py
│   └── test_basic.py
└── [Additional directory structure]
```

### Verification Commands
```bash
# Activate environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run linting
ruff check src/

# Run tests
pytest tests/

# Launch application
streamlit run app.py
```

### Acceptance Criteria
- [ ] Virtual environment created and activated
- [ ] All dependencies install successfully
- [ ] Streamlit application launches without errors
- [ ] Home page displays basic content
- [ ] Configuration loads successfully
- [ ] Logging writes to console and file
- [ ] Linting runs without critical errors
- [ ] Pytest runs and passes basic test
- [ ] README contains setup instructions
- [ ] Fresh installation tested on clean environment

### Dependencies
- Milestone 0 complete and approved

---

## Milestone 2: Data Ingestion

**Duration**: 1 week  
**Status**: ⏳ Not Started

### Objectives
- Implement CSV and JSON file loading
- Add file validation and error handling
- Create data preview functionality
- Build upload page UI

### Tasks

#### 2.1 Ingestion Module
- [ ] Create `src/ingestion/loader.py`
  - [ ] `load_csv()` function with encoding detection
  - [ ] `load_json()` function with structure handling
  - [ ] `infer_types()` for column type inference
- [ ] Create `src/ingestion/validator.py`
  - [ ] `validate_file()` for file-level checks
  - [ ] `validate_dataframe()` for DataFrame checks
  - [ ] `check_column_names()` for column validation
- [ ] Create `IngestionResult` dataclass in `src/ingestion/models.py`

#### 2.2 Upload Page UI
- [ ] Create `src/ui/pages/upload.py`
- [ ] Implement file uploader widget
- [ ] Display file information (size, rows, columns)
- [ ] Implement data preview table (first 100 rows)
- [ ] Display column information table
- [ ] Add Continue and Clear buttons
- [ ] Handle upload states (empty, uploading, uploaded, error)

#### 2.3 Error Handling
- [ ] Implement validation error messages
- [ ] Handle file size exceeded errors
- [ ] Handle malformed CSV/JSON errors
- [ ] Handle encoding errors with suggestions
- [ ] Test with various invalid inputs

#### 2.4 Testing
- [ ] Unit tests for `loader.py` functions
- [ ] Unit tests for `validator.py` functions
- [ ] Test with valid CSV and JSON files
- [ ] Test with invalid files (malformed, too large, wrong type)
- [ ] Test with edge cases (empty files, single row, Unicode)

### Sample Data Preparation
- [ ] Create `data/samples/` directory
- [ ] Add sample CSV file (100-1000 rows with PII)
- [ ] Add sample JSON file
- [ ] Add malformed files for testing
- [ ] Document sample data structure

### Files to Create
```
src/ingestion/
├── __init__.py
├── models.py
├── loader.py
└── validator.py

src/ui/pages/
└── upload.py

tests/unit/ingestion/
├── test_loader.py
└── test_validator.py

data/samples/
├── customers.csv
├── orders.json
├── malformed.csv
└── README.md
```

### Verification Commands
```bash
# Run unit tests
pytest tests/unit/ingestion/ -v

# Launch app and test upload
streamlit run app.py
# Navigate to Upload page
# Upload sample CSV and JSON files
# Verify preview and validation
```

### Acceptance Criteria
- [ ] CSV files load successfully with correct encoding
- [ ] JSON files load successfully (array and object formats)
- [ ] File validation catches invalid files
- [ ] Data preview displays correctly
- [ ] Column information table accurate
- [ ] Error messages clear and actionable
- [ ] Unit tests pass with >80% coverage
- [ ] Sample data files work correctly
- [ ] Upload workflow smooth and intuitive

### Dependencies
- Milestone 1 complete

---

## Milestone 3: Data Quality Profiling

**Duration**: 1 week  
**Status**: ⏳ Not Started

### Objectives
- Implement data quality profiling
- Detect missing values, duplicates, type issues
- Calculate quality score
- Build data quality dashboard page

### Tasks

#### 3.1 Validation Module
- [ ] Create `src/validation/profiler.py`
  - [ ] `profile_dataframe()` function
  - [ ] `detect_missing_values()`
  - [ ] `detect_duplicates()`
  - [ ] `detect_type_issues()`
  - [ ] `calculate_quality_score()`
- [ ] Create `QualityProfile` and `QualityIssue` dataclasses
- [ ] Create `src/validation/schema_validator.py` (basic, Pandera integration optional)
- [ ] Create `src/validation/cleaner.py`
  - [ ] `remove_duplicates()`
  - [ ] `fill_missing()`
  - [ ] `drop_columns()`
  - [ ] `convert_types()`

#### 3.2 UI Components
- [ ] Create `src/ui/components/metrics.py` for metric cards
- [ ] Create `src/ui/components/charts.py` for chart wrappers
- [ ] Create `src/ui/components/tables.py` for formatted tables

#### 3.3 Data Quality Page
- [ ] Create `src/ui/pages/quality.py`
- [ ] Display quality score and key metrics (metric cards)
- [ ] Show issues by severity (stacked bar chart)
- [ ] Display issues detail table (sortable, filterable)
- [ ] Show missing values by column (bar chart)
- [ ] Implement data cleaning section (optional actions)
- [ ] Add navigation buttons (Continue, Back, Download Report)

#### 3.4 Testing
- [ ] Unit tests for profiler functions
- [ ] Test with datasets containing known issues
- [ ] Test quality score calculation
- [ ] Test cleaning operations (remove duplicates, fill missing)
- [ ] Verify before/after comparisons

### Files to Create
```
src/validation/
├── __init__.py
├── models.py
├── profiler.py
├── schema_validator.py
└── cleaner.py

src/ui/components/
├── __init__.py
├── metrics.py
├── charts.py
└── tables.py

src/ui/pages/
└── quality.py

tests/unit/validation/
├── test_profiler.py
├── test_schema_validator.py
└── test_cleaner.py
```

### Verification Commands
```bash
# Run tests
pytest tests/unit/validation/ -v

# Test in UI
streamlit run app.py
# Upload sample data with known issues
# Navigate to Data Quality page
# Verify all metrics and charts display
# Test cleaning operations
```

### Acceptance Criteria
- [ ] Profiling detects all specified issue types
- [ ] Quality score calculation accurate
- [ ] Issues categorized by severity correctly
- [ ] Charts and tables display correctly
- [ ] Cleaning operations work without errors
- [ ] Before/after comparisons accurate
- [ ] Unit tests pass with >70% coverage
- [ ] UI responsive and polished
- [ ] Download quality report works (JSON)

### Dependencies
- Milestone 2 complete

---

## Milestone 4: Rule-Based PII Detection

**Duration**: 1-2 weeks  
**Status**: ⏳ Not Started

### Objectives
- Implement custom rule-based PII detectors
- Support email, phone, SSN, credit card, IP address detection
- Create configurable detector factory
- Achieve high precision with validation logic

### Tasks

#### 4.1 Detection Module Foundation
- [ ] Create `src/detection/base_detector.py` with `PIIDetector` abstract class
- [ ] Create `PIIDetection` dataclass in `src/detection/models.py`
- [ ] Create `src/detection/detector_factory.py`

#### 4.2 Rule-Based Detectors
- [ ] Create `src/detection/rule_based_detector.py` with classes:
  - [ ] `EmailDetector`: Pattern + domain validation
  - [ ] `PhoneDetector`: North American + international patterns
  - [ ] `SSNDetector`: US SSN format + validation
  - [ ] `CreditCardDetector`: Pattern + Luhn algorithm
  - [ ] `IPAddressDetector`: IPv4 and IPv6
- [ ] Implement confidence scoring (1.0 for valid matches)
- [ ] Support configuration (enable/disable categories)

#### 4.3 Detector Orchestration
- [ ] Create `RuleBasedPIIDetector` class that combines all detectors
- [ ] Implement batch processing for DataFrames
- [ ] Handle overlapping detections (choose highest confidence)
- [ ] Generate structured detection results

#### 4.4 Testing
- [ ] Unit tests for each detector with positive/negative examples
- [ ] Test Luhn algorithm for credit cards
- [ ] Test SSN validation logic
- [ ] Test phone number format variations
- [ ] Test IPv4 and IPv6 detection
- [ ] Test with edge cases (malformed, ambiguous text)
- [ ] Integration test with sample dataset

### Files to Create
```
src/detection/
├── __init__.py
├── models.py
├── base_detector.py
├── rule_based_detector.py
└── detector_factory.py

tests/unit/detection/
├── test_email_detector.py
├── test_phone_detector.py
├── test_ssn_detector.py
├── test_credit_card_detector.py
├── test_ip_detector.py
└── test_rule_based_detector.py

tests/fixtures/
└── detection_samples.py
```

### Verification Commands
```bash
# Run unit tests
pytest tests/unit/detection/ -v

# Test specific detector
pytest tests/unit/detection/test_email_detector.py -v

# Test with sample data
python -m src.detection.rule_based_detector --input data/samples/customers.csv
```

### Acceptance Criteria
- [ ] All specified PII categories detected correctly
- [ ] Validation logic reduces false positives
- [ ] Confidence scores assigned appropriately
- [ ] Detector configurable (enable/disable categories)
- [ ] Overlapping detections handled correctly
- [ ] Unit tests pass with >80% coverage for detectors
- [ ] Performance acceptable (>100 records/second)
- [ ] Edge cases handled gracefully
- [ ] Detection results structured correctly

### Dependencies
- Milestone 3 complete

---

## Milestone 5: NLP-Assisted PII Detection

**Duration**: 1-2 weeks  
**Status**: ⏳ Not Started

### Objectives
- Integrate Microsoft Presidio for PII analysis
- Configure spaCy NER model
- Separate NLP-based detections from pattern-based
- Handle model loading and errors gracefully

### Tasks

#### 5.1 Presidio Integration
- [ ] Install Presidio and spaCy dependencies
- [ ] Download spaCy model (`en_core_web_lg`)
- [ ] Create `src/detection/nlp_detector.py`
  - [ ] `PresidioDetector` class wrapping Presidio Analyzer
  - [ ] Configure recognizers (enable only NER-based ones)
  - [ ] Filter out pattern-based recognizers for fair comparison
  - [ ] Map Presidio entity types to PII categories

#### 5.2 NLP Configuration
- [ ] Configure spaCy model loading with error handling
- [ ] Set confidence thresholds (default 0.5)
- [ ] Configure entity types to recognize (PERSON, ORG, GPE if relevant)
- [ ] Implement batch processing for performance
- [ ] Add warmup logic (load model once, reuse)

#### 5.3 Error Handling
- [ ] Handle model not found errors with clear messages
- [ ] Handle model loading failures
- [ ] Implement timeout for large texts
- [ ] Fallback to rule-based with warning if NLP fails
- [ ] Log NLP errors without exposing PII

#### 5.4 Detector Factory Update
- [ ] Update `detector_factory.py` to support 'nlp-assisted' method
- [ ] Add method selection in configuration

#### 5.5 Testing
- [ ] Unit tests for Presidio integration
- [ ] Test NER entity detection (PERSON, ORG)
- [ ] Test with texts containing named entities
- [ ] Verify pattern-based recognizers excluded
- [ ] Test error handling (model not found, loading failure)
- [ ] Performance test (measure time for 1000 records)

### Files to Create
```
src/detection/
└── nlp_detector.py

tests/unit/detection/
└── test_nlp_detector.py

config/
└── nlp_config.yaml  # Optional
```

### Verification Commands
```bash
# Download spaCy model
python -m spacy download en_core_web_lg

# Verify model installed
python -m spacy info en_core_web_lg

# Run tests
pytest tests/unit/detection/test_nlp_detector.py -v

# Test NLP detection
python -m src.detection.nlp_detector --input data/samples/text_with_names.txt
```

### Acceptance Criteria
- [ ] spaCy model downloads and loads successfully
- [ ] Presidio integration working
- [ ] NER-based entities detected (PERSON, ORG)
- [ ] Pattern-based Presidio recognizers excluded from comparison
- [ ] Confidence thresholds configurable
- [ ] Error handling prevents crashes
- [ ] Model loading time acceptable (<10 seconds)
- [ ] Detection performance reasonable (>10 records/second)
- [ ] Unit tests pass
- [ ] Model compatibility verified on Windows

### Dependencies
- Milestone 4 complete

### Risks
- **High**: spaCy model compatibility issues on Windows
- **Medium**: Presidio version compatibility with Python 3.11
- **Mitigation**: Test early, document workarounds

---

## Milestone 6: Anonymization Module

**Duration**: 1 week  
**Status**: ⏳ Not Started

### Objectives
- Implement transformation strategies (mask, redact, pseudonymize, generalize)
- Apply transformations to detected PII
- Handle overlapping detections and edge cases
- Generate transformation audit logs

### Tasks

#### 6.1 Anonymization Strategies
- [ ] Create `src/anonymization/strategies.py` with classes:
  - [ ] `MaskStrategy`: Replace with mask character
  - [ ] `RedactStrategy`: Remove or replace with placeholder
  - [ ] `PseudonymizeStrategy`: HMAC-based consistent hashing
  - [ ] `GeneralizeStrategy`: Replace with category label
- [ ] Each strategy implements `transform(value, pii_type) -> str`

#### 6.2 Transformer
- [ ] Create `src/anonymization/transformer.py`
  - [ ] `apply_transformations(df, detections, config)` function
  - [ ] Handle overlapping detections (choose highest confidence)
  - [ ] Handle repeated identifiers (consistent pseudonymization)
  - [ ] Preserve non-PII data
- [ ] Create `generate_audit(transformations)` function

#### 6.3 Configuration
- [ ] Create `AnonymizationConfig` dataclass
- [ ] Create `src/anonymization/config.py`
- [ ] Support strategy selection per PII type
- [ ] Support global settings (mask_char, redact_placeholder, pseudo_key)

#### 6.4 Testing
- [ ] Unit tests for each strategy
- [ ] Test HMAC pseudonymization (consistent hashing)
- [ ] Test overlapping PII handling
- [ ] Test repeated identifiers (same email multiple times)
- [ ] Test edge cases (NULL values, empty strings)
- [ ] Integration test with detection results

### Files to Create
```
src/anonymization/
├── __init__.py
├── models.py
├── strategies.py
├── transformer.py
└── config.py

tests/unit/anonymization/
├── test_strategies.py
└── test_transformer.py
```

### Verification Commands
```bash
# Run tests
pytest tests/unit/anonymization/ -v

# Test transformation
python -m src.anonymization.transformer --input data/samples/customers.csv --detections detections.json
```

### Acceptance Criteria
- [ ] All transformation strategies implemented
- [ ] Transformations apply correctly to DataFrames
- [ ] Overlapping detections handled (no data corruption)
- [ ] Pseudonymization consistent (same input → same output)
- [ ] Audit log accurate (counts, types, strategies)
- [ ] Original data never modified (immutability)
- [ ] Unit tests pass with >80% coverage
- [ ] No PII values in audit logs

### Dependencies
- Milestone 5 complete

---

## Milestone 7: Pipeline Orchestration and Storage

**Duration**: 1 week  
**Status**: ⏳ Not Started

### Objectives
- Integrate all pipeline stages into cohesive workflow
- Implement DuckDB storage for results and metadata
- Add error handling and logging throughout pipeline
- Create pipeline result dataclasses and contracts

### Tasks

#### 7.1 Pipeline Module
- [ ] Create `src/pipeline/models.py` with dataclasses:
  - [ ] `PipelineConfig`
  - [ ] `PipelineResult`
- [ ] Create `src/pipeline/pipeline.py`
  - [ ] `DataPipeline` class with `run()` method
  - [ ] Orchestrate stages: Ingest → Profile → Validate → Detect → Transform → Store → Report
  - [ ] Error handling for each stage
  - [ ] Logging at stage boundaries
  - [ ] Generate unique run IDs

#### 7.2 Storage Module
- [ ] Create `src/storage/duckdb_manager.py`
  - [ ] `initialize_database()`: Create schema and tables
  - [ ] `save_dataset()`: Insert dataset metadata
  - [ ] `save_processing_run()`: Insert run record
  - [ ] `save_quality_metrics()`: Insert quality data
  - [ ] `save_detection_stats()`: Insert aggregated detection stats
  - [ ] `query_history()`: Retrieve past runs
  - [ ] `cleanup_old_runs()`: Retention policy
- [ ] Implement database schema (as per architecture spec)
- [ ] Add database connection management and error handling

#### 7.3 Temporary File Management
- [ ] Create `src/storage/temp_manager.py`
  - [ ] `create_temp_file()` and `create_temp_dir()`
  - [ ] `cleanup_temp_files(session_id)`
  - [ ] `auto_cleanup_on_exit()`
- [ ] Integrate with pipeline for session-scoped cleanup

#### 7.4 Testing
- [ ] Integration test for full pipeline execution
- [ ] Test with sample CSV and JSON files
- [ ] Verify database inserts and queries
- [ ] Test error handling (stage failures)
- [ ] Test cleanup and rollback

### Files to Create
```
src/pipeline/
├── __init__.py
├── models.py
└── pipeline.py

src/storage/
├── __init__.py
├── duckdb_manager.py
└── temp_manager.py

tests/integration/
└── test_pipeline.py

data/
└── pipeline.duckdb  # Created by application
```

### Verification Commands
```bash
# Initialize database
python -m src.storage.duckdb_manager --init

# Run pipeline integration test
pytest tests/integration/test_pipeline.py -v

# Test pipeline with sample data
python -m src.pipeline.pipeline --input data/samples/customers.csv --method rule-based
```

### Acceptance Criteria
- [ ] Pipeline executes all stages successfully
- [ ] DuckDB database created with correct schema
- [ ] Dataset and run metadata persisted
- [ ] Quality metrics and detection stats saved
- [ ] Temporary files cleaned up automatically
- [ ] Error handling prevents data corruption
- [ ] Stage durations logged
- [ ] Integration tests pass
- [ ] Pipeline results structured correctly

### Dependencies
- Milestones 2-6 complete

---

## Milestone 8: Experimental Evaluation Framework

**Duration**: 2 weeks  
**Status**: ⏳ Not Started

### Objectives
- Generate synthetic labeled dataset for evaluation
- Implement experiment runner for method comparison
- Calculate precision, recall, F1-score, and timing metrics
- Store evaluation results in database

### Tasks

#### 8.1 Dataset Generation
- [ ] Create `src/evaluation/dataset_generator.py`
  - [ ] `generate_synthetic_dataset(config)` function
  - [ ] Use Faker for realistic PII generation
  - [ ] Generate positive examples (with PII)
  - [ ] Generate negative examples (no PII)
  - [ ] Include edge cases and adversarial examples
  - [ ] Generate ground truth annotations
- [ ] Create `GroundTruthAnnotation` and `Entity` dataclasses
- [ ] Save dataset and annotations to JSON

#### 8.2 Metrics Calculation
- [ ] Create `src/evaluation/metrics.py`
  - [ ] `match_predictions(ground_truth, predictions)`: Entity matching logic
  - [ ] `calculate_metrics(y_true, y_pred)`: Precision, recall, F1
  - [ ] `confusion_matrix(y_true, y_pred)`: TP, FP, FN, TN
  - [ ] `classification_report()`: Per-category metrics
  - [ ] `calculate_timing_stats(times)`: Mean, std, min, max

#### 8.3 Experiment Runner
- [ ] Create `src/evaluation/experiment_runner.py`
  - [ ] `run_experiment(dataset, method, config)` function
  - [ ] `warmup_model(method)`: Pre-load NLP model
  - [ ] `time_detection(dataset, method, runs)`: Repeated timing
  - [ ] `collect_predictions(dataset, method)`: Get all predictions
  - [ ] Generate experiment report

#### 8.4 CLI Scripts
- [ ] Create `experiments/scripts/generate_dataset.py` CLI script
- [ ] Create `experiments/scripts/run_evaluation.py` CLI script
- [ ] Create `experiments/scripts/generate_report.py` CLI script
- [ ] Support command-line arguments for configuration

#### 8.5 Testing
- [ ] Unit tests for dataset generator
- [ ] Unit tests for metrics calculations (with known inputs)
- [ ] Test matching logic (exact and partial)
- [ ] Verify reproducibility (same seed → same results)
- [ ] Integration test for full experiment

### Files to Create
```
src/evaluation/
├── __init__.py
├── models.py
├── dataset_generator.py
├── metrics.py
└── experiment_runner.py

experiments/
├── configs/
│   └── experiment_config.yaml
├── scripts/
│   ├── generate_dataset.py
│   ├── run_evaluation.py
│   └── generate_report.py
└── results/
    └── .gitkeep

data/synthetic/
└── eval_dataset.json  # Generated

tests/unit/evaluation/
├── test_dataset_generator.py
├── test_metrics.py
└── test_experiment_runner.py
```

### Verification Commands
```bash
# Generate dataset
python experiments/scripts/generate_dataset.py --seed 42 --size 5000 --output data/synthetic/eval_dataset.json

# Run experiments
python experiments/scripts/run_evaluation.py --dataset data/synthetic/eval_dataset.json --methods rule-based,nlp-assisted --runs 3

# Generate report
python experiments/scripts/generate_report.py --results experiments/results/metrics_20261025.json

# Run unit tests
pytest tests/unit/evaluation/ -v
```

### Acceptance Criteria
- [ ] Synthetic dataset generation reproducible (same seed)
- [ ] Dataset contains positive and negative examples
- [ ] Ground truth annotations accurate
- [ ] Metrics calculations correct (verified with known inputs)
- [ ] Experiment runner executes both methods
- [ ] Timing measurements accurate (excludes setup/warmup)
- [ ] Results saved to database and JSON
- [ ] CLI scripts functional and documented
- [ ] Unit tests pass with >70% coverage
- [ ] Reproducibility verified (re-run produces same metrics)

### Dependencies
- Milestones 4-7 complete

---

## Milestone 9: UI Implementation

**Duration**: 2 weeks  
**Status**: ⏳ Not Started

### Objectives
- Build all remaining Streamlit pages
- Integrate UI with backend pipeline and evaluation modules
- Implement navigation and state management
- Apply design system and polish UI

### Tasks

#### 9.1 Complete Page Implementation
- [ ] Create `src/ui/pages/detection.py` (PII Detection page)
- [ ] Create `src/ui/pages/anonymization.py` (Anonymization page)
- [ ] Create `src/ui/pages/comparison.py` (Method Comparison page)
- [ ] Create `src/ui/pages/experiments.py` (Experiment Results page)
- [ ] Create `src/ui/pages/settings.py` (Settings/History page, optional)
- [ ] Update `src/ui/pages/home.py` with final content

#### 9.2 UI Components Completion
- [ ] Finalize `src/ui/components/metrics.py`
- [ ] Finalize `src/ui/components/charts.py`
- [ ] Finalize `src/ui/components/tables.py`
- [ ] Create `src/ui/components/feedback.py` (success/error messages)
- [ ] Create `src/ui/components/forms.py` (configuration forms)

#### 9.3 Navigation and State Management
- [ ] Update `app.py` with complete navigation
- [ ] Implement sidebar with all page links
- [ ] Add breadcrumb or progress indicators
- [ ] Manage session state across pages
- [ ] Implement state cleanup on new uploads

#### 9.4 Integration with Backend
- [ ] Wire upload page to ingestion module
- [ ] Wire quality page to validation module
- [ ] Wire detection page to detection module
- [ ] Wire anonymization page to transformation module
- [ ] Wire comparison page to both detectors
- [ ] Wire experiments page to evaluation results

#### 9.5 Design System Application
- [ ] Create `.streamlit/config.toml` with theme
- [ ] Add custom CSS if needed (minimal)
- [ ] Apply consistent colors and typography
- [ ] Ensure all metric cards, charts, tables use design system
- [ ] Polish empty states and error messages

#### 9.6 Testing
- [ ] Manual UI testing for each page
- [ ] Test complete user workflows (upload → process → export)
- [ ] Test error scenarios and edge cases
- [ ] Test navigation and state transitions
- [ ] Verify all charts and tables render correctly

### Files to Create/Update
```
app.py  # Update with navigation

src/ui/pages/
├── home.py  # Update
├── upload.py  # Already exists
├── quality.py  # Already exists
├── detection.py  # New
├── anonymization.py  # New
├── comparison.py  # New
├── experiments.py  # New
└── settings.py  # New (optional)

src/ui/components/
├── metrics.py  # Finalize
├── charts.py  # Finalize
├── tables.py  # Finalize
├── feedback.py  # New
└── forms.py  # New

.streamlit/
└── config.toml  # New

tests/ui/
└── test_workflows.py  # Manual test scenarios
```

### Verification Commands
```bash
# Launch app
streamlit run app.py

# Test workflows:
# 1. Upload → Quality → Detection → Anonymization → Export
# 2. Upload → Detection (Rule-Based) → Comparison → Experiments
# 3. Settings → View History → Clear Old Runs
```

### Acceptance Criteria
- [ ] All pages implemented and accessible
- [ ] Navigation smooth and intuitive
- [ ] UI matches design specifications (colors, typography, layout)
- [ ] All workflows functional end-to-end
- [ ] Charts and visualizations correct and interactive
- [ ] Error messages clear and actionable
- [ ] Empty states helpful
- [ ] Loading indicators present for long operations
- [ ] Download buttons work correctly
- [ ] Session state managed correctly
- [ ] UI responsive (desktop/laptop optimized)
- [ ] No console errors in Streamlit logs
- [ ] Professional appearance suitable for portfolio

### Dependencies
- Milestones 2-8 complete

---

## Milestone 10: Integration and Hardening

**Duration**: 1 week  
**Status**: ⏳ Not Started

### Objectives
- Execute full suite of unit and integration tests
- Fix bugs and edge cases
- Validate privacy and security controls
- Optimize performance where needed
- Achieve test coverage targets

### Tasks

#### 10.1 Testing
- [ ] Run all unit tests and fix failures
- [ ] Run integration tests and fix issues
- [ ] Add missing tests for uncovered code
- [ ] Achieve >70% test coverage for core modules
- [ ] Test CSV formula injection protection
- [ ] Test all error paths and edge cases

#### 10.2 Bug Fixes
- [ ] Fix any crashes or exceptions
- [ ] Fix data corruption issues
- [ ] Fix UI rendering issues
- [ ] Fix performance bottlenecks
- [ ] Address linting warnings

#### 10.3 Security and Privacy Validation
- [ ] Verify no PII in logs (audit all log statements)
- [ ] Verify no PII in database (only aggregated stats)
- [ ] Test input validation (file types, sizes, path traversal)
- [ ] Test CSV formula injection protection on export
- [ ] Verify temporary file cleanup
- [ ] Check for hardcoded secrets

#### 10.4 Performance Optimization
- [ ] Profile pipeline execution time
- [ ] Optimize slow operations (if >5min for 100K rows)
- [ ] Add caching where appropriate (Streamlit `@st.cache_data`)
- [ ] Optimize database queries if needed

#### 10.5 Documentation Updates
- [ ] Update README with latest instructions
- [ ] Document any configuration changes
- [ ] Update docstrings for modified functions
- [ ] Add inline comments for complex logic

### Files to Update
- All source files (bug fixes)
- All test files (new tests, fixes)
- README.md (instructions)
- config/default.yaml (if settings changed)

### Verification Commands
```bash
# Run full test suite
pytest tests/ -v --cov=src --cov-report=term --cov-report=html

# Check coverage
open htmlcov/index.html

# Run linting
ruff check src/ tests/

# Test performance
python experiments/scripts/run_evaluation.py --dataset data/samples/large_dataset.csv --profile
```

### Acceptance Criteria
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Test coverage ≥70% for core modules (ingestion, validation, detection, anonymization, pipeline)
- [ ] No critical linting errors
- [ ] No known crashes or data corruption bugs
- [ ] Performance meets targets (<5min for 100K rows)
- [ ] Privacy controls validated (no PII leaks)
- [ ] Security controls validated (input validation, formula injection)
- [ ] Temporary files cleaned up correctly
- [ ] Documentation updated and accurate

### Dependencies
- Milestone 9 complete

---

## Milestone 11: Research Report and Documentation

**Duration**: 1-2 weeks  
**Status**: ⏳ Not Started

### Objectives
- Run final experiments with production configuration
- Analyze results and perform error analysis
- Write comprehensive research report
- Create figures and visualizations
- Complete README and user documentation

### Tasks

#### 11.1 Final Experiments
- [ ] Generate final evaluation dataset (seed=42, size=5000)
- [ ] Run both detection methods (3 runs each)
- [ ] Collect metrics and timing data
- [ ] Perform error analysis (sample FPs and FNs)
- [ ] Save results to database and JSON

#### 11.2 Research Report
- [ ] Write `reports/research_report.md`
  - [ ] Abstract
  - [ ] Introduction (background, motivation, research question)
  - [ ] Related work (brief literature review)
  - [ ] Methodology (architecture, detection methods, dataset, evaluation protocol)
  - [ ] Results (metrics tables, charts, confusion matrices, error analysis)
  - [ ] Discussion (interpretation, trade-offs, limitations)
  - [ ] Conclusion (summary, contributions, future work)
  - [ ] References
- [ ] Generate figures (save to `reports/figures/`)
  - [ ] Precision/recall/F1 comparison bar chart
  - [ ] Confusion matrices (heatmaps)
  - [ ] Processing time comparison
  - [ ] Per-category performance charts
- [ ] Export experiment results to `reports/results/metrics.json`

#### 11.3 README Completion
- [ ] Update `README.md` with complete content:
  - [ ] Project overview and motivation
  - [ ] Features list
  - [ ] Architecture overview
  - [ ] Technology stack
  - [ ] Installation instructions (Windows)
  - [ ] Usage instructions
  - [ ] Sample datasets
  - [ ] Running tests
  - [ ] Running experiments
  - [ ] Results summary (link to research report)
  - [ ] Limitations and disclaimers
  - [ ] Troubleshooting
  - [ ] Contributing (optional)
  - [ ] License
- [ ] Add architecture diagram (Mermaid or image)
- [ ] Add screenshots of UI pages

#### 11.4 Additional Documentation
- [ ] Create `docs/ARCHITECTURE.md` (detailed architecture from spec)
- [ ] Create `docs/API.md` (module and function documentation)
- [ ] Create `docs/CONTRIBUTING.md` (development guidelines, optional)
- [ ] Update all docstrings and inline comments
- [ ] Generate API documentation (optional, using Sphinx or pdoc)

#### 11.5 Screenshots
- [ ] Capture screenshots of all UI pages
- [ ] Save to `docs/screenshots/`
- [ ] Include in README and documentation

### Files to Create/Update
```
README.md  # Complete update

reports/
├── research_report.md  # New
├── figures/
│   ├── precision_recall_f1_comparison.png
│   ├── confusion_matrix_rule_based.png
│   ├── confusion_matrix_nlp.png
│   ├── processing_time_comparison.png
│   └── per_category_performance.png
└── results/
    ├── metrics.json
    └── experiment_summary.csv

docs/
├── screenshots/
│   ├── home_page.png
│   ├── upload_page.png
│   ├── quality_page.png
│   ├── detection_page.png
│   ├── anonymization_page.png
│   ├── comparison_page.png
│   └── experiments_page.png
├── ARCHITECTURE.md  # New
├── API.md  # New
└── CONTRIBUTING.md  # New (optional)
```

### Verification Commands
```bash
# Run final experiments
python experiments/scripts/run_evaluation.py --dataset data/synthetic/eval_dataset.json --methods rule-based,nlp-assisted --runs 3 --output reports/results/metrics.json

# Generate report figures
python experiments/scripts/generate_report.py --results reports/results/metrics.json --output reports/

# Verify README instructions
# Follow README setup instructions on clean machine
```

### Acceptance Criteria
- [ ] Final experiments executed successfully
- [ ] Metrics and timing data collected
- [ ] Research report complete (10-15 pages)
- [ ] Figures generated and embedded in report
- [ ] README complete and accurate
- [ ] Installation instructions tested on clean environment
- [ ] Screenshots captured and included
- [ ] Architecture documentation complete
- [ ] All limitations clearly documented
- [ ] No fabricated results or citations
- [ ] Research report suitable for portfolio and master's application

### Dependencies
- Milestone 10 complete

---

## Milestone 12: Packaging and Optional Deployment

**Duration**: 1 week  
**Status**: ⏳ Not Started

### Objectives
- Verify reproducible setup from scratch
- Create Docker container (optional)
- Deploy to Streamlit Community Cloud (optional)
- Finalize GitHub repository
- Create demonstration video or script (optional)

### Tasks

#### 12.1 Reproducibility Verification
- [ ] Test setup on clean Windows machine
- [ ] Verify all dependencies install correctly
- [ ] Verify spaCy model downloads successfully
- [ ] Verify application launches and works end-to-end
- [ ] Fix any setup issues discovered
- [ ] Update README with any missing steps

#### 12.2 Docker Containerization (Optional)
- [ ] Create `Dockerfile`
- [ ] Create `.dockerignore`
- [ ] Build Docker image
- [ ] Test container locally
- [ ] Document Docker usage in README
- [ ] Optionally push to Docker Hub

#### 12.3 Deployment Preparation (Optional)
- [ ] Review Streamlit Community Cloud requirements
- [ ] Create `requirements.txt` compatible with Streamlit Cloud
- [ ] Configure secrets (if needed) in `.streamlit/secrets.toml.example`
- [ ] Test with in-memory DuckDB (ephemeral filesystem)
- [ ] Prepare synthetic demo dataset for public deployment
- [ ] Add disclaimer for public deployment (no real data)

#### 12.4 Deployment (Optional)
- [ ] Connect GitHub repository to Streamlit Cloud
- [ ] Configure deployment settings
- [ ] Deploy application
- [ ] Test deployed application
- [ ] Monitor for errors
- [ ] Update README with deployed URL

#### 12.5 GitHub Repository Finalization
- [ ] Review all files in repository
- [ ] Ensure `.gitignore` complete
- [ ] Remove any secrets or sensitive data
- [ ] Verify no large files committed
- [ ] Create detailed commit history
- [ ] Tag release version (v1.0.0)
- [ ] Create GitHub README (same as project README)
- [ ] Add topics/tags to repository

#### 12.6 Demonstration Materials (Optional)
- [ ] Create demonstration script (step-by-step usage)
- [ ] Record demonstration video (5-10 minutes)
- [ ] Upload video to YouTube or portfolio site
- [ ] Link video in README

### Files to Create
```
Dockerfile  # Optional
.dockerignore  # Optional
.streamlit/secrets.toml.example  # If secrets needed

docs/
├── DEPLOYMENT.md  # Deployment instructions
└── DEMONSTRATION.md  # Demo script

# Video file (not committed)
demo_video.mp4  # Upload separately
```

### Verification Commands
```bash
# Test clean installation (on clean machine or VM)
git clone <repo-url>
cd Privacy-Aware-Data-Engineering-Pipeline
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_lg
streamlit run app.py

# Build Docker image (optional)
docker build -t privacy-pipeline .
docker run -p 8501:8501 privacy-pipeline

# Test deployed application
# Visit deployed URL
# Upload sample dataset
# Complete full workflow
```

### Acceptance Criteria
- [ ] Fresh installation succeeds on clean Windows machine
- [ ] All dependencies install without errors
- [ ] Application runs and completes full workflow
- [ ] (Optional) Docker container builds and runs successfully
- [ ] (Optional) Application deployed to Streamlit Cloud
- [ ] (Optional) Deployed application functional with demo data
- [ ] GitHub repository clean and professional
- [ ] No secrets or sensitive data in repository
- [ ] README accurate and complete
- [ ] Release tagged (v1.0.0)
- [ ] (Optional) Demonstration video created and linked
- [ ] Project ready for portfolio and master's application submission

### Dependencies
- Milestone 11 complete

---

## Summary of Milestones

| Milestone | Duration | Status | Key Deliverables |
|-----------|----------|--------|------------------|
| 0. Requirements & Specs | 1 week | In Progress | All planning documents |
| 1. Project Foundation | 1 week | Not Started | Environment, structure, basic app |
| 2. Data Ingestion | 1 week | Not Started | CSV/JSON loading, upload page |
| 3. Data Quality | 1 week | Not Started | Profiling, quality page |
| 4. Rule-Based Detection | 1-2 weeks | Not Started | Custom detectors |
| 5. NLP Detection | 1-2 weeks | Not Started | Presidio + spaCy integration |
| 6. Anonymization | 1 week | Not Started | Transformation strategies |
| 7. Pipeline & Storage | 1 week | Not Started | Orchestration, DuckDB |
| 8. Evaluation Framework | 2 weeks | Not Started | Experiments, metrics |
| 9. UI Implementation | 2 weeks | Not Started | All pages, design system |
| 10. Integration & Hardening | 1 week | Not Started | Testing, bug fixes, optimization |
| 11. Research Report & Docs | 1-2 weeks | Not Started | Report, README, screenshots |
| 12. Packaging & Deployment | 1 week | Not Started | Docker, deployment, demo |

**Total Estimated Duration**: 8-12 weeks (part-time development)

---

## Development Workflow

### For Each Milestone

1. **Pre-work**:
   - Review milestone objectives and tasks
   - Ensure dependencies complete
   - Read relevant specifications

2. **Implementation**:
   - Create files and implement features
   - Follow architecture and design specs
   - Write unit tests alongside code
   - Commit frequently with clear messages

3. **Testing**:
   - Run unit tests and fix failures
   - Test manually in UI (if applicable)
   - Test edge cases and error handling

4. **Review**:
   - Review code against requirements
   - Check code quality (linting)
   - Verify acceptance criteria met

5. **Documentation**:
   - Update docstrings and comments
   - Update README if needed
   - Document any deviations from plan

6. **Milestone Report**:
   - Summarize what was implemented
   - List files created/modified
   - Note any issues or changes to plan
   - Confirm acceptance criteria
   - Get approval before next milestone

### Git Workflow

```bash
# Start new milestone
git checkout -b milestone-N-description

# Implement and commit incrementally
git add <files>
git commit -m "feat: implement X"

# Run tests before pushing
pytest tests/
ruff check src/

# Push to GitHub
git push origin milestone-N-description

# After milestone completion
git checkout main
git merge milestone-N-description
git tag vN.0
git push origin main --tags
```

---

## Next Steps

1. **Review and approve this roadmap** along with other planning documents
2. **Begin Milestone 1** (Project Foundation)
3. **Work through milestones sequentially**, seeking approval before proceeding
4. **Adapt plan as needed** based on discoveries during implementation
5. **Maintain momentum** with regular commits and milestone completions

---

**Document Status**: Draft  
**Next Review**: After complete specifications approved  
**Ready for Implementation**: After Milestone 0 complete
