@echo off
echo Starting AI Flashcard Generator Backend...
echo.

REM Check if Python 3.10 or 3.11 is available
python --version 2>nul
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.10 or 3.11 from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Start the server
echo.
echo Starting FastAPI server...
echo Server will be available at: http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
python main.py

pause 