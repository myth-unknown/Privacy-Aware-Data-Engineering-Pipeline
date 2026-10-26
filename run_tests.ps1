# Privacy-Aware Data Engineering Pipeline
# Test runner script

Write-Host "Running Tests" -ForegroundColor Cyan
Write-Host "================" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "Virtual environment not found!" -ForegroundColor Red
    exit 1
}

. venv\Scripts\Activate.ps1

# Run pytest
Write-Host "Running pytest with coverage..." -ForegroundColor Green
Write-Host ""
python -m pytest tests/ -v --cov=src --cov-report=term --cov-report=html

Write-Host ""
Write-Host "Tests complete!" -ForegroundColor Green
Write-Host "Coverage report: htmlcov\index.html" -ForegroundColor Yellow
