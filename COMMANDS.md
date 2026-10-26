# Quick Command Reference

## Running the Application

### Option 1: Using Helper Script
```powershell
.\run_app.ps1
```

.\start.ps1


### Option 2: Manual
```powershell
.\venv\Scripts\Activate.ps1
python -m streamlit run app.py
```

The application will open at: http://localhost:8501

---

## Running Tests

### Option 1: Using Helper Script
```powershell
.\run_tests.ps1
```

### Option 2: Manual
```powershell
.\venv\Scripts\Activate.ps1
python -m pytest tests/ -v --cov=src
```

### Run Specific Tests
```powershell
.\venv\Scripts\Activate.ps1
pytest tests/unit/detection/ -v
pytest tests/unit/anonymization/ -v
```

---

## Linting

### Check for Issues
```powershell
.\venv\Scripts\Activate.ps1
ruff check src/ tests/ --statistics
```

### Auto-Fix Issues
```powershell
.\venv\Scripts\Activate.ps1
ruff check src/ tests/ --fix
```

---

## Virtual Environment

### Activate (if not already active)
```powershell
.\venv\Scripts\Activate.ps1
```

### Deactivate
```powershell
deactivate
```

### Reinstall Dependencies
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## Troubleshooting

### "Streamlit not found"
Make sure virtual environment is activated:
```powershell
.\venv\Scripts\Activate.ps1
pip install streamlit
```

### "Module not found" errors
Reinstall all dependencies:
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Run tests with detailed output
```powershell
.\venv\Scripts\Activate.ps1
pytest tests/ -v -s
```

---

## Development Commands

### Add a new dependency
```powershell
.\venv\Scripts\Activate.ps1
pip install package-name
pip freeze > requirements.txt
```

### View test coverage
After running tests, open: `htmlcov\index.html` in browser

### Clear cache
```powershell
Remove-Item -Recurse -Force .pytest_cache, .ruff_cache, htmlcov, __pycache__
```

---

## Sample Data

Sample datasets are located in:
- `data/samples/customers.csv` - 10 customer records with PII
- `data/samples/orders.json` - 5 order records
- `data/samples/malformed.csv` - Dataset with quality issues

---

## Key Directories

```
.
├── app.py                 # Main Streamlit application
├── src/                   # Source code
│   ├── ingestion/        # Data loading
│   ├── validation/       # Quality profiling
│   ├── detection/        # PII detection
│   ├── anonymization/    # Anonymization
│   ├── ui/               # UI pages
│   └── utils/            # Utilities
├── tests/                # Test suite
│   ├── unit/             # Unit tests
│   └── fixtures/         # Test fixtures
├── data/                 # Data files
│   └── samples/          # Sample datasets
├── config/               # Configuration
├── docs/                 # Documentation
└── logs/                 # Application logs
```

---

## Port Issues

If port 8501 is already in use:
```powershell
.\venv\Scripts\Activate.ps1
python -m streamlit run app.py --server.port 8502
```

---

## Quick Health Check

```powershell
.\venv\Scripts\Activate.ps1
python -c "import streamlit, pandas, presidio_analyzer; print('All imports OK!')"
```

---

**Need Help?** Check `QUICKSTART.md` or `README.md`
