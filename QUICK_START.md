# Quick Start Guide

## 🚀 Running the Application

### Method 1: Double-Click (Easiest) ⭐

**Windows Command Prompt:**
```
Double-click: start.bat
```

**Windows PowerShell:**
```
Double-click: start.ps1
(or type: .\start.ps1)
```

The application will open automatically at http://localhost:8501

---

### Method 2: One Command (Terminal)

**PowerShell (Recommended for Windows):**
```powershell
.\start.ps1
```

**Command Prompt (cmd):**
```batch
start.bat
```

**Git Bash / Linux / macOS:**
```bash
./venv/Scripts/activate    # Windows
# source venv/bin/activate # Linux/macOS
python -m streamlit run app.py
```

---

### Method 3: Manual Steps (Full Control)

**Step 1: Activate Virtual Environment**

PowerShell:
```powershell
.\venv\Scripts\activate
```

Command Prompt:
```batch
venv\Scripts\activate
```

Linux/macOS:
```bash
source venv/bin/activate
```

**Step 2: Run Application**
```powershell
python -m streamlit run app.py
```

**Step 3: Open Browser**
- Go to: http://localhost:8501
- Application should open automatically

**Step 4: Stop Application**
- Press `Ctrl + C` in terminal

---

## 🧪 Running Tests

### Method 1: Double-Click
```
Double-click: test.bat
```

### Method 2: One Command

PowerShell:
```powershell
.\run_tests.ps1
```

Command Prompt:
```batch
test.bat
```

### Method 3: Manual
```powershell
.\venv\Scripts\activate
pytest tests/ -v --cov=src
```

---

## 📁 Project Structure

```
Privacy-Aware-Data-Engineering-Pipeline/
│
├── start.bat           ← Double-click to run (cmd)
├── start.ps1          ← Double-click to run (PowerShell)
├── test.bat           ← Double-click to test
├── run_app.ps1        ← Detailed run script
├── run_tests.ps1      ← Detailed test script
│
├── app.py             ← Main application
├── requirements.txt   ← Dependencies
│
├── src/               ← Source code
├── tests/             ← Test files
├── data/              ← Data files
└── venv/              ← Virtual environment
```

---

## 🐛 Troubleshooting

### "Virtual environment not found"
```powershell
# Create it first
python -m venv venv

# Then activate
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLP model
python -m spacy download en_core_web_lg
```

### "Streamlit not found"
```powershell
.\venv\Scripts\activate
pip install -r requirements.txt
```

### "Port already in use"
```powershell
# Use different port
python -m streamlit run app.py --server.port 8502
```

### "Permission denied" (PowerShell)
```powershell
# Run PowerShell as Administrator, then:
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or just use the batch file:
start.bat
```

---

## 📋 All Available Commands

### Run Application
```powershell
.\start.ps1              # Quick start (PowerShell)
start.bat               # Quick start (cmd)
.\run_app.ps1           # Detailed (PowerShell)
python -m streamlit run app.py  # Direct
```

### Run Tests
```powershell
test.bat                # Quick test (cmd)
.\run_tests.ps1         # Detailed test
pytest tests/ -v        # Direct
```

### Code Quality
```powershell
ruff check src/ tests/  # Lint check
ruff check src/ tests/ --fix  # Auto-fix
```

### Help
```powershell
python -m streamlit --help
pytest --help
```

---

## ⚡ Keyboard Shortcuts

While app is running:
- `Ctrl + C` - Stop application
- `R` (in browser) - Rerun application
- `C` (in browser) - Clear cache

---

## 🌐 Access URLs

- **Local**: http://localhost:8501
- **Network**: http://192.168.x.x:8501 (shown in terminal)

---

## 📝 Sample Data

Test the app with included sample files:

```
data/samples/test_employee_data.csv  - Employee data with PII
data/samples/customers.csv           - Customer information
data/samples/orders.json             - Order data (JSON)
data/samples/malformed.csv           - Test validation
```

---

## 🎯 Quick Workflow

1. **Start App**: Double-click `start.bat` or `start.ps1`
2. **Upload Data**: Use `data/samples/test_employee_data.csv`
3. **Check Quality**: View data quality metrics
4. **Detect PII**: Run detection with "Hybrid" method
5. **Anonymize**: Select masking for emails, redaction for SSN
6. **Export**: Download anonymized data

---

## 💡 Pro Tips

**Fastest Way to Start:**
1. Double-click `start.bat` (Windows)
2. Wait 5 seconds
3. Browser opens automatically ✨

**For Development:**
```powershell
# Terminal 1 - Run app
.\start.ps1

# Terminal 2 - Watch logs
# (logs appear in Terminal 1)

# Terminal 3 - Run tests while developing
.\run_tests.ps1
```

**For Demo:**
```powershell
# Full screen browser (F11)
# Use sample data for quick demo
# Screenshot results for portfolio
```

---

## ✅ Verification

After running, you should see:
```
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

If you see this, you're ready to go! 🎉

---

**Need more help?** See [COMMANDS.md](COMMANDS.md) for complete command reference.
