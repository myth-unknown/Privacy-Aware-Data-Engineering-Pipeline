# Privacy-Aware Data Engineering Pipeline

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-planning-yellow.svg)](docs/05-development-roadmap.md)

**A research-oriented data engineering and privacy preservation system with experimental PII detection comparison.**

This project demonstrates data engineering capabilities, privacy-aware data processing, and reproducible research methodology. Built as a technical portfolio piece for the European Data Science and Intelligent Systems (EDISS) master's program application.

---

## 📋 Project Overview

The Privacy-Aware Data Engineering Pipeline is a local-first, browser-based application that:

- ✅ Ingests and validates structured datasets (CSV, JSON)
- ✅ Profiles data quality and detects issues
- ✅ Detects personally identifiable information (PII) using:
  - Rule-based methods (regex + validation)
  - NLP-assisted methods (Microsoft Presidio + spaCy)
- ✅ Applies privacy-preserving transformations (masking, redaction, pseudonymization)
- ✅ Evaluates detection methods through controlled experiments
- ✅ Presents results through professional web interface

**Research Question**: *How do rule-based and NLP-assisted PII detection methods compare in precision, recall, F1-score, and processing efficiency?*

---

## 🎯 Key Features

### Data Engineering Pipeline
- CSV and JSON file ingestion with validation
- Data quality profiling (missing values, duplicates, type issues)
- Schema validation and optional data cleaning
- End-to-end processing with error handling

### PII Detection
- **Rule-Based**: Email, phone, SSN, credit card, IP address
- **NLP-Assisted**: Named entities (person, organization) via Presidio + spaCy
- Configurable detection strategies and confidence thresholds

### Privacy Transformations
- Masking (replace with `***`)
- Redaction (complete removal)
- Pseudonymization (consistent HMAC-based hashing)
- Generalization (category labels)
- Per-category configuration
- Transformation audit trails

### Experimental Evaluation
- Synthetic dataset generation with ground truth
- Precision, recall, F1-score metrics
- Confusion matrices and error analysis
- Processing time comparison
- Reproducible experiments (fixed seeds)

### Professional Web Interface
- Multi-page Streamlit application
- Interactive dashboards and visualizations
- Upload, process, and export workflows
- Method comparison charts
- Experiment results presentation

---

## 🚀 Quick Start

> **Note**: This project is currently in the planning phase. Installation and usage instructions will be available after Milestone 1 completion.

### Prerequisites
- Python 3.11 or later
- Windows 10/11 (primary target), macOS, or Linux
- 8GB RAM recommended
- 2GB free disk space

### Installation (After Milestone 1)

```powershell
# 1. Clone repository
git clone https://github.com/myth-unknown/Privacy-Aware-Data-Engineering-Pipeline.git
cd Privacy-Aware-Data-Engineering-Pipeline

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 4. Install dependencies
pip install -r requirements.txt

# 5. Download spaCy NLP model
python -m spacy download en_core_web_lg

# 6. Run tests to verify setup
pytest tests/

# 7. Launch application
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`.

---

## 📚 Documentation

### Planning Documents (Milestone 0)
All detailed specifications are in the `docs/` directory:

- **[Project Summary](docs/08-project-summary.md)**: High-level overview
- **[Requirements Specification](docs/01-requirements-specification.md)**: Functional and non-functional requirements
- **[Architecture Specification](docs/02-architecture-specification.md)**: System design and component interactions
- **[UI/UX Specification](docs/03-ui-ux-specification.md)**: Design system and user workflows
- **[Data & Research Specification](docs/04-data-research-specification.md)**: Experimental design and evaluation methodology
- **[Development Roadmap](docs/05-development-roadmap.md)**: 12 milestones with detailed tasks
- **[Risk Register](docs/06-risk-register.md)**: Identified risks and mitigation strategies
- **[File & Module Plan](docs/07-file-module-plan.md)**: Project structure and coding standards

### Implementation Documentation (Coming in Milestones 1-12)
- **Architecture Guide**: Detailed component documentation
- **API Reference**: Module and function documentation
- **Research Report**: Experimental methodology and results
- **User Guide**: Step-by-step usage instructions
- **Deployment Guide**: Docker and cloud deployment (optional)

---

## 🏗️ Project Structure

```
Privacy-Aware-Data-Engineering-Pipeline/
├── app.py                    # Streamlit application entry point
├── requirements.txt          # Python dependencies
├── src/                      # Source code
│   ├── ingestion/           # Data loading and validation
│   ├── validation/          # Data quality profiling
│   ├── detection/           # PII detection (rule-based + NLP)
│   ├── anonymization/       # Privacy transformations
│   ├── pipeline/            # Pipeline orchestration
│   ├── storage/             # DuckDB and temporary file management
│   ├── evaluation/          # Experiments and metrics
│   ├── ui/                  # Streamlit pages and components
│   └── utils/               # Configuration and logging
├── tests/                    # Test suite (unit + integration)
├── data/                     # Datasets (not committed except samples)
├── experiments/              # Experiment scripts and configs
├── reports/                  # Research report and figures
├── docs/                     # Documentation
└── config/                   # YAML configuration files
```

---

## 🛠️ Technology Stack

- **Language**: Python 3.11
- **UI**: Streamlit, Plotly
- **Data**: pandas, NumPy
- **PII Detection**: Microsoft Presidio, spaCy
- **Storage**: DuckDB
- **Evaluation**: Faker, scikit-learn
- **Testing**: pytest, pytest-cov
- **Code Quality**: Ruff

---

## 📊 Development Status

| Milestone | Status | Completion |
|-----------|--------|------------|
| 0. Requirements & Specifications | ✅ Complete | 100% |
| 1. Project Foundation | ⏳ Not Started | 0% |
| 2. Data Ingestion | ⏳ Not Started | 0% |
| 3. Data Quality | ⏳ Not Started | 0% |
| 4. Rule-Based Detection | ⏳ Not Started | 0% |
| 5. NLP Detection | ⏳ Not Started | 0% |
| 6. Anonymization | ⏳ Not Started | 0% |
| 7. Pipeline & Storage | ⏳ Not Started | 0% |
| 8. Evaluation Framework | ⏳ Not Started | 0% |
| 9. UI Implementation | ⏳ Not Started | 0% |
| 10. Integration & Hardening | ⏳ Not Started | 0% |
| 11. Research Report & Docs | ⏳ Not Started | 0% |
| 12. Packaging & Deployment | ⏳ Not Started | 0% |

**Current Phase**: Planning Complete — Ready for Implementation  
**Estimated Completion**: 8-12 weeks (part-time development)

---

## 🔬 Research Contribution

This project conducts a controlled comparative evaluation of PII detection methods:

**Research Question**:  
*How do rule-based and NLP-assisted PII detection methods compare in precision, recall, F1-score, and processing efficiency on a controlled dataset containing structured records and unstructured text?*

**Methodology**:
- Synthetic dataset generation with ground truth labels
- Quantitative metrics: precision, recall, F1-score, processing time
- Fair comparison: same data, same evaluation criteria
- Reproducible protocol: fixed seeds, versioned dependencies
- Error analysis: qualitative insights into failure modes

**Expected Deliverables**:
- Comprehensive research report (10-15 pages)
- Experimental results with visualizations
- Reproducibility instructions and archived datasets
- Discussion of trade-offs, limitations, and future work

---

## 🛡️ Privacy & Security

This project implements privacy-by-design principles:

- ✅ **No real personal data**: All testing uses synthetic data only
- ✅ **No PII in logs**: Logging redacts sensitive values
- ✅ **No PII in database**: Only aggregated statistics stored
- ✅ **Input validation**: File type, size, and content validation
- ✅ **CSV formula injection protection**: Sanitized exports
- ✅ **Secure file handling**: Python `tempfile` module
- ✅ **Secrets management**: Environment variables, no hardcoded credentials

**Disclaimer**: This is a research and portfolio project, not a production privacy compliance tool. It does not guarantee 100% PII detection or GDPR/HIPAA compliance.

---

## 🧪 Testing

```powershell
# Run all tests
pytest tests/

# Run with coverage report
pytest tests/ --cov=src --cov-report=html

# Run specific test module
pytest tests/unit/detection/test_email_detector.py -v

# Run linting
ruff check src/ tests/
```

**Test Coverage Targets**:
- Core modules (ingestion, validation, detection, anonymization, pipeline): **>70%**
- Evaluation module: **>70%**
- Utils: **>80%**

---

## 📝 Usage (After Implementation)

### Basic Workflow

1. **Upload Dataset**: Navigate to Upload page, select CSV or JSON file
2. **Review Quality**: View data quality report, optionally clean data
3. **Detect PII**: Select detection method (rule-based or NLP), run detection
4. **Anonymize**: Configure transformation strategies, apply anonymization
5. **Export**: Download processed dataset and reports

### Running Experiments

```powershell
# Generate synthetic evaluation dataset
python experiments/scripts/generate_dataset.py --seed 42 --size 5000 --output data/synthetic/eval_dataset.json

# Run comparative experiments
python experiments/scripts/run_evaluation.py --dataset data/synthetic/eval_dataset.json --methods rule-based,nlp-assisted --runs 3

# Generate report
python experiments/scripts/generate_report.py --results experiments/results/metrics.json
```

---

## 🤝 Contributing

This is primarily a solo portfolio project for academic purposes. However, feedback and suggestions are welcome!

**Development Guidelines**:
- Follow PEP 8 style guide (enforced by Ruff)
- Write unit tests for new features
- Update documentation for significant changes
- No PII in logs, tests, or commits
- Pin dependency versions for reproducibility

See [docs/07-file-module-plan.md](docs/07-file-module-plan.md) for detailed coding standards.

---

## ⚠️ Limitations

This project is designed as a research and learning tool. It has known limitations:

- **Language**: English only (NLP models are language-specific)
- **PII Categories**: Limited to common types (email, phone, SSN, CC, IP, names)
- **Dataset Size**: Optimized for <100K rows (performance degrades beyond)
- **Detection Accuracy**: Not 100% (false positives and negatives expected)
- **Anonymization**: Transformations may not be irreversible or compliant with regulations
- **Deployment**: Local-first design (not optimized for production multi-user scenarios)

See [docs/06-risk-register.md](docs/06-risk-register.md) for detailed risk assessment.

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

**Third-Party Licenses**:
- Microsoft Presidio: MIT License
- spaCy: MIT License
- Streamlit: Apache License 2.0
- Other dependencies: See `requirements.txt` for library licenses

---

## 🙏 Acknowledgments

- **Microsoft Presidio**: PII detection and anonymization framework
- **spaCy**: Industrial-strength NLP library
- **Streamlit**: Rapid web app development framework
- **Faker**: Realistic fake data generation
- **EDISS Program**: Inspiration for research-oriented approach

---

## 📧 Contact

**Developer**: myth-unknown  
**GitHub**: [https://github.com/myth-unknown](https://github.com/myth-unknown)  
**Project Repository**: [https://github.com/myth-unknown/Privacy-Aware-Data-Engineering-Pipeline](https://github.com/myth-unknown/Privacy-Aware-Data-Engineering-Pipeline)

**Purpose**: Technical portfolio for European Data Science and Intelligent Systems (EDISS) master's program application

---

## 🗺️ Roadmap

### Current: Planning Phase (Milestone 0) ✅
- Requirements and architecture specifications complete
- Design and research methodology defined
- Development roadmap established
- Risk assessment completed

### Next: Foundation Phase (Milestone 1)
- Set up development environment
- Create project structure
- Implement basic application
- Verify critical dependencies

### Future: Implementation Phase (Milestones 2-10)
- Incremental feature development
- Continuous testing and quality assurance
- Regular milestone completions

### Final: Research & Deployment (Milestones 11-12)
- Run final experiments
- Write research report
- Complete documentation
- Optional deployment

**Timeline**: 8-12 weeks total (part-time development)  
**Expected Completion**: Q1 2027 (for master's application)

---

## 📚 Resources

### Documentation
- [Project Summary](docs/08-project-summary.md) - Start here for overview
- [Development Roadmap](docs/05-development-roadmap.md) - Implementation plan
- [Architecture Specification](docs/02-architecture-specification.md) - Technical design

### External Resources
- [Microsoft Presidio Documentation](https://microsoft.github.io/presidio/)
- [spaCy Documentation](https://spacy.io/usage)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Faker Documentation](https://faker.readthedocs.io/)

### Research References
- PII Detection and Anonymization literature (to be added in research report)
- Privacy-preserving data processing techniques
- Comparative evaluation methodologies

---

**Status**: 🟡 Planning Complete — Implementation Starting Soon

**Last Updated**: October 25, 2026  
**Version**: 0.1.0 (Planning Phase)
