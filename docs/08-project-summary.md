# Project Summary
## Privacy-Aware Data Engineering Pipeline

**Version:** 1.0  
**Date:** October 25, 2026  
**Status:** Planning Phase Complete — Ready for Implementation

---

## Executive Summary

The **Privacy-Aware Data Engineering Pipeline** is a research-oriented software portfolio project designed to demonstrate proficiency in data engineering, privacy-preserving data processing, and experimental evaluation. This project serves as a technical portfolio piece for the European Data Science and Intelligent Systems (EDISS) master's program application.

**Core Objective**: Build a local-first, browser-based application that ingests structured datasets, validates data quality, detects personally identifiable information (PII) using both rule-based and NLP-assisted methods, applies privacy transformations, and evaluates detection approaches through reproducible experiments.

**Research Question**: *"How do rule-based and NLP-assisted PII detection methods compare in precision, recall, F1-score, and processing efficiency on a controlled dataset containing structured records and unstructured text?"*

---

## Project Scope

### What This Project Includes

✅ **Complete Data Engineering Pipeline**
- CSV and JSON file ingestion with validation
- Data quality profiling and issue detection
- Schema validation and data cleaning
- End-to-end processing with error handling

✅ **Privacy-Preserving PII Detection**
- Custom rule-based detector (email, phone, SSN, credit card, IP)
- NLP-assisted detection (Microsoft Presidio + spaCy)
- Configurable detection strategies

✅ **Anonymization and Transformation**
- Multiple strategies: masking, redaction, pseudonymization, generalization
- Configurable per PII category
- Transformation audit trails

✅ **Experimental Evaluation Framework**
- Synthetic dataset generation with ground truth
- Precision, recall, F1-score, timing metrics
- Confusion matrices and error analysis
- Reproducible experimental protocol

✅ **Professional Web Interface**
- Streamlit-based multi-page application
- Interactive dashboards and visualizations
- Data upload, processing, and export workflows
- Experiment results presentation

✅ **Research Documentation**
- Comprehensive research report (10-15 pages)
- Methodology, results, discussion, limitations
- Reproducibility instructions
- Architecture and API documentation

### What This Project Excludes

❌ Real-time streaming data processing  
❌ Distributed or cloud-native architecture  
❌ Production-grade multi-user deployment  
❌ GDPR/HIPAA compliance certification  
❌ Machine learning model training  
❌ Multi-language support (English only)  
❌ Advanced features beyond core requirements  

---

## Technology Stack

### Core Technologies
- **Language**: Python 3.11
- **UI Framework**: Streamlit
- **Data Processing**: pandas, NumPy
- **Visualization**: Plotly

### PII Detection
- **Rule-Based**: Custom regex + validation logic
- **NLP-Assisted**: Microsoft Presidio, spaCy (`en_core_web_lg`)

### Data Storage & Analytics
- **Database**: DuckDB (local, embedded, analytical)
- **Temp Storage**: Python `tempfile` module

### Evaluation & Metrics
- **Synthetic Data**: Faker library
- **Metrics**: scikit-learn (precision, recall, F1, confusion matrix)

### Quality & Testing
- **Testing**: pytest, pytest-cov, pytest-mock
- **Linting**: Ruff
- **Validation**: Pandera (optional)
- **Type Hints**: Python typing module

### Development Tools
- **Version Control**: Git, GitHub
- **Environment**: venv (Python virtual environment)
- **Configuration**: YAML, python-dotenv
- **Documentation**: Markdown, docstrings

### Optional (Milestone 12)
- **Containerization**: Docker
- **Deployment**: Streamlit Community Cloud

---

## Architecture Overview

### System Architecture Pattern

**Modular Pipeline Architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────────┐
│         Streamlit UI Layer (Presentation)    │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│        Application Layer (Pipeline)          │
│  Ingest → Profile → Detect → Transform      │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│         Data Layer (DuckDB, Temp Files)      │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│      Evaluation Layer (Experiments, Metrics)  │
└──────────────────────────────────────────────┘
```

### Key Architectural Principles

1. **UI Independence**: Core logic has no Streamlit dependencies
2. **Modular Stages**: Each pipeline stage is independently testable
3. **Clear Contracts**: Defined input/output interfaces using dataclasses
4. **Immutability**: Original data never modified
5. **Error Isolation**: Failures contained within stages

---

## Project Structure

```
Privacy-Aware-Data-Engineering-Pipeline/
├── app.py                    # Streamlit entry point
├── requirements.txt          # Dependencies
├── src/                      # Source code
│   ├── ingestion/           # Data loading
│   ├── validation/          # Quality profiling
│   ├── detection/           # PII detection
│   ├── anonymization/       # Transformations
│   ├── pipeline/            # Orchestration
│   ├── storage/             # DuckDB + temp files
│   ├── evaluation/          # Experiments & metrics
│   ├── ui/                  # Streamlit pages & components
│   └── utils/               # Configuration, logging
├── tests/                    # Test suite
│   ├── unit/                # Unit tests
│   ├── integration/         # Integration tests
│   └── fixtures/            # Test data
├── data/                     # Datasets (mostly not committed)
│   └── samples/             # Sample data (committed)
├── experiments/              # Experiment scripts & configs
│   ├── configs/
│   ├── scripts/
│   └── results/
├── reports/                  # Research report & figures
├── docs/                     # Documentation
└── config/                   # YAML configuration
```

---

## Development Roadmap

### Milestones (8-12 weeks, part-time)

| # | Milestone | Duration | Key Deliverables |
|---|-----------|----------|------------------|
| 0 | Requirements & Specs | 1 week | ✅ All planning documents |
| 1 | Project Foundation | 1 week | Environment, structure, basic app |
| 2 | Data Ingestion | 1 week | CSV/JSON loading, upload page |
| 3 | Data Quality | 1 week | Profiling, quality page |
| 4 | Rule-Based Detection | 1-2 weeks | Custom detectors |
| 5 | NLP Detection | 1-2 weeks | Presidio + spaCy |
| 6 | Anonymization | 1 week | Transformation strategies |
| 7 | Pipeline & Storage | 1 week | Orchestration, DuckDB |
| 8 | Evaluation Framework | 2 weeks | Experiments, metrics |
| 9 | UI Implementation | 2 weeks | All pages, design system |
| 10 | Integration & Hardening | 1 week | Testing, bug fixes |
| 11 | Research Report & Docs | 1-2 weeks | Report, README, screenshots |
| 12 | Packaging & Deployment | 1 week | Docker (optional), deployment (optional) |

**Current Status**: Milestone 0 (Planning) nearing completion

---

## Key Features

### 1. Data Ingestion & Validation
- Support for CSV and JSON files (up to 50 MB, 100K rows)
- Encoding detection and malformed file handling
- Data preview and column inspection
- File validation with clear error messages

### 2. Data Quality Analysis
- Missing value detection (count and percentage)
- Duplicate row identification
- Type inconsistency checking
- Quality score calculation (0-100)
- Optional data cleaning operations

### 3. PII Detection Methods

**Rule-Based Detection:**
- Email addresses (RFC 5322 subset + domain validation)
- Phone numbers (North American + international)
- Social Security Numbers (US format + validation)
- Credit card numbers (pattern + Luhn algorithm)
- IP addresses (IPv4, IPv6)

**NLP-Assisted Detection:**
- Microsoft Presidio analyzer
- spaCy NER model (`en_core_web_lg`)
- Person names, organizations, locations
- Configurable confidence thresholds

### 4. Privacy Transformations
- **Masking**: Replace with mask character (e.g., `***@***.com`)
- **Redaction**: Complete removal or placeholder
- **Pseudonymization**: Consistent HMAC-based hashing
- **Generalization**: Category labels (e.g., `[EMAIL]`)
- Configurable strategy per PII type
- Transformation audit logs

### 5. Experimental Evaluation
- Synthetic dataset generation (Faker library)
- Ground truth annotation
- Precision, recall, F1-score calculation
- Confusion matrices
- Processing time measurement
- Per-category metrics
- Error analysis (false positives/negatives)
- Reproducible experiments (fixed seeds)

### 6. User Interface
- **Home**: Overview and quick start
- **Upload**: File upload with preview
- **Data Quality**: Profiling dashboard
- **PII Detection**: Detection results and configuration
- **Anonymization**: Transformation interface
- **Method Comparison**: Visual comparison charts
- **Experiments**: Detailed evaluation results
- **Settings**: Configuration and history (optional)

### 7. Research & Documentation
- Comprehensive research report
- Methodology and experimental protocol
- Results with figures and tables
- Discussion of trade-offs and limitations
- Reproducibility instructions
- Complete README with setup and usage

---

## Research Contribution

### Research Question
*"How do rule-based and NLP-assisted PII detection methods compare in precision, recall, F1-score, and processing efficiency on a controlled dataset containing structured records and unstructured text?"*

### Hypotheses
1. NLP-assisted method will achieve higher recall
2. Rule-based method will achieve higher precision
3. Rule-based method will be significantly faster
4. Performance will vary by PII category

### Methodology
- **Controlled experiment** with synthetic labeled data
- **Quantitative metrics**: precision, recall, F1, timing
- **Fair comparison**: same data, same evaluation criteria
- **Reproducible protocol**: fixed seeds, versioned dependencies
- **Error analysis**: qualitative insights into failure modes

### Expected Outcomes
- Comparative performance data for both methods
- Insight into precision-recall trade-offs
- Performance vs. accuracy trade-offs
- Guidance for method selection based on use case
- Documentation of limitations and future work

---

## Quality Assurance

### Testing Strategy
- **Unit tests**: >70% coverage for core modules
- **Integration tests**: Full pipeline execution
- **Edge case tests**: Malformed inputs, errors, boundary conditions
- **Evaluation tests**: Metric calculation validation
- **Manual UI testing**: Complete workflows

### Security & Privacy Controls
- No PII in logs, database, or screenshots
- Input validation (file types, sizes, path traversal)
- CSV formula injection protection
- Secure temporary file handling
- Secrets management (environment variables)
- Dependency security (pinned versions)

### Code Quality
- Linting with Ruff (PEP 8 compliance)
- Type hints for public interfaces
- Comprehensive docstrings
- Consistent naming conventions
- Modular, maintainable architecture
- No circular dependencies

### Reproducibility
- Fixed random seeds
- Pinned dependency versions
- Archived evaluation datasets
- Complete setup instructions
- CLI scripts for experiments

---

## Risk Management

### Critical Risks
1. **NLP model compatibility** on Windows → Mitigate: Test early, use fallbacks
2. **Presidio compatibility** with Python 3.11 → Mitigate: Test early, downgrade if needed
3. **PII leakage** in logs/database → Mitigate: Code review, automated tests

### High Priority Risks
- Performance degradation on large datasets
- False positive/negative rates
- Research report incomplete or rushed

### Mitigation Strategy
- Early testing of critical dependencies (Milestone 1)
- Iterative development with testing at each milestone
- Privacy-by-design approach
- Sufficient time allocation for research report (Milestone 11)
- Regular risk reviews throughout development

---

## Success Criteria

### Functional Completeness
✓ All FR-1 through FR-9 requirements implemented  
✓ All pipeline stages functioning end-to-end  
✓ Both detection methods integrated and working  
✓ Experiments runnable and reproducible  
✓ UI complete with all planned pages  

### Quality
✓ Unit tests passing (coverage ≥70% for core)  
✓ Integration tests passing  
✓ No critical bugs  
✓ Code linted and formatted  

### Research Validity
✓ Experiments executed on controlled dataset  
✓ Results measured and documented  
✓ Limitations clearly stated  
✓ Reproducibility instructions provided  
✓ Research report complete (10-15 pages)  

### Documentation
✓ README complete with setup and usage  
✓ Architecture documentation  
✓ Research report with methodology and results  
✓ Inline code documentation  

### Privacy & Security
✓ No raw PII in logs, database, or screenshots  
✓ Input validation implemented  
✓ Secure file handling  
✓ No secrets in source control  

### Reproducibility
✓ Fresh installation on clean Windows succeeds  
✓ All dependencies pinned  
✓ Setup instructions accurate  
✓ Experiments produce consistent results  

---

## Target Audience

### Primary: Master's Program Admission Committees
- Demonstrates technical competence in data engineering
- Shows ability to conduct independent research
- Evidence of software engineering best practices
- Professional portfolio quality

### Secondary: Technical Reviewers & Employers
- Data engineers interested in privacy-aware systems
- Researchers in PII detection and anonymization
- Potential employers evaluating technical skills

### Tertiary: Open Source Community
- Developers learning privacy engineering
- Students building portfolio projects
- Researchers seeking reproducible baselines

---

## Project Values

### Technical Excellence
- Clean, maintainable, well-tested code
- Professional architecture and design
- Evidence-based decision making

### Privacy-First Design
- No real personal data used
- Privacy controls at every layer
- Transparent processing and limitations

### Research Integrity
- No fabricated results or citations
- Honest reporting of limitations
- Reproducible methodology
- Ethical use of data

### Learning and Growth
- Demonstrates ability to learn new technologies
- Shows progression from requirements to implementation
- Documents challenges and solutions

---

## Next Steps

### Immediate (Before Implementation)
1. ✅ Complete all planning documents
2. ⏳ Review and approve specifications
3. ⏳ Resolve any open questions or conflicts
4. ⏳ Prepare development environment

### Milestone 1 (Week 1)
- Set up Python environment and dependencies
- Create project structure
- Test critical dependencies (spaCy, Presidio)
- Implement basic Streamlit application
- Verify configuration and logging work

### Implementation Phase (Weeks 2-10)
- Follow development roadmap sequentially
- Complete one milestone at a time
- Seek approval before proceeding to next milestone
- Maintain clean Git history

### Finalization Phase (Weeks 11-12)
- Run final experiments and analyze results
- Write comprehensive research report
- Complete all documentation
- Test reproducibility on clean environment
- (Optional) Deploy demonstration version

---

## Conclusion

The **Privacy-Aware Data Engineering Pipeline** is a well-planned, technically ambitious, yet achievable portfolio project that demonstrates:

✓ **Data engineering skills**: Pipeline design, data quality, ETL  
✓ **Privacy engineering**: PII detection, anonymization, security controls  
✓ **Software engineering**: Clean architecture, testing, documentation  
✓ **Research skills**: Experimental design, evaluation, reporting  
✓ **Full-stack development**: Backend logic + web UI  

The project is designed to be completed in 8-12 weeks by a solo developer, with clear milestones, realistic scope, and well-defined acceptance criteria. The comprehensive planning phase reduces implementation risks and provides a clear roadmap to success.

**Status**: Planning complete ✅  
**Ready for implementation**: Yes ✅  
**Confidence**: High (with identified risks and mitigations in place)  

---

**Document Version**: 1.0  
**Last Updated**: October 25, 2026  
**Prepared by**: Project Developer  
**Reviewed by**: (Pending review)  

**Approval Status**: ⏳ Awaiting approval to proceed with Milestone 1

---

## Appendix: Planning Documents

All detailed specifications are available in the `docs/` directory:

1. **Requirements Specification** (`01-requirements-specification.md`)
   - Functional, non-functional, research requirements
   - Acceptance criteria and explicit non-goals

2. **Architecture Specification** (`02-architecture-specification.md`)
   - Component responsibilities and data flow
   - Module boundaries and contracts
   - Security architecture and deployment options

3. **UI/UX Specification** (`03-ui-ux-specification.md`)
   - Design system and visual identity
   - Page specifications and workflows
   - Component library and interaction patterns

4. **Data & Research Specification** (`04-data-research-specification.md`)
   - Data formats and PII categories
   - Experimental design and evaluation metrics
   - Dataset generation and reproducibility requirements

5. **Development Roadmap** (`05-development-roadmap.md`)
   - 12 detailed milestones with tasks and acceptance criteria
   - Dependency management and verification commands
   - Implementation workflow and Git strategy

6. **Risk Register** (`06-risk-register.md`)
   - Technical, deployment, research, security, and project management risks
   - Mitigation strategies and contingency plans
   - Risk monitoring plan

7. **File & Module Plan** (`07-file-module-plan.md`)
   - Complete directory structure
   - Module responsibilities and dependencies
   - Naming conventions and coding standards
   - Configuration and testing strategies

8. **Project Summary** (`08-project-summary.md`)
   - This document: high-level overview and synthesis

---

**Ready to begin implementation!** 🚀
