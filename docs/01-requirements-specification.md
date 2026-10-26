# Requirements Specification
## Privacy-Aware Data Engineering Pipeline

**Version:** 1.0  
**Date:** October 25, 2026  
**Project Type:** Research-Oriented Master's Portfolio Project

---

## 1. Project Overview

### 1.1 Purpose
Design and implement a local-first, browser-based application that demonstrates:
- Robust data engineering pipeline design
- Privacy-preserving data processing
- PII detection using multiple approaches
- Reproducible experimental evaluation
- Professional software development practices

### 1.2 Target Audience
- Technical reviewers and potential employers
- Data engineering and privacy engineering professionals
- Open source community
- The developer (for learning and portfolio demonstration)

### 1.3 Success Criteria
- Functioning end-to-end data pipeline with clear stages
- Measurable comparison of PII detection methods using controlled experiments
- Professional, polished user interface
- Comprehensive documentation and reproducible setup
- Clean, maintainable, testable codebase
- Evidence of privacy-aware design decisions

---

## 2. Functional Requirements

### FR-1: Data Ingestion

**FR-1.1** The system SHALL accept CSV file uploads with the following constraints:
- Maximum file size: 50 MB (configurable)
- Maximum rows: 100,000 rows (configurable)
- Encoding detection and UTF-8 handling
- Delimiter detection or configuration
- Header row detection

**FR-1.2** The system SHALL accept JSON file uploads with the following structure:
- Array of objects (records)
- Single-level or nested objects with configurable flattening
- Maximum file size: 50 MB (configurable)

**FR-1.3** The system SHALL validate uploaded files:
- File type verification
- Encoding validation
- Malformed file detection
- Empty file detection
- Column name validation (no duplicates, non-empty)

**FR-1.4** The system SHALL provide upload preview:
- First 100 rows display
- Column names and inferred types
- Row and column counts
- File size and encoding information
- Basic statistics (missing values per column)

**FR-1.5** The system SHALL handle upload errors gracefully:
- Clear error messages for malformed files
- Encoding errors with suggested fixes
- File size violations
- Unsupported formats

**FR-1.6** The system SHALL NOT:
- Execute or evaluate file contents as code
- Accept executable file types
- Trust file contents as instructions
- Persist raw uploads indefinitely

### FR-2: Data Quality Profiling and Validation

**FR-2.1** The system SHALL detect and report data quality issues:
- Missing values (count and percentage per column)
- Duplicate rows (exact and configurable key-based)
- Duplicate column names
- Type inconsistencies within columns
- Invalid email formats (basic RFC-compliant pattern)
- Invalid phone number patterns (configurable by region)
- Out-of-range values (when ranges configured)
- Empty columns (all NULL or empty string)
- Constant columns (single unique value)
- High-cardinality columns (potential identifiers)

**FR-2.2** The system SHALL generate data quality summary:
- Overall quality score or rating
- Issue counts by severity (error, warning, info)
- Column-level quality metrics
- Recommendations for cleaning

**FR-2.3** The system SHALL provide configurable validation rules:
- Schema definition (column names, types, nullable)
- Range constraints (min, max for numeric)
- Pattern constraints (regex for strings)
- Uniqueness constraints
- Custom validation expressions

**FR-2.4** The system SHALL support explicit data cleaning operations:
- Remove duplicate rows (with confirmation)
- Fill missing values (with strategy selection)
- Drop columns (with confirmation)
- Type conversion (with validation)
- Before/after comparison reports

**FR-2.5** The system SHALL maintain data lineage:
- Record of all transformations applied
- Timestamps and operation types
- Row counts before/after each operation
- No silent data modification

### FR-3: Rule-Based PII Detection

**FR-3.1** The system SHALL implement a custom rule-based detector for:
- Email addresses (RFC 5322 subset pattern)
- Phone numbers (North American and international formats)
- IP addresses (IPv4 and basic IPv6)
- Credit card numbers (Luhn algorithm validation)
- Social Security Numbers (US format with validation)

**FR-3.2** The detector SHALL apply contextual validation:
- Email: DNS-like domain structure
- Phone: digit count and format validation
- Credit card: Luhn checksum
- SSN: basic format validation

**FR-3.3** The detector SHALL produce structured results:
- PII category/type
- Column name and row index
- Text span (start, end positions for unstructured text)
- Matched value (optionally redacted in logs)
- Confidence score (0.0-1.0, where rule-based = 1.0 for valid matches)

**FR-3.4** The detector SHALL be independently testable:
- Unit tests with known positive/negative cases
- Performance tests (throughput)
- No UI dependencies

**FR-3.5** The detector SHALL support configuration:
- Enable/disable specific PII categories
- Adjust validation strictness
- Custom patterns (advanced users)

### FR-4: NLP-Assisted PII Detection

**FR-4.1** The system SHALL integrate Microsoft Presidio for PII analysis:
- Presidio Analyzer for entity recognition
- Presidio Anonymizer for transformation
- Configurable recognizers

**FR-4.2** The system SHALL use an appropriate NLP model:
- spaCy `en_core_web_lg` or compatible model
- Offline operation after initial download
- Named Entity Recognition (NER) for PERSON, ORG, GPE, DATE

**FR-4.3** The system SHALL configure Presidio recognizers:
- Pattern-based recognizers (for fair comparison, these must be excluded from "NLP-assisted" evaluation)
- NER-based recognizers (actual NLP component)
- Custom recognizers where appropriate
- Confidence thresholds (default: 0.5)

**FR-4.4** The system SHALL clearly distinguish detection methods:
- Rule-based: custom detector using regex + validation
- NLP-assisted: Presidio with NER model for named entities
- Method labels must accurately reflect the underlying mechanism

**FR-4.5** The system SHALL handle NLP errors gracefully:
- Model not found/not downloaded
- Model loading failures
- Timeout on large datasets
- Fallback to rule-based detection with warning

**FR-4.6** The integration SHALL support:
- Entity confidence scoring
- Entity type mapping to PII categories
- Batch processing for performance
- Memory-efficient processing of large texts

### FR-5: PII Review and Anonymization

**FR-5.1** The system SHALL provide multiple transformation strategies:
- **Masking**: Replace with fixed-length mask (e.g., "***@***.***")
- **Redaction**: Remove entirely or replace with placeholder ("[REDACTED]")
- **Pseudonymization**: Consistent replacement using HMAC-based hashing
- **Generalization**: Replace with category (e.g., "[EMAIL]", "[PHONE]")

**FR-5.2** Transformation configuration:
- Strategy selection per PII category
- Global or column-specific settings
- Preview transformations before applying
- Undo/rollback capability (through pipeline re-execution)

**FR-5.3** The system SHALL handle edge cases:
- Overlapping PII detections (choose highest confidence)
- Repeated identifiers (consistent pseudonymization)
- NULL/missing values (preserve)
- Partial matches (handle gracefully)
- Multiple PII types in single field

**FR-5.4** The system SHALL maintain transformation audit:
- Count of transformations by category and strategy
- Columns affected
- Rows affected
- Timestamp of transformation
- Method used (rule-based vs. NLP)
- **Do not log original sensitive values**

**FR-5.5** The system SHALL preserve data utility:
- Maintain data types where possible
- Preserve non-sensitive information
- Maintain referential consistency for pseudonymization
- Document impact on data utility

**FR-5.6** Terminology accuracy:
- **Masking**: Obscuring with visible pattern (reversible with key)
- **Redaction**: Complete removal (irreversible)
- **Pseudonymization**: Deterministic replacement (reversible with key, consistent)
- **Anonymization**: Irreversible removal of identifiability (not guaranteed by simple masking)

### FR-6: Pipeline Orchestration and Storage

**FR-6.1** The system SHALL implement a modular pipeline with stages:
1. **Ingestion**: Load and validate file
2. **Profiling**: Generate data quality report
3. **Validation**: Apply schema and constraint checks
4. **Detection**: Run configured PII detectors
5. **Transformation**: Apply anonymization strategies
6. **Post-validation**: Re-check quality and constraints
7. **Storage**: Persist results and metadata
8. **Reporting**: Generate processing summary

**FR-6.2** Each pipeline stage SHALL:
- Have clear input/output contracts (dataclasses or TypedDict)
- Handle errors without corrupting data
- Log stage execution (start, end, duration, status)
- Return structured results
- Be testable independently

**FR-6.3** The system SHALL use DuckDB for analytical storage:
- **datasets** table: metadata (id, name, upload_date, row_count, column_count, file_hash)
- **processing_runs** table: execution metadata (run_id, dataset_id, timestamp, status, duration, method)
- **quality_metrics** table: profiling results per run
- **pii_detections** table: aggregated detection statistics (not raw PII values)
- **evaluation_results** table: experiment metrics

**FR-6.4** Database schema design:
- Use UUID or timestamp-based run identifiers
- Foreign key relationships for referential integrity
- Indexed columns for query performance
- No raw sensitive data in database
- Configurable retention policy

**FR-6.5** Session and concurrency management:
- Streamlit session state isolation
- Unique run identifiers per pipeline execution
- Safe temporary file handling (using `tempfile` module)
- Cleanup of temporary files after processing
- Handle concurrent Streamlit sessions safely

**FR-6.6** Error handling and recovery:
- Atomic stage execution (rollback on failure)
- Partial failure reporting
- Detailed error messages
- Pipeline restart capability
- Maintain database consistency

**FR-6.7** Data lifecycle:
- Original uploaded files: session-scoped, deleted after processing
- Processed datasets: optionally persist in DuckDB or export
- Temporary processing artifacts: cleaned up automatically
- Database: configurable retention (default: keep 50 most recent runs)

### FR-7: Experimental Evaluation Framework

**FR-7.1** The system SHALL support controlled experiments comparing:
- **Method A**: Custom rule-based detector
- **Method B**: NLP-assisted detector (Presidio with NER)

**FR-7.2** Synthetic dataset generation:
- Use Faker library for realistic PII generation
- Generate positive examples (containing PII)
- Generate negative examples (no PII, but similar structure)
- Include edge cases: malformed PII, ambiguous text, noise
- Generate 1,000-10,000 records (configurable)
- Create structured (CSV) and unstructured (text) test cases

**FR-7.3** Ground truth annotation:
- Programmatic labeling during generation
- Label format: (text, start, end, category)
- Store in JSON format for reproducibility
- Include metadata (generation date, version, configuration)

**FR-7.4** Evaluation protocol:
- Fixed evaluation dataset (consistent across method comparisons)
- Reproducible random seed
- Separate train/dev/test only if method tuning occurs
- For rule-based methods: no training, only test set evaluation
- Fair comparison: same input data, same evaluation criteria

**FR-7.5** Evaluation metrics:
- **Precision**: TP / (TP + FP) — How many detected PII are correct?
- **Recall**: TP / (TP + FN) — How many actual PII were detected?
- **F1-Score**: Harmonic mean of precision and recall
- **Per-category metrics**: Precision, recall, F1 for each PII type
- **Macro-averaging**: Equal weight to each category
- **Micro-averaging**: Aggregate TP, FP, FN across categories
- **Processing time**: Total and per-record
- **Throughput**: Records per second

**FR-7.6** Matching rules:
- **Entity-level matching**: Exact span and category match
- **Partial matching**: Optional relaxed overlap criterion (e.g., IoU ≥ 0.5)
- **Category matching**: Must match ground truth category exactly
- **Case sensitivity**: Normalize during comparison
- **Handling multiple predictions**: Best match by confidence

**FR-7.7** Experiment execution:
- Warm-up run for NLP model loading (excluded from timing)
- Multiple independent runs (3-5) for timing stability
- Measure prediction time only (exclude I/O and setup)
- Record system information (Python version, library versions, CPU)

**FR-7.8** Results storage and reporting:
- Confusion matrix per method
- Classification report (sklearn format)
- Timing statistics (mean, std dev, min, max)
- Export results to JSON and CSV
- Comparison charts (precision/recall/F1 bar charts)
- Error analysis: FP and FN examples

**FR-7.9** Reproducibility requirements:
- Fixed random seeds
- Versioned dependencies (pinned in requirements.txt)
- Documented experiment configuration
- Archived evaluation datasets
- Runnable experiment scripts (CLI interface)

**FR-7.10** Limitations and validity:
- Clearly document that synthetic data may not reflect real-world PII
- Acknowledge potential bias in dataset generation
- Explain that results depend on specific model versions and configurations
- Note that evaluation measures detection, not downstream utility preservation

### FR-8: User Interface and Dashboard

**FR-8.1** The system SHALL provide a Streamlit-based web interface with pages:
1. **Home/Overview**: Introduction, feature summary, quick start
2. **Upload Dataset**: File upload with preview and validation
3. **Data Quality**: Profiling results, validation reports, cleaning options
4. **PII Detection**: Detection results, category distribution, confidence analysis
5. **Anonymization**: Transformation configuration, preview, application, audit
6. **Method Comparison**: Visual comparison of rule-based vs. NLP methods
7. **Experiment Results**: Detailed evaluation metrics, charts, error analysis
8. **Settings/History**: (Optional) Configuration, run history, database management

**FR-8.2** Navigation and layout:
- Sidebar navigation with clear page labels
- Consistent header and branding
- Breadcrumb or progress indicator for multi-step workflows
- Responsive layout (optimized for 1280px+ width)

**FR-8.3** Data visualizations:
- Data quality: Bar charts for missing values, issue type distribution
- PII detection: Stacked bar charts by category, heatmaps by column
- Method comparison: Side-by-side bar charts (precision, recall, F1)
- Timing comparison: Horizontal bar charts or box plots
- Confusion matrices: Heatmaps with annotations
- All charts interactive using Plotly

**FR-8.4** Data tables:
- Paginated tables for large datasets
- Sortable columns
- Filtering and search where appropriate
- Highlighted PII (with redaction for privacy)
- Export buttons (CSV, JSON)

**FR-8.5** User feedback and state management:
- Loading spinners for long operations
- Progress bars for multi-stage processing
- Success messages (green)
- Warning messages (yellow)
- Error messages (red)
- Empty states with helpful guidance
- Contextual help tooltips

**FR-8.6** Download capabilities:
- Processed dataset (CSV or JSON)
- Data quality report (JSON)
- PII detection report (JSON)
- Transformation audit (CSV)
- Experiment results (JSON, CSV)
- Charts as PNG (via Plotly)

**FR-8.7** Accessibility and usability:
- Sufficient color contrast (WCAG AA)
- Meaningful labels and alt text
- Keyboard navigation support (Streamlit default)
- Clear error messages with actionable guidance
- Minimal cognitive load (one primary action per page)

### FR-9: Documentation and Reporting

**FR-9.1** The system SHALL generate processing reports including:
- Dataset summary (rows, columns, size)
- Data quality score and issues
- PII detection summary (counts by category and method)
- Transformation summary (strategy and counts)
- Processing duration and timestamp
- Warnings and errors
- Downloadable as JSON

**FR-9.2** The system SHALL generate experiment reports including:
- Dataset description and size
- Method configurations
- Evaluation metrics table
- Confusion matrices
- Error analysis (sample FPs and FNs)
- Timing statistics
- Reproducibility information
- Downloadable as JSON and PDF (if feasible)

**FR-9.3** The system SHALL maintain processing history:
- List of past processing runs
- Run metadata (date, dataset, method, status)
- Ability to view past results
- Optional: Delete old runs

---

## 3. Non-Functional Requirements

### NFR-1: Performance

**NFR-1.1** The system SHALL process datasets within acceptable time limits:
- Small datasets (<1,000 rows): <5 seconds
- Medium datasets (1,000-10,000 rows): <30 seconds
- Large datasets (10,000-100,000 rows): <5 minutes

**NFR-1.2** The UI SHALL remain responsive:
- Page load time: <2 seconds
- User interactions: <500ms feedback
- Long operations: Background processing with progress indication

**NFR-1.3** Memory efficiency:
- Maximum memory usage: <2 GB for 100K row dataset
- Streaming or batch processing for large files
- Proper cleanup of temporary objects

### NFR-2: Reliability

**NFR-2.1** Error handling:
- No silent failures
- No data corruption
- Graceful degradation when components fail
- Automatic cleanup of partial results

**NFR-2.2** Data integrity:
- Original data never modified
- Transformations always create new outputs
- Database transactions for consistency
- Checksums for file integrity

### NFR-3: Maintainability

**NFR-3.1** Code quality:
- Modular architecture with clear separation of concerns
- Functions <50 lines (guideline, not strict rule)
- Modules <500 lines (guideline)
- Type hints for public functions and important data structures
- Docstrings for modules, classes, and public functions
- No circular imports
- Consistent naming conventions (PEP 8)

**NFR-3.2** Testing:
- Unit test coverage >70% for core modules
- Integration tests for pipeline execution
- Edge case tests for error handling
- Evaluation tests for metric calculations

**NFR-3.3** Documentation:
- README with setup and usage instructions
- Architecture documentation (this document)
- Inline code comments for complex logic
- Research report with methodology and results

### NFR-4: Portability

**NFR-4.1** Platform support:
- Primary: Windows 10/11
- Secondary: macOS, Linux (via compatible dependencies)
- Python 3.11+ (or 3.10+ if 3.11 has compatibility issues)

**NFR-4.2** Deployment:
- Local execution without external services
- Optional: Streamlit Community Cloud deployment
- Optional: Docker containerization
- No platform-specific code in core modules (use pathlib, os.path)

### NFR-5: Security and Privacy

**NFR-5.1** Input validation:
- File type whitelist
- File size limits
- Path traversal protection
- No code execution from uploads
- CSV formula injection protection on export

**NFR-5.2** Data protection:
- No raw PII in logs
- No raw PII in screenshots or documentation
- No raw PII in database (only aggregated statistics)
- Secure temporary file handling (`tempfile` module)
- Automatic cleanup of uploaded files

**NFR-5.3** Secrets management:
- No hardcoded credentials
- Use environment variables for configuration
- `.env` file for local development (not committed)
- `.streamlit/secrets.toml` for Streamlit deployment (not committed)

**NFR-5.4** Dependency security:
- Pinned dependency versions
- Regular security updates
- No known vulnerabilities in dependencies
- Minimal dependency footprint

### NFR-6: Usability

**NFR-6.1** Ease of use:
- Intuitive workflow (clear next steps)
- Minimal configuration required for basic usage
- Helpful error messages
- Contextual help and tooltips
- Sample datasets provided

**NFR-6.2** Professional appearance:
- Consistent visual design
- Clean, uncluttered layouts
- Appropriate use of color and typography
- Professional branding (project name, logo if designed)

---

## 4. Research Requirements

### RR-1: Research Question

**Primary Research Question:**
"How do rule-based and NLP-assisted PII detection methods compare in precision, recall, F1-score, and processing efficiency on a controlled dataset containing structured records and unstructured text?"

**Secondary Questions:**
- Which method produces more false positives?
- Which method is more suitable for high-recall requirements?
- What is the performance trade-off between accuracy and speed?
- How do methods differ across PII categories?

### RR-2: Methodology Requirements

**RR-2.1** Experimental design:
- Comparative evaluation (Method A vs. Method B)
- Quantitative metrics (precision, recall, F1, timing)
- Controlled dataset with ground truth
- Reproducible protocol
- Statistical reporting (mean, std dev for timing)

**RR-2.2** Baseline and comparison:
- **Baseline**: Custom rule-based detector
- **Comparison**: NLP-assisted detector (Presidio + NER)
- Fair comparison: same data, same evaluation criteria, same PII categories

**RR-2.3** Dataset requirements:
- Synthetic data with known ground truth
- Diverse PII categories
- Realistic and adversarial examples
- Sufficient size for statistical validity (≥1,000 examples)

**RR-2.4** Limitations and threats to validity:
- Synthetic data may not generalize to real-world data
- Evaluation limited to supported PII categories
- Method performance depends on specific configurations and model versions
- No guarantee of generalization to other languages or domains

### RR-3: Documentation Requirements

**RR-3.1** Research report SHALL include:
1. **Introduction**: Problem statement, motivation, scope
2. **Background**: Related work, PII detection approaches, privacy concerns
3. **Methodology**: System architecture, detection methods, dataset generation, evaluation protocol
4. **Results**: Metrics tables, charts, confusion matrices
5. **Discussion**: Interpretation, comparison, limitations
6. **Conclusion**: Summary, implications, future work
7. **References**: Cited documentation and scholarly work

**RR-3.2** Reproducibility documentation:
- Experiment configuration files
- Dataset generation scripts
- Evaluation scripts with CLI interface
- Dependency versions
- Random seeds
- Instructions to replicate experiments

**RR-3.3** Ethical considerations:
- No real personal data used in experiments
- Synthetic data generation methodology disclosed
- Limitations of automated PII detection clearly stated
- No claim of GDPR or regulatory compliance without legal review

---

## 5. Security and Privacy Requirements

### SPR-1: Input Security

**SPR-1.1** File upload validation:
- Whitelist: `.csv`, `.json` only
- Maximum file size: 50 MB (configurable)
- Reject executable file types
- Reject files with suspicious extensions

**SPR-1.2** File parsing security:
- Use safe CSV parsing (pandas with error handling)
- Use safe JSON parsing (`json.loads`, no `eval`)
- Handle malformed files without code execution
- Protect against CSV formula injection on export (prefix `=`, `+`, `-`, `@` with `'`)

**SPR-1.3** Path security:
- Use `tempfile` module for temporary files
- Validate filenames (no path traversal characters)
- Restrict file operations to designated directories
- No user-controlled file paths for system operations

### SPR-2: Data Privacy

**SPR-2.1** PII handling in logs:
- Never log full PII values
- Log PII categories and counts only
- Redact or mask PII in exception messages
- No PII in debug output

**SPR-2.2** PII handling in database:
- Store only aggregated detection statistics
- Store transformation counts, not original values
- Use hashed identifiers where necessary
- No raw PII persistence

**SPR-2.3** PII handling in UI:
- Redact or mask PII in previews (optional, user-configurable)
- Warn users before displaying raw data
- No PII in screenshots or documentation

**SPR-2.4** Data retention:
- Uploaded files: deleted after processing (within session)
- Temporary files: cleaned up automatically
- Processed results: user-controlled export
- Database: configurable retention policy

### SPR-3: Access Control

**SPR-3.1** Local application:
- No authentication required (local-only deployment)
- For public deployment: use Streamlit authentication or restrict access
- No public upload of sensitive data recommended

**SPR-3.2** Deployment security:
- HTTPS for any public deployment
- Environment variables for secrets
- No secrets in source code or version control

### SPR-4: Dependency Security

**SPR-4.1** Dependency management:
- Pin all dependencies with exact versions
- Regular security audits (`pip-audit` or similar)
- No dependencies with known high-severity vulnerabilities
- Minimal dependency footprint

---

## 6. Explicit Non-Goals

The following are explicitly OUT OF SCOPE for this project:

**NG-1: Advanced Architecture**
- ❌ Microservices architecture
- ❌ Message queues (Kafka, RabbitMQ)
- ❌ Distributed processing (Spark, Dask)
- ❌ Container orchestration (Kubernetes)
- ❌ Separate API server (FastAPI, Flask separate from UI)

**NG-2: Real-Time and Scalability**
- ❌ Real-time streaming data processing
- ❌ Multi-user production deployment with authentication
- ❌ Horizontal scaling
- ❌ Dataset size >100K rows

**NG-3: Advanced Features**
- ❌ Machine learning model training (use pre-trained models only)
- ❌ Deep learning PII detection
- ❌ Multi-language support (English only)
- ❌ Advanced NLP (sentiment, topic modeling)
- ❌ Data versioning and lineage tracking (beyond basic audit)

**NG-4: Compliance Certification**
- ❌ GDPR compliance certification
- ❌ HIPAA compliance
- ❌ Legal review or attestation
- ❌ Formal privacy impact assessment (beyond design documentation)

**NG-5: Production Operations**
- ❌ Production monitoring and alerting
- ❌ High availability
- ❌ Disaster recovery
- ❌ Multi-region deployment
- ❌ Commercial SLA guarantees

---

## 7. Acceptance Criteria

### AC-1: Functional Completeness
- [ ] All FR-1 through FR-9 requirements implemented
- [ ] All pipeline stages functioning end-to-end
- [ ] Both detection methods integrated and working
- [ ] Experiments runnable and reproducible
- [ ] UI complete with all planned pages

### AC-2: Quality
- [ ] Unit tests passing (coverage ≥70% for core modules)
- [ ] Integration tests passing
- [ ] No critical bugs
- [ ] Code linted (Ruff or equivalent)
- [ ] Type hints for public interfaces

### AC-3: Research Validity
- [ ] Experiments executed on controlled dataset
- [ ] Results measured and documented
- [ ] Limitations clearly stated
- [ ] Reproducibility instructions provided
- [ ] Research report complete

### AC-4: Usability
- [ ] Professional, polished UI
- [ ] Clear workflows and navigation
- [ ] Helpful error messages
- [ ] Sample datasets provided
- [ ] Setup instructions tested on clean Windows environment

### AC-5: Documentation
- [ ] README complete with setup, usage, results
- [ ] Architecture documentation
- [ ] Research report
- [ ] Inline code documentation
- [ ] API/module documentation (docstrings)

### AC-6: Privacy and Security
- [ ] No raw PII in logs, database, or screenshots
- [ ] Input validation implemented
- [ ] Secure temporary file handling
- [ ] No secrets in source control
- [ ] CSV formula injection protection

### AC-7: Reproducibility
- [ ] Fresh installation on clean Windows environment succeeds
- [ ] All dependencies pinned
- [ ] Setup instructions accurate
- [ ] Sample datasets work
- [ ] Experiments produce consistent results with fixed seeds

---

## 8. Assumptions

**A-1: Environment**
- User has Windows 10/11 with administrator privileges for Python installation
- User has Python 3.10 or 3.11 installed or can install it
- User has internet connection for initial dependency and model downloads

**A-2: Data**
- Input datasets are CSV or JSON files
- Datasets are in English
- PII categories align with common North American formats (SSN, phone, email, etc.)
- Datasets fit in memory (with 8GB+ RAM recommended for 100K rows)

**A-3: Usage**
- Application used for demonstration and research purposes
- Not intended for production use with real sensitive data (without additional security review)
- Local-only deployment initially (public deployment is optional)

**A-4: Technical**
- NLP model (spaCy) can be downloaded and loaded successfully
- Presidio compatible with selected Python version
- DuckDB stable and compatible on Windows

---

## 9. Open Questions and Decisions

### Resolved Decisions
- **Technology stack**: Approved as specified (Python, Streamlit, pandas, DuckDB, Presidio, spaCy)
- **Research question**: Approved as specified

### Unresolved Questions
- **Python version**: Use 3.11 or 3.10? (Recommendation: 3.11 unless compatibility issues arise)
- **spaCy model size**: Use `en_core_web_lg` (large, 560MB) or `en_core_web_md` (medium, 40MB)? (Recommendation: lg for better accuracy)
- **Pseudonymization key management**: Store keys in session state or environment variable? (Recommendation: session state for local use, env var for reproducibility)
- **Docker priority**: Build Docker image in Milestone 12 or defer? (Recommendation: Milestone 12, optional)
- **Deployment target**: Streamlit Community Cloud, Hugging Face Spaces, or local only? (Recommendation: Streamlit Community Cloud, optional)

---

## 10. Constraints

### Technical Constraints
- **Platform**: Windows development environment (use cross-platform libraries)
- **Language**: Python only (no JavaScript, Rust, etc.)
- **UI framework**: Streamlit (no React, Vue, etc.)
- **Database**: DuckDB for analytics (no PostgreSQL, MySQL initially)
- **Deployment**: Local-first (cloud deployment optional)

### Resource Constraints
- **Development time**: Solo developer, manageable milestones
- **Memory**: <2GB for typical dataset processing
- **Storage**: <1GB for application, dependencies, and sample data
- **Complexity**: Maintainable by single developer, explainable in interview

### Domain Constraints
- **Language**: English only
- **PII types**: Limited to high-confidence, pattern-based categories
- **Geography**: North American formats prioritized (SSN, US phone numbers)

---

## 11. Dependencies on External Systems

### Required External Dependencies
- **Python Package Index (PyPI)**: For dependency installation
- **spaCy model repository**: For downloading NLP model
- **Internet access**: One-time for setup, then offline capable

### Optional External Dependencies
- **GitHub**: For version control and portfolio hosting
- **Streamlit Community Cloud**: For optional public deployment
- **Docker Hub**: For optional container distribution

---

## 12. Risk Register (Summary)

*Detailed risk register provided in separate document.*

### High Priority Risks
- **R-1**: NLP model compatibility issues on Windows
- **R-2**: Presidio version compatibility with Python 3.11
- **R-5**: Performance degradation on large datasets
- **R-11**: CSV formula injection on export

### Medium Priority Risks
- **R-3**: DuckDB file locking in multi-session scenarios
- **R-6**: False positive rate too high
- **R-8**: Memory consumption exceeds 2GB

### Low Priority Risks
- **R-9**: Deployment limitations on Streamlit Community Cloud
- **R-12**: Documentation becomes outdated

---

**Document Status**: Draft  
**Next Review**: After architecture specification approval  
**Owner**: Project Developer
