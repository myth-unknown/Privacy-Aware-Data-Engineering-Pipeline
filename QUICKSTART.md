# Quick Start Guide
## Privacy-Aware Data Engineering Pipeline

**Getting started in 3 simple steps!**

---

## Step 1: Verify Setup

The virtual environment and all dependencies should already be installed. Verify:

```powershell
# Check virtual environment exists
dir venv

# Activate virtual environment
venv\Scripts\Activate.ps1

# Verify Python
python --version
# Should show: Python 3.12.x

# Verify key packages
pip list | Select-String "streamlit|presidio|spacy"
# Should show: streamlit, presidio-analyzer, presidio-anonymizer, spacy

# Verify spaCy model
python -m spacy info en_core_web_lg
# Should show model information
```

---

## Step 2: Run the Application

### Option A: Using PowerShell Script (Easiest)
```powershell
.\run_app.ps1
```

### Option B: Manual Command
```powershell
# Activate virtual environment
venv\Scripts\Activate.ps1

# Run streamlit
python -m streamlit run app.py
```

### Option C: Using Direct Python Path
```powershell
venv\Scripts\python.exe -m streamlit run app.py
```

The application will open automatically in your browser at:
**http://localhost:8501**

Press **Ctrl+C** in PowerShell to stop the server.

---

## Step 3: Run Tests

### Option A: Using PowerShell Script
```powershell
.\run_tests.ps1
```

### Option B: Manual Command
```powershell
# Activate virtual environment
venv\Scripts\Activate.ps1

# Run tests
pytest tests/ -v
```

---

## Common Issues & Solutions

### Issue: "streamlit is not recognized"

**Solution**: Use `python -m streamlit` instead of just `streamlit`

```powershell
# Instead of:
streamlit run app.py

# Use:
python -m streamlit run app.py
```

### Issue: Virtual environment not activated

**Solution**: Always activate before running commands

```powershell
# Activate first
venv\Scripts\Activate.ps1

# Then run commands
python -m streamlit run app.py
```

### Issue: Module not found errors

**Solution**: Reinstall dependencies

```powershell
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m spacy download en_core_web_lg
```

---

## Development Workflow

### Run Application
```powershell
.\run_app.ps1
# or
python -m streamlit run app.py
```

### Run Tests
```powershell
.\run_tests.ps1
# or
pytest tests/ -v --cov=src
```

### Run Linting
```powershell
venv\Scripts\Activate.ps1
ruff check src/ tests/
```

### Fix Linting Issues
```powershell
ruff check src/ tests/ --fix --unsafe-fixes
```

---

## Directory Structure

```
Privacy-Aware-Data-Engineering-Pipeline/
├── app.py                    # Main application entry point
├── run_app.ps1               # Launch script
├── run_tests.ps1             # Test runner script
├── requirements.txt          # Dependencies
├── config/default.yaml       # Configuration
├── src/                      # Source code
│   ├── ui/pages/home.py     # Home page
│   └── utils/               # Utilities
├── tests/                    # Tests
├── data/                     # Data files (not committed)
├── logs/                     # Log files (not committed)
└── docs/                     # Documentation
```

---

## Next Steps

1. **Explore the Application**: Browse through the home page to understand the features
2. **Wait for Milestone 2**: Upload functionality will be added next
3. **Check Documentation**: Review `docs/` for detailed specifications
4. **Run Tests**: Ensure everything works with `.\run_tests.ps1`

---

## Need Help?

- **Documentation**: Check `README.md` for complete setup instructions
- **Planning Docs**: See `docs/` directory for specifications
- **Issues**: Check console output for error messages
- **Tests**: Run `pytest tests/ -v` to verify installation

---

**Application Status**: ✅ Ready to use!  
**Current Milestone**: Milestone 1 Complete  
**Next Milestone**: Data Ingestion (coming soon)
