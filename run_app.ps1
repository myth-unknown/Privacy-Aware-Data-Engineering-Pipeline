# Privacy-Aware Data Engineering Pipeline
# Launch script for Streamlit application

Write-Host "Privacy-Aware Data Engineering Pipeline" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
. venv\Scripts\Activate.ps1

# Check if streamlit is installed
try {
    $streamlitVersion = python -m streamlit --version 2>$null
    Write-Host "Streamlit found: $streamlitVersion" -ForegroundColor Green
} catch {
    Write-Host "Streamlit not found in virtual environment!" -ForegroundColor Red
    Write-Host "Please run: pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

# Launch application
Write-Host ""
Write-Host "Launching application..." -ForegroundColor Cyan
Write-Host "Local URL: http://localhost:8501" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the application" -ForegroundColor Gray
Write-Host ""

# Run streamlit
python -m streamlit run app.py
