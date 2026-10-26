@echo off
REM Simple batch script to run the Privacy-Aware Data Engineering Pipeline
REM Works with Command Prompt (cmd)

echo =====================================
echo Privacy-Aware Data Pipeline
echo =====================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo Please run setup first: python -m venv venv
    echo Then install: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Activate virtual environment
echo [1/2] Activating virtual environment...
call venv\Scripts\activate.bat

REM Run the application
echo [2/2] Starting application...
echo.
echo Application will open at: http://localhost:8501
echo Press Ctrl+C to stop
echo.
python -m streamlit run app.py
