# Architecture Specification
## Privacy-Aware Data Engineering Pipeline

**Version:** 1.0  
**Date:** October 25, 2026

---

## 1. System Overview

### 1.1 Architecture Pattern

The system follows a **modular pipeline architecture** with clear separation between:
- **Presentation layer** (Streamlit UI)
- **Application layer** (pipeline orchestration, business logic)
- **Data layer** (storage, retrieval, transformation)
- **Evaluation layer** (experimental framework, metrics)

**Key architectural principles:**
- **UI independence**: Core processing logic has no Streamlit dependencies
- **Modular stages**: Each pipeline stage is independently testable
- **Clear contracts**: Defined input/output interfaces using dataclasses
- **Immutability**: Original data never modified; transformations create new outputs
- **Error isolation**: Failures contained within stages, with graceful degradation

### 1.2 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Streamlit UI Layer                        │
│  (Pages: Home, Upload, Quality, Detection, Anonymization, etc.) │
└─────────────────┬───────────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────────┐
│                   Application Layer (Pipeline)                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  Ingestion  │─▶│  Profiling  │─▶│  Validation │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  Detection  │─▶│Transformation│─▶│   Storage   │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────┬───────────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────────┐
│                         Data Layer                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  DuckDB     │  │  Temp Files │  │  Config     │             │
│  │  (Analytics)│  │  (Session)  │  │  (Settings) │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                    Evaluation Layer (Research)                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  Dataset    │─▶│  Experiment │─▶│   Metrics   │             │
│  │  Generator  │  │  Runner     │  │  Calculator │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└──────────────────────────────────────────────────────────────────┘
```

---

## 2. Component Specifications

### 2.1 Presentation Layer (UI)

**Responsibility**: User interaction, visualization, workflow orchestration

**Components:**
- **Streamlit Pages**: Multi-page app structure
  - `app.py`: Entry point, navigation setup
  - `src/ui/pages/home.py`: Overview and introduction
  - `src/ui/pages/upload.py`: File upload and preview
  - `src/ui/pages/quality.py`: Data quality dashboard
  - `src/ui/pages/detection.py`: PII detection results
  - `src/ui/pages/anonymization.py`: Transformation interface
  - `src/ui/pages/comparison.py`: Method comparison
  - `src/ui/pages/experiments.py`: Evaluation results
  - `src/ui/pages/settings.py`: Configuration and history

- **UI Components**: Reusable widgets
  - `src/ui/components/metrics.py`: Metric cards, KPI displays
  - `src/ui/components/charts.py`: Plotly chart wrappers
  - `src/ui/components/tables.py`: Formatted dataframe displays
  - `src/ui/components/feedback.py`: Success/error/warning messages
  - `src/ui/components/forms.py`: Configuration forms

- **State Management**:
  - Use `st.session_state` for UI state
  - Store pipeline results in session state
  - Clear state on new uploads

**Dependencies**: Streamlit, Plotly  
**Depends on**: Application layer (pipeline modules)  
**Rules**:
- No business logic in UI code
- No direct database access from pages
- All data processing delegated to application layer
- UI components accept data as parameters, not session state

### 2.2 Application Layer (Pipeline)

**Responsibility**: Business logic, data processing, pipeline orchestration

#### 2.2.1 Ingestion Module

**Location**: `src/ingestion/`

**Components:**
- `loader.py`: File loading and parsing
  - `load_csv(file_path, encoding, delimiter)`: Load CSV to DataFrame
  - `load_json(file_path)`: Load JSON to DataFrame
  - `detect_encoding(file_path)`: Auto-detect file encoding
  - `infer_types(df)`: Infer column data types

- `validator.py`: Input validation
  - `validate_file(file, max_size, allowed_types)`: File-level validation
  - `validate_dataframe(df, max_rows, max_columns)`: DataFrame validation
  - `check_column_names(df)`: Validate column names (no duplicates, non-empty)

**Contracts:**
```python
@dataclass
class IngestionResult:
    success: bool
    dataframe: Optional[pd.DataFrame]
    metadata: Dict[str, Any]  # {rows, columns, size_bytes, encoding, ...}
    errors: List[str]
    warnings: List[str]
```

#### 2.2.2 Validation Module

**Location**: `src/validation/`

**Components:**
- `profiler.py`: Data quality profiling
  - `profile_dataframe(df)`: Generate quality report
  - `detect_missing_values(df)`: Count and percentage
  - `detect_duplicates(df, subset)`: Exact and key-based duplicates
  - `detect_type_issues(df)`: Type consistency checks
  - `calculate_quality_score(profile)`: Overall quality metric

- `schema_validator.py`: Schema and constraint validation
  - `validate_schema(df, schema)`: Check against Pandera schema
  - `validate_constraints(df, constraints)`: Range, pattern, uniqueness checks

- `cleaner.py`: Explicit data cleaning operations
  - `remove_duplicates(df, subset, keep)`: Remove duplicate rows
  - `fill_missing(df, column, strategy)`: Fill missing values
  - `drop_columns(df, columns)`: Remove columns
  - `convert_types(df, column, target_type)`: Type conversion

**Contracts:**
```python
@dataclass
class QualityProfile:
    row_count: int
    column_count: int
    missing_values: Dict[str, int]  # column -> count
    duplicate_rows: int
    type_issues: Dict[str, List[str]]  # column -> issues
    quality_score: float  # 0-100
    issues: List[QualityIssue]

@dataclass
class QualityIssue:
    severity: str  # 'error', 'warning', 'info'
    category: str  # 'missing', 'duplicate', 'type', 'constraint'
    column: Optional[str]
    description: str
    count: int
```

#### 2.2.3 Detection Module

**Location**: `src/detection/`

**Components:**
- `base_detector.py`: Abstract detector interface
  ```python
  class PIIDetector(ABC):
      @abstractmethod
      def detect(self, df: pd.DataFrame) -> List[PIIDetection]:
          pass
  ```

- `rule_based_detector.py`: Custom rule-based PII detection
  - `EmailDetector`: RFC 5322 subset pattern + domain validation
  - `PhoneDetector`: North American + international formats
  - `IPAddressDetector`: IPv4, IPv6
  - `CreditCardDetector`: Patterns + Luhn validation
  - `SSNDetector`: US SSN format + validation

- `nlp_detector.py`: Presidio + spaCy integration
  - `PresidioDetector`: Wrapper for Presidio Analyzer
  - `configure_recognizers()`: Setup NER-based recognizers
  - `filter_nlp_entities()`: Extract only NLP-derived detections

- `detector_factory.py`: Factory for detector instantiation
  - `create_detector(method: str)`: Return appropriate detector

**Contracts:**
```python
@dataclass
class PIIDetection:
    column: str
    row_index: int
    pii_type: str  # 'email', 'phone', 'ssn', etc.
    start: int  # character position (for text fields)
    end: int
    confidence: float  # 0.0-1.0
    method: str  # 'rule-based', 'nlp-assisted'
```

#### 2.2.4 Anonymization Module

**Location**: `src/anonymization/`

**Components:**
- `strategies.py`: Transformation strategies
  - `MaskStrategy`: Replace with pattern (e.g., "***@***.***")
  - `RedactStrategy`: Remove or replace with placeholder
  - `PseudonymizeStrategy`: HMAC-based consistent hashing
  - `GeneralizeStrategy`: Replace with category label

- `transformer.py`: Apply transformations
  - `apply_transformations(df, detections, config)`: Execute transformations
  - `handle_overlaps(detections)`: Resolve overlapping PII
  - `generate_audit(transformations)`: Create transformation log

- `config.py`: Transformation configuration
  - `AnonymizationConfig`: Strategy per PII type, global settings

**Contracts:**
```python
@dataclass
class AnonymizationConfig:
    strategies: Dict[str, str]  # pii_type -> strategy_name
    mask_char: str = '*'
    redact_placeholder: str = '[REDACTED]'
    pseudo_key: Optional[str] = None  # HMAC key

@dataclass
class TransformationAudit:
    transformations_applied: int
    by_type: Dict[str, int]  # pii_type -> count
    by_strategy: Dict[str, int]  # strategy -> count
    columns_affected: List[str]
    rows_affected: int
```

#### 2.2.5 Pipeline Module

**Location**: `src/pipeline/`

**Components:**
- `pipeline.py`: Orchestrate end-to-end processing
  ```python
  class DataPipeline:
      def run(self, file_path: str, config: PipelineConfig) -> PipelineResult:
          # 1. Ingest
          # 2. Profile
          # 3. Validate
          # 4. Detect PII
          # 5. Transform
          # 6. Post-validate
          # 7. Store
          # 8. Report
  ```

- `config.py`: Pipeline configuration
  - `PipelineConfig`: Detection method, anonymization settings, validation rules

- `result.py`: Pipeline result dataclass
  - `PipelineResult`: Aggregates all stage results

**Contracts:**
```python
@dataclass
class PipelineConfig:
    detection_method: str  # 'rule-based', 'nlp-assisted'
    anonymization_config: AnonymizationConfig
    validation_schema: Optional[Dict]
    max_rows: int = 100_000
    max_file_size_mb: int = 50

@dataclass
class PipelineResult:
    run_id: str
    status: str  # 'success', 'partial', 'failed'
    ingestion: IngestionResult
    quality_profile: QualityProfile
    detections: List[PIIDetection]
    transformation_audit: TransformationAudit
    processed_data: pd.DataFrame
    duration_seconds: float
    errors: List[str]
    warnings: List[str]
```

### 2.3 Data Layer

#### 2.3.1 Storage Module

**Location**: `src/storage/`

**Components:**
- `duckdb_manager.py`: DuckDB database operations
  - `initialize_database()`: Create schema and tables
  - `save_dataset(metadata)`: Insert dataset record
  - `save_processing_run(run_result)`: Insert run record
  - `save_quality_metrics(run_id, profile)`: Insert quality data
  - `save_detection_stats(run_id, detections)`: Insert aggregated stats
  - `query_history(limit)`: Retrieve past runs
  - `cleanup_old_runs(keep_count)`: Retention policy

**Schema:**
```sql
-- datasets table
CREATE TABLE datasets (
    id VARCHAR PRIMARY KEY,
    name VARCHAR,
    upload_date TIMESTAMP,
    row_count INTEGER,
    column_count INTEGER,
    file_hash VARCHAR,
    size_bytes INTEGER
);

-- processing_runs table
CREATE TABLE processing_runs (
    run_id VARCHAR PRIMARY KEY,
    dataset_id VARCHAR,
    timestamp TIMESTAMP,
    method VARCHAR,  -- 'rule-based', 'nlp-assisted'
    status VARCHAR,  -- 'success', 'partial', 'failed'
    duration_seconds REAL,
    FOREIGN KEY (dataset_id) REFERENCES datasets(id)
);

-- quality_metrics table
CREATE TABLE quality_metrics (
    id INTEGER PRIMARY KEY,
    run_id VARCHAR,
    quality_score REAL,
    missing_values INTEGER,
    duplicate_rows INTEGER,
    issue_count INTEGER,
    FOREIGN KEY (run_id) REFERENCES processing_runs(run_id)
);

-- pii_detection_stats table
CREATE TABLE pii_detection_stats (
    id INTEGER PRIMARY KEY,
    run_id VARCHAR,
    pii_type VARCHAR,
    detection_count INTEGER,
    avg_confidence REAL,
    FOREIGN KEY (run_id) REFERENCES processing_runs(run_id)
);

-- evaluation_results table
CREATE TABLE evaluation_results (
    id INTEGER PRIMARY KEY,
    experiment_id VARCHAR,
    method VARCHAR,
    dataset_name VARCHAR,
    precision REAL,
    recall REAL,
    f1_score REAL,
    processing_time_seconds REAL,
    timestamp TIMESTAMP
);
```

#### 2.3.2 Temporary File Management

**Location**: `src/storage/temp_manager.py`

**Components:**
- `create_temp_file(suffix)`: Create temporary file
- `create_temp_dir()`: Create temporary directory
- `cleanup_temp_files(session_id)`: Delete session files
- `auto_cleanup_on_exit()`: Register cleanup handlers

**Strategy:**
- Use Python's `tempfile` module
- Session-scoped temporary directories
- Automatic cleanup on application exit
- Explicit cleanup after processing

### 2.4 Evaluation Layer

#### 2.4.1 Dataset Generation Module

**Location**: `src/evaluation/dataset_generator.py`

**Components:**
- `generate_synthetic_dataset(config)`: Create labeled dataset
  - Use Faker for realistic PII generation
  - Generate positive examples (with PII)
  - Generate negative examples (no PII, but similar structure)
  - Include edge cases (malformed, ambiguous, noisy)
  
- `GroundTruthAnnotation`: Dataclass for labels
  ```python
  @dataclass
  class GroundTruthAnnotation:
      text: str
      entities: List[Entity]
  
  @dataclass
  class Entity:
      start: int
      end: int
      label: str  # 'email', 'phone', etc.
  ```

#### 2.4.2 Experiment Runner Module

**Location**: `src/evaluation/experiment_runner.py`

**Components:**
- `run_experiment(dataset, method)`: Execute detection and measure
- `warmup_model(method)`: Pre-load models (exclude from timing)
- `time_detection(dataset, method, runs)`: Repeated timing
- `collect_predictions(dataset, method)`: Get all predictions

#### 2.4.3 Metrics Module

**Location**: `src/evaluation/metrics.py`

**Components:**
- `calculate_metrics(y_true, y_pred)`: Precision, recall, F1
- `match_predictions(ground_truth, predictions)`: Entity matching
- `confusion_matrix(y_true, y_pred)`: TP, FP, FN, TN
- `classification_report(y_true, y_pred)`: Per-category metrics
- `calculate_timing_stats(times)`: Mean, std, min, max

**Matching Rules:**
```python
def match_predictions(ground_truth: List[Entity], 
                      predictions: List[PIIDetection]) -> MatchResult:
    # Exact match: same span (start, end) and same label
    # Partial match (optional): IoU ≥ 0.5 and same label
    # Returns: TP, FP, FN counts
```

---

## 3. Data Flow

### 3.1 Main Processing Flow

```
User Upload File
    ↓
[Ingestion] Load & Validate File
    ↓
[Profiling] Analyze Data Quality
    ↓
[Validation] Check Schema & Constraints
    ↓
[Detection] Identify PII (Rule-based or NLP)
    ↓
[Anonymization] Apply Transformations
    ↓
[Post-Validation] Re-check Quality
    ↓
[Storage] Save Results to DuckDB
    ↓
[Reporting] Generate Summary
    ↓
Display Results in UI
```

### 3.2 Experiment Flow

```
[Dataset Generator] Create Synthetic Data with Ground Truth
    ↓
[Experiment Runner] 
    ├─ Method A (Rule-based) → Predictions
    └─ Method B (NLP-assisted) → Predictions
    ↓
[Metrics Calculator]
    ├─ Match predictions to ground truth
    ├─ Calculate precision, recall, F1
    └─ Measure processing time
    ↓
[Storage] Save to evaluation_results table
    ↓
[Reporting] Generate comparison charts
    ↓
Display in Experiments Page
```

### 3.3 Error Flow

```
Error Occurs in Pipeline Stage
    ↓
Log Error with Context
    ↓
Capture in Stage Result
    ↓
Propagate to Pipeline Result
    ↓
Update Run Status ('failed' or 'partial')
    ↓
Display Error in UI
    ↓
Allow User to Retry or Adjust Configuration
```

---

## 4. Module Dependencies

### 4.1 Dependency Graph

```
Presentation Layer (Streamlit Pages)
    ↓ depends on
Application Layer (Pipeline, Detection, Anonymization)
    ↓ depends on
Data Layer (Storage, Config)

Evaluation Layer (independent, used by Experiments Page)
    ↓ depends on
Detection Module (for method comparison)
```

### 4.2 Dependency Rules

1. **UI → Application**: Pages call pipeline and module functions, never vice versa
2. **Application → Data**: Modules use storage and config, storage doesn't call business logic
3. **No circular imports**: Strict unidirectional dependencies
4. **Evaluation independence**: Experiment runner can run without Streamlit
5. **Detector abstraction**: Detection module defines interface, implementations are pluggable

---

## 5. Configuration Management

### 5.1 Configuration Files

**Location**: `config/`

- `config/default.yaml`: Default settings
  ```yaml
  ingestion:
    max_file_size_mb: 50
    max_rows: 100000
    allowed_types: ['.csv', '.json']
  
  detection:
    rule_based:
      email: true
      phone: true
      ssn: true
      credit_card: true
      ip_address: true
    
    nlp_assisted:
      model: 'en_core_web_lg'
      confidence_threshold: 0.5
      recognizers: ['SpacyRecognizer']
  
  anonymization:
    default_strategy: 'mask'
    strategies:
      email: 'mask'
      phone: 'redact'
      ssn: 'pseudonymize'
  
  storage:
    database_path: 'data/pipeline.duckdb'
    retention_runs: 50
  ```

- `config/experiment.yaml`: Experiment-specific settings
  ```yaml
  dataset:
    size: 5000
    positive_ratio: 0.6
    noise_level: 0.1
    seed: 42
  
  evaluation:
    metrics: ['precision', 'recall', 'f1', 'timing']
    matching: 'exact'  # or 'partial'
    timing_runs: 3
  ```

### 5.2 Configuration Loading

**Location**: `src/utils/config_loader.py`

```python
def load_config(config_path: str = 'config/default.yaml') -> Dict:
    # Load YAML, merge with environment variable overrides
    pass

def get_config_value(key: str, default: Any = None) -> Any:
    # Dot-notation access: get_config_value('detection.rule_based.email')
    pass
```

### 5.3 Environment Variables

**Location**: `.env` (not committed, use `.env.example` as template)

```bash
# Optional overrides
PIPELINE_MAX_FILE_SIZE_MB=50
PIPELINE_MAX_ROWS=100000
SPACY_MODEL=en_core_web_lg
DUCKDB_PATH=data/pipeline.duckdb
PSEUDONYM_KEY=<generate-secure-key>
LOG_LEVEL=INFO
```

---

## 6. Logging and Monitoring

### 6.1 Logging Strategy

**Location**: `src/utils/logger.py`

**Configuration:**
- **Level**: INFO (configurable via environment variable)
- **Format**: `[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s`
- **Handlers**: 
  - Console (stdout)
  - File: `logs/pipeline.log` (rotating, max 10MB, 5 backups)

**Logging Rules:**
- **Never log raw PII values**
- Log PII categories and counts only
- Redact PII in exception messages
- Log all stage entries and exits
- Log configuration changes
- Log errors with full stack traces (but redact sensitive data)

**Example:**
```python
import logging
logger = logging.getLogger(__name__)

# Good
logger.info(f"Detected {len(detections)} PII instances of types: {set(d.pii_type for d in detections)}")

# Bad - DO NOT DO THIS
logger.info(f"Detected email: {email_value}")
```

### 6.2 Performance Monitoring

**Metrics to Track:**
- Pipeline stage durations
- Detection throughput (records/second)
- Memory usage (approximate)
- Database query times
- File I/O times

**Implementation:**
- Use Python `time.perf_counter()` for timing
- Log stage durations at INFO level
- Store aggregate metrics in DuckDB for analysis

---

## 7. Error Handling

### 7.1 Error Categories

1. **User Input Errors**:
   - Invalid file format
   - File too large
   - Malformed data
   - **Response**: Clear error message, allow retry

2. **Processing Errors**:
   - Detection failures
   - Transformation errors
   - Database errors
   - **Response**: Log error, return partial result with warning, allow retry

3. **System Errors**:
   - Out of memory
   - Model not found
   - Database corruption
   - **Response**: Log critical error, graceful shutdown, recovery instructions

### 7.2 Error Handling Pattern

```python
try:
    result = stage.execute(data)
except UserInputError as e:
    logger.warning(f"User input error: {e}")
    return StageResult(success=False, errors=[str(e)])
except ProcessingError as e:
    logger.error(f"Processing error: {e}", exc_info=True)
    return StageResult(success=False, errors=[str(e)])
except Exception as e:
    logger.critical(f"Unexpected error: {e}", exc_info=True)
    raise  # Re-raise for top-level handler
```

### 7.3 Graceful Degradation

- If NLP model fails to load, fall back to rule-based detection with warning
- If DuckDB unavailable, use in-memory storage with warning
- If experiment fails, allow manual analysis with exported data
- Always provide actionable error messages

---

## 8. Testing Strategy

### 8.1 Test Layers

1. **Unit Tests** (`tests/unit/`):
   - Test individual functions and classes
   - Mock external dependencies
   - Fast execution (<1 second per test)
   - Coverage target: >70% for core modules

2. **Integration Tests** (`tests/integration/`):
   - Test pipeline stages together
   - Use test database and temporary files
   - Test with small synthetic datasets
   - Coverage: Critical paths and error scenarios

3. **End-to-End Tests** (`tests/e2e/`):
   - Test complete pipeline execution
   - Use sample datasets from `data/samples/`
   - Verify final outputs and reports
   - Coverage: Happy path and key error cases

4. **Evaluation Tests** (`tests/evaluation/`):
   - Test metric calculations with known inputs
   - Test ground truth matching logic
   - Test dataset generation reproducibility
   - Verify experiment runner correctness

### 8.2 Test Fixtures

**Location**: `tests/fixtures/`

- `sample_data.py`: Generate small test DataFrames
- `mock_detections.py`: Mock PII detection results
- `ground_truth.json`: Small labeled dataset for evaluation tests

### 8.3 Testing Tools

- **pytest**: Test framework
- **pytest-cov**: Coverage measurement
- **pytest-mock**: Mocking library
- **freezegun**: Time mocking (for reproducible timestamps)

---

## 9. Security Architecture

### 9.1 Input Validation Layer

**Location**: All entry points (upload handlers, API if added)

**Controls:**
- File type whitelist enforcement
- File size limits
- Path traversal protection (no `../` in filenames)
- Safe parsing (no `eval`, `exec`)
- Encoding validation

### 9.2 Data Protection Layer

**Locations**: Logging, database, exports

**Controls:**
- PII redaction in logs
- No raw PII in database
- CSV formula injection protection on export
- Secure temporary file creation (`tempfile.mkstemp`)

### 9.3 Secrets Management

**Strategy:**
- Environment variables for configuration
- `.env` file for local development (not committed)
- `.streamlit/secrets.toml` for Streamlit deployment (not committed)
- No hardcoded secrets in code

### 9.4 Dependency Security

**Strategy:**
- Pin all dependencies with exact versions (`requirements.txt`)
- Regular security audits (`pip-audit`)
- Review dependencies before adding
- Minimal dependency footprint

---

## 10. Deployment Architecture

### 10.1 Local Deployment (Primary)

**Environment**: Windows 10/11, Python 3.11

**Structure:**
```
User's Machine
├── Python 3.11 (virtual environment)
├── Application Code (from Git)
├── DuckDB File (local)
├── Temporary Files (session-scoped)
└── Streamlit Server (localhost:8501)
```

**Advantages:**
- Full control over data
- No network latency
- No deployment costs
- Privacy-friendly (data never leaves machine)

**Setup:**
1. Clone repository
2. Create virtual environment
3. Install dependencies (`pip install -r requirements.txt`)
4. Download spaCy model (`python -m spacy download en_core_web_lg`)
5. Run application (`streamlit run app.py`)

### 10.2 Cloud Deployment (Optional)

**Target**: Streamlit Community Cloud

**Structure:**
```
Streamlit Cloud
├── App Instance (ephemeral filesystem)
├── GitHub Repository (code source)
├── Secrets (via Streamlit secrets management)
└── Public URL (*.streamlit.app)
```

**Considerations:**
- **Ephemeral filesystem**: DuckDB file lost on restart (use in-memory mode)
- **No persistent uploads**: Use session-scoped processing only
- **Privacy**: Only use with synthetic data (no real sensitive data)
- **Resource limits**: 1 GB RAM, limited CPU

**Deployment Steps:**
1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Configure secrets (if needed)
4. Deploy

### 10.3 Docker Deployment (Optional)

**Dockerfile Strategy:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_lg
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

**Advantages:**
- Reproducible environment
- Easy distribution
- Platform-independent (Windows, macOS, Linux)

---

## 11. Performance Considerations

### 11.1 Optimization Strategies

1. **Data Processing:**
   - Use pandas vectorized operations (avoid Python loops)
   - Batch PII detection (process multiple rows together)
   - Stream large files if needed (read in chunks)

2. **Detection:**
   - Compile regex patterns once (module-level)
   - Cache NLP model (load once per session)
   - Parallelize detection where safe (multiprocessing for large datasets)

3. **Database:**
   - Create indexes on frequently queried columns
   - Use DuckDB's columnar storage efficiently
   - Batch inserts for evaluation results

4. **UI:**
   - Cache expensive computations (`@st.cache_data`)
   - Paginate large tables
   - Lazy-load charts (only render visible content)

### 11.2 Performance Targets

- **Small datasets (<1K rows)**: <5 seconds end-to-end
- **Medium datasets (1K-10K rows)**: <30 seconds end-to-end
- **Large datasets (10K-100K rows)**: <5 minutes end-to-end
- **UI responsiveness**: <500ms for interactions
- **Memory usage**: <2 GB for 100K rows

---

## 12. Scalability Boundaries

### 12.1 Designed For

- **Dataset size**: Up to 100,000 rows
- **Concurrency**: Single user or <10 concurrent users (local deployment)
- **Throughput**: 100-1,000 records/second (rule-based), 10-100 records/second (NLP)
- **Storage**: <1 GB for application and data

### 12.2 Not Designed For

- **Real-time streaming**: Batch processing only
- **Distributed processing**: Single-machine only
- **Massive datasets**: >100K rows (would require Spark, Dask, or similar)
- **Multi-tenant production**: Authentication and isolation not implemented

### 12.3 Future Scaling Paths

If scaling beyond initial scope:
1. **Horizontal scaling**: Add message queue (RabbitMQ) + worker pool
2. **Distributed processing**: Migrate to Apache Spark or Dask
3. **Persistent storage**: Migrate to PostgreSQL or cloud database
4. **API separation**: Decouple UI from processing (FastAPI + React)

---

## 13. Extensibility Points

### 13.1 Adding New PII Detectors

1. Implement `PIIDetector` interface in `src/detection/`
2. Register in `detector_factory.py`
3. Add configuration in `config/default.yaml`
4. Add tests in `tests/unit/detection/`

### 13.2 Adding New Anonymization Strategies

1. Implement strategy in `src/anonymization/strategies.py`
2. Register in `transformer.py`
3. Add configuration in `config/default.yaml`
4. Add tests

### 13.3 Adding New UI Pages

1. Create page in `src/ui/pages/`
2. Register in `app.py` navigation
3. Use existing UI components for consistency
4. Follow design system

### 13.4 Adding New Experiments

1. Create experiment configuration in `experiments/configs/`
2. Implement experiment script in `experiments/scripts/`
3. Use evaluation framework for metrics
4. Store results in DuckDB

---

## 14. Architecture Decisions

### AD-1: Why Streamlit Instead of React?

**Decision**: Use Streamlit for UI  
**Rationale**:
- Faster development (Python only, no frontend-backend split)
- Suitable for data-centric applications
- Built-in components for charts, tables, forms
- Good enough for portfolio demonstration
**Trade-off**: Less control over UI compared to React, not suitable for complex interactions

### AD-2: Why DuckDB Instead of PostgreSQL?

**Decision**: Use DuckDB for analytical storage  
**Rationale**:
- Local, embedded database (no separate server)
- Optimized for analytics (columnar storage)
- SQL interface for complex queries
- Easy to bundle with application
**Trade-off**: Not suitable for multi-user production, but sufficient for single-user and research purposes

### AD-3: Why Presidio Instead of Custom NLP?

**Decision**: Use Microsoft Presidio for NLP-assisted detection  
**Rationale**:
- Production-ready, well-maintained library
- Supports multiple recognizers (patterns + NLP)
- Configurable and extensible
- Good documentation
**Trade-off**: Adds dependency complexity, but saves development time and provides reliable baseline

### AD-4: Why Separate Evaluation Layer?

**Decision**: Evaluation layer independent of pipeline  
**Rationale**:
- Enables controlled experiments without UI
- Reproducible experimental protocol
- Can run experiments via CLI or notebooks
- Research credibility requires independent evaluation
**Trade-off**: Some code duplication, but worth it for scientific rigor

### AD-5: Why Immutable Data Processing?

**Decision**: Never modify original data, always create new outputs  
**Rationale**:
- Safety: No accidental data corruption
- Reproducibility: Can re-run pipeline
- Auditability: Clear transformation history
- Trust: Users can verify original data unchanged
**Trade-off**: Higher memory usage, but acceptable for dataset sizes in scope

---

## 15. Future Architectural Considerations

### 15.1 API Separation

If API access needed (e.g., for programmatic use or mobile app):
- Implement FastAPI backend
- Expose pipeline as REST API
- Keep Streamlit as one UI option
- Share core modules between API and UI

### 15.2 Multi-User Support

If multi-user production deployment needed:
- Add authentication (OAuth, JWT)
- Session management in database
- User-scoped data isolation
- PostgreSQL instead of DuckDB
- Message queue for background jobs

### 15.3 Model Training

If custom model training added:
- Add ML module (`src/ml/`)
- Training pipeline separate from inference
- Model versioning and registry
- Experiment tracking (MLflow or similar)

---

## 16. Architecture Validation

### 16.1 Quality Attributes

| Attribute | Target | Verification Method |
|-----------|--------|---------------------|
| Modularity | High | Dependency graph, low coupling |
| Testability | High | Unit test coverage >70% |
| Maintainability | High | Code review, documentation coverage |
| Performance | Acceptable | Load testing with 100K rows |
| Security | Good | Security checklist, input validation |
| Privacy | High | Data flow analysis, audit logs |
| Reproducibility | High | Fresh installation test |

### 16.2 Architecture Review Checklist

- [ ] All modules have clear responsibilities
- [ ] No circular dependencies
- [ ] UI independent of business logic
- [ ] Core modules testable without UI
- [ ] Error handling at all layers
- [ ] Logging without PII exposure
- [ ] Configuration externalized
- [ ] Secrets not in code
- [ ] Input validation at entry points
- [ ] Data immutability enforced
- [ ] Evaluation framework independent
- [ ] Database schema normalized
- [ ] Performance targets achievable
- [ ] Deployment options documented

---

**Document Status**: Draft  
**Next Steps**: Review and approval before implementation  
**Dependencies**: Requires approved requirements specification
