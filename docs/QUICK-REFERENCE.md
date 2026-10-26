# Quick Reference Guide
## Privacy-Aware Data Engineering Pipeline

**For Use During Implementation**

---

## 📋 Planning Documents Overview

| Document | Purpose | When to Use |
|----------|---------|-------------|
| [08-project-summary.md](08-project-summary.md) | High-level overview | Start here, review before milestones |
| [01-requirements-specification.md](01-requirements-specification.md) | What to build | Reference during feature implementation |
| [02-architecture-specification.md](02-architecture-specification.md) | How to build it | Reference during design decisions |
| [03-ui-ux-specification.md](03-ui-ux-specification.md) | How it should look | Reference during UI implementation |
| [04-data-research-specification.md](04-data-research-specification.md) | Research methodology | Reference during evaluation implementation |
| [05-development-roadmap.md](05-development-roadmap.md) | When to build it | Follow sequentially during implementation |
| [06-risk-register.md](06-risk-register.md) | What can go wrong | Review weekly, before critical dependencies |
| [07-file-module-plan.md](07-file-module-plan.md) | Where to put code | Reference during coding |

---

## 🎯 Current Milestone Checklist

> Update this section as you progress through milestones

**Current Milestone**: Milestone 0 (Planning) — Nearing Completion  
**Next Milestone**: Milestone 1 (Project Foundation)

### Before Starting Milestone 1
- [ ] Review all planning documents one final time
- [ ] Resolve any open questions or conflicts
- [ ] Get approval for specifications (self-review if solo)
- [ ] Ensure Python 3.11 installed
- [ ] Ensure Git configured
- [ ] Clear workspace and mental readiness

---

## 🚀 Milestone 1 Quick Tasks

**Objective**: Set up environment and basic structure

**Key Tasks**:
1. [ ] Create Python 3.11 virtual environment
2. [ ] Create initial `requirements.txt`
3. [ ] Create complete directory structure
4. [ ] Create configuration files (`config/default.yaml`, `.env.example`)
5. [ ] Implement config loader and logger
6. [ ] Create basic `app.py` and home page
7. [ ] Write first test and verify pytest works
8. [ ] Test spaCy and Presidio installation **CRITICAL**

**Files to Create**: See Roadmap Milestone 1, Section "Files to Create"

**Verification**:
```powershell
# Activate environment
venv\Scripts\activate

# Test dependencies
pip install streamlit pandas presidio-analyzer presidio-anonymizer spacy
python -m spacy download en_core_web_lg

# Verify spaCy model
python -m spacy info en_core_web_lg

# Test app launches
streamlit run app.py

# Test pytest
pytest tests/ -v
```

**Risk Alert**: Test spaCy and Presidio compatibility immediately (R-1, R-2)

---

## ⚠️ Critical Reminders

### Privacy & Security (Always)
- ❌ **NEVER** log raw PII values
- ❌ **NEVER** store raw PII in database
- ❌ **NEVER** commit secrets to Git
- ✅ **ALWAYS** use aggregated stats only
- ✅ **ALWAYS** use environment variables for secrets
- ✅ **ALWAYS** sanitize CSV exports (formula injection)

### Code Quality (Before Every Commit)
- [ ] Run linting: `ruff check src/ tests/`
- [ ] Run tests: `pytest tests/ -v`
- [ ] Check no PII in logs or debug output
- [ ] Verify imports organized
- [ ] Ensure docstrings for new functions/classes

### Git Workflow (Every Milestone)
```powershell
# Start milestone
git checkout -b milestone-N-description

# Commit frequently
git add <files>
git commit -m "feat: implement X"

# Before pushing
pytest tests/
ruff check src/

# After milestone completion
git checkout main
git merge milestone-N-description
git tag vN.0
git push origin main --tags
```

---

## 📐 Architecture Quick Reference

### Module Dependencies
```
UI → Application → Data
     ↓
Evaluation (independent)
```

### Pipeline Stages (in order)
1. Ingestion (load file)
2. Profiling (analyze quality)
3. Validation (check schema/constraints)
4. Detection (find PII)
5. Transformation (apply anonymization)
6. Post-validation (re-check)
7. Storage (save to DuckDB)
8. Reporting (generate summary)

### Key Dataclasses
- `IngestionResult` (src/ingestion/models.py)
- `QualityProfile` (src/validation/models.py)
- `PIIDetection` (src/detection/models.py)
- `AnonymizationConfig` (src/anonymization/models.py)
- `PipelineResult` (src/pipeline/models.py)

---

## 🧪 Testing Quick Reference

### Run Tests
```powershell
# All tests
pytest tests/ -v

# Specific module
pytest tests/unit/detection/ -v

# With coverage
pytest tests/ --cov=src --cov-report=html

# Specific test
pytest tests/unit/detection/test_email_detector.py::test_valid_email -v
```

### Write Tests
```python
# tests/unit/ingestion/test_loader.py
import pytest
from src.ingestion.loader import load_csv

def test_load_csv_valid_file():
    """Test loading valid CSV file."""
    df = load_csv('data/samples/customers.csv')
    assert df is not None
    assert len(df) > 0
    assert 'email' in df.columns

def test_load_csv_file_not_found():
    """Test loading non-existent file raises error."""
    with pytest.raises(FileNotFoundError):
        load_csv('nonexistent.csv')
```

---

## 🎨 UI Quick Reference

### Color Palette
- Primary Blue: `#2E5CFF`
- Success Green: `#10B981`
- Warning Yellow: `#F59E0B`
- Error Red: `#EF4444`
- Background: `#FFFFFF`
- Text: `#111827`

### Create Page
```python
# src/ui/pages/example.py
import streamlit as st
from src.ui.components.metrics import metric_card
from src.ui.components.charts import bar_chart

def render():
    """Render example page."""
    st.title("Example Page")
    
    # Metric card
    metric_card(
        value="1,234",
        label="Items Detected",
        icon="🔍"
    )
    
    # Chart
    bar_chart(
        data=df,
        x='category',
        y='count',
        title='Distribution'
    )
```

### Register Page in app.py
```python
# app.py
import streamlit as st
from src.ui.pages import home, upload, quality, example

pages = {
    "Home": home,
    "Upload": upload,
    "Quality": quality,
    "Example": example,  # Add new page
}

selection = st.sidebar.radio("Navigate", list(pages.keys()))
pages[selection].render()
```

---

## 🔍 PII Detection Quick Reference

### Rule-Based Detector Example
```python
# src/detection/rule_based_detector.py
import re
from typing import List
from src.detection.models import PIIDetection

class EmailDetector:
    """Detect email addresses using regex."""
    
    PATTERN = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    
    def detect(self, text: str) -> List[PIIDetection]:
        """Detect emails in text."""
        detections = []
        for match in self.PATTERN.finditer(text):
            detections.append(PIIDetection(
                column='',  # Set by caller
                row_index=-1,  # Set by caller
                pii_type='email',
                start=match.start(),
                end=match.end(),
                confidence=1.0,
                method='rule-based'
            ))
        return detections
```

### NLP Detector Example
```python
# src/detection/nlp_detector.py
from presidio_analyzer import AnalyzerEngine
from src.detection.models import PIIDetection

class PresidioDetector:
    """Detect PII using Presidio + spaCy."""
    
    def __init__(self):
        self.analyzer = AnalyzerEngine()
    
    def detect(self, text: str) -> List[PIIDetection]:
        """Detect PII using NLP."""
        results = self.analyzer.analyze(text, language='en')
        detections = []
        for result in results:
            detections.append(PIIDetection(
                column='',
                row_index=-1,
                pii_type=result.entity_type.lower(),
                start=result.start,
                end=result.end,
                confidence=result.score,
                method='nlp-assisted'
            ))
        return detections
```

---

## 📊 Evaluation Quick Reference

### Generate Dataset
```python
# experiments/scripts/generate_dataset.py
from faker import Faker
from src.evaluation.models import GroundTruthAnnotation, Entity

fake = Faker()
Faker.seed(42)  # For reproducibility

def generate_example():
    """Generate one example with ground truth."""
    name = fake.name()
    email = fake.email()
    phone = fake.phone_number()
    
    text = f"Contact {name} at {email} or {phone}"
    
    entities = [
        Entity(start=8, end=8+len(name), label='PERSON'),
        Entity(start=text.find(email), end=text.find(email)+len(email), label='EMAIL'),
        Entity(start=text.find(phone), end=text.find(phone)+len(phone), label='PHONE'),
    ]
    
    return GroundTruthAnnotation(text=text, entities=entities)
```

### Calculate Metrics
```python
# src/evaluation/metrics.py
from sklearn.metrics import precision_score, recall_score, f1_score

def calculate_metrics(y_true, y_pred):
    """Calculate precision, recall, F1."""
    return {
        'precision': precision_score(y_true, y_pred, zero_division=0),
        'recall': recall_score(y_true, y_pred, zero_division=0),
        'f1': f1_score(y_true, y_pred, zero_division=0),
    }
```

---

## 🗄️ Database Quick Reference

### Initialize Database
```python
# src/storage/duckdb_manager.py
import duckdb

def initialize_database(db_path='data/pipeline.duckdb'):
    """Create database and tables."""
    conn = duckdb.connect(db_path)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS datasets (
            id VARCHAR PRIMARY KEY,
            name VARCHAR,
            upload_date TIMESTAMP,
            row_count INTEGER,
            column_count INTEGER
        )
    """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS processing_runs (
            run_id VARCHAR PRIMARY KEY,
            dataset_id VARCHAR,
            timestamp TIMESTAMP,
            method VARCHAR,
            status VARCHAR,
            duration_seconds REAL,
            FOREIGN KEY (dataset_id) REFERENCES datasets(id)
        )
    """)
    
    return conn
```

### Query History
```python
def query_history(conn, limit=10):
    """Get recent processing runs."""
    return conn.execute(f"""
        SELECT run_id, timestamp, method, status
        FROM processing_runs
        ORDER BY timestamp DESC
        LIMIT {limit}
    """).fetchdf()
```

---

## 🔧 Configuration Quick Reference

### Load Configuration
```python
# src/utils/config_loader.py
import yaml

def load_config(config_path='config/default.yaml'):
    """Load YAML configuration."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def get_config_value(config, key, default=None):
    """Get nested config value using dot notation."""
    keys = key.split('.')
    value = config
    for k in keys:
        value = value.get(k, default)
        if value is default:
            return default
    return value
```

### Environment Variables
```python
# Load from .env
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_PATH = os.getenv('DUCKDB_PATH', 'data/pipeline.duckdb')
MAX_FILE_SIZE_MB = int(os.getenv('PIPELINE_MAX_FILE_SIZE_MB', 50))
```

---

## 📝 Logging Quick Reference

### Setup Logging
```python
# src/utils/logger.py
import logging

def setup_logging(level='INFO', log_file='logs/pipeline.log'):
    """Configure logging."""
    logging.basicConfig(
        level=getattr(logging, level),
        format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file)
        ]
    )

# Use in modules
import logging
logger = logging.getLogger(__name__)

logger.info(f"Processed {len(df)} rows")
logger.warning(f"Quality score low: {score}")
logger.error(f"Detection failed: {error}")
```

### Logging Rules
```python
# Good
logger.info(f"Detected {len(detections)} PII instances")
logger.info(f"PII types: {set(d.pii_type for d in detections)}")

# Bad - DO NOT DO THIS
logger.info(f"Detected email: {email_value}")  # ❌ Logs PII
logger.debug(f"Row data: {row}")  # ❌ May contain PII
```

---

## 🐛 Debugging Quick Reference

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'src'`  
**Solution**: Ensure running from project root, not subdirectory

**Issue**: spaCy model not found  
**Solution**: `python -m spacy download en_core_web_lg`

**Issue**: DuckDB file locked  
**Solution**: Close all connections before reopening

**Issue**: Streamlit caching issues  
**Solution**: Clear cache with `st.cache_data.clear()` or restart app

**Issue**: Tests fail with import errors  
**Solution**: Ensure `tests/` has `__init__.py` files, use absolute imports

### Debug Mode
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Streamlit debug mode
# Run with: streamlit run app.py --logger.level=debug
```

---

## 📦 Dependency Checklist

### Core Dependencies (verify in Milestone 1)
- [ ] streamlit: Web UI framework
- [ ] pandas: Data processing
- [ ] plotly: Visualizations
- [ ] presidio-analyzer: PII detection
- [ ] presidio-anonymizer: PII transformation
- [ ] spacy: NLP
- [ ] duckdb: Database
- [ ] faker: Synthetic data
- [ ] scikit-learn: Metrics
- [ ] pytest: Testing
- [ ] ruff: Linting
- [ ] pyyaml: Configuration
- [ ] python-dotenv: Environment variables

### Installation Order
```powershell
# 1. Core dependencies
pip install streamlit pandas numpy plotly

# 2. PII detection
pip install presidio-analyzer presidio-anonymizer spacy

# 3. spaCy model (separate)
python -m spacy download en_core_web_lg

# 4. Database and evaluation
pip install duckdb faker scikit-learn

# 5. Development tools
pip install pytest pytest-cov pytest-mock ruff pyyaml python-dotenv
```

---

## ⏱️ Time Estimates

| Milestone | Optimistic | Realistic | Pessimistic |
|-----------|------------|-----------|-------------|
| 1. Foundation | 3 days | 1 week | 1.5 weeks |
| 2. Ingestion | 3 days | 1 week | 1.5 weeks |
| 3. Quality | 3 days | 1 week | 1.5 weeks |
| 4. Rule Detection | 5 days | 1.5 weeks | 2 weeks |
| 5. NLP Detection | 5 days | 1.5 weeks | 2 weeks |
| 6. Anonymization | 3 days | 1 week | 1.5 weeks |
| 7. Pipeline | 3 days | 1 week | 1.5 weeks |
| 8. Evaluation | 7 days | 2 weeks | 3 weeks |
| 9. UI | 7 days | 2 weeks | 3 weeks |
| 10. Hardening | 3 days | 1 week | 1.5 weeks |
| 11. Report | 7 days | 1.5 weeks | 2 weeks |
| 12. Deployment | 3 days | 1 week | 1.5 weeks |
| **Total** | **7 weeks** | **10 weeks** | **14 weeks** |

**Recommended**: Plan for 10-12 weeks with buffer time

---

## 🎓 Learning Resources

### Python Data Engineering
- [Real Python - pandas tutorials](https://realpython.com/pandas-python-explore-dataset/)
- [pandas documentation](https://pandas.pydata.org/docs/)

### Privacy & PII Detection
- [Microsoft Presidio docs](https://microsoft.github.io/presidio/)
- [spaCy NER guide](https://spacy.io/usage/linguistic-features#named-entities)

### Streamlit
- [Streamlit tutorial](https://docs.streamlit.io/library/get-started)
- [Streamlit components](https://docs.streamlit.io/library/api-reference)

### Testing
- [pytest documentation](https://docs.pytest.org/)
- [Python testing best practices](https://realpython.com/pytest-python-testing/)

### Research Methodology
- [Precision, Recall, F1 explanation](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_fscore_support.html)
- [Confusion matrix](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html)

---

## 🆘 When Stuck

### Problem-Solving Process
1. **Check planning docs**: Requirements, architecture, specifications
2. **Review risk register**: Is this a known risk?
3. **Search documentation**: Library/framework docs
4. **Check similar code**: Look at existing modules
5. **Run tests**: Isolate the problem
6. **Debug incrementally**: Print statements, breakpoints
7. **Search online**: Stack Overflow, GitHub issues
8. **Take a break**: Sometimes helps to step away
9. **Document issue**: Write down what you tried
10. **Adjust plan if needed**: Update specs, roadmap

### Emergency Contacts (Self-Reminders)
- **Planning docs**: `docs/` directory
- **Architecture**: `docs/02-architecture-specification.md`
- **Risks**: `docs/06-risk-register.md`
- **File structure**: `docs/07-file-module-plan.md`

---

## ✅ Pre-Commit Checklist

Before every Git commit:
- [ ] Code linted: `ruff check src/ tests/`
- [ ] Tests pass: `pytest tests/ -v`
- [ ] No PII in logs or debug output
- [ ] Docstrings added for new functions
- [ ] No commented-out code (unless explained)
- [ ] No secrets or hardcoded paths
- [ ] Imports organized
- [ ] Meaningful commit message

---

## 🎯 Success Indicators

**You're on track if:**
- ✅ Each milestone completes within estimated time (+/- 50%)
- ✅ Tests pass consistently
- ✅ Code reviews reveal no major issues
- ✅ Dependencies install without problems
- ✅ Progress feels steady (not rushed or stalled)
- ✅ Documentation stays updated
- ✅ You understand what you're building and why

**Warning signs:**
- ⚠️ Milestones taking >2x estimated time
- ⚠️ Many failing tests or skipped tests
- ⚠️ Repeated dependency issues
- ⚠️ Scope creep (adding unplanned features)
- ⚠️ Documentation falling behind
- ⚠️ Feeling rushed or overwhelmed

**If warning signs appear:**
- Review roadmap and adjust estimates
- Identify blockers and address them
- Consider reducing scope (defer nice-to-haves)
- Take breaks to avoid burnout
- Revisit risk register

---

## 📅 Weekly Review Template

**Date**: _______  
**Current Milestone**: _______  
**Progress**: ___% complete

**Completed This Week:**
- [ ] Task 1
- [ ] Task 2

**Blockers:**
- Issue 1: Description and status
- Issue 2: Description and status

**Next Week:**
- [ ] Task 1
- [ ] Task 2

**Risks:**
- Any new risks identified?
- Any existing risks materialized?

**Notes:**
- Lessons learned
- Adjustments to plan
- Questions to resolve

---

**This document is your implementation companion. Reference it frequently!**

**Good luck with implementation! 🚀**
