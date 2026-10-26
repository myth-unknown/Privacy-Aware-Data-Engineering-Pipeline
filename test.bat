@echo off
REM Simple batch script to run tests

echo =====================================
echo Running Tests
echo =====================================
echo.

if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
echo Running pytest...
echo.
python -m pytest tests/ -v --cov=src
echo.
echo Tests complete!
pause
