@echo off
REM Quick start script for Windows

echo ============================================
echo   Health Assistant - Quick Start
echo ============================================
echo.

REM Check if models exist
if not exist "models\*.pkl" (
    echo Models not found. Running training...
    python train-models-script.py
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start backend
echo Starting backend server...
echo.
echo ============================================
echo   Health Assistant is Running!
echo ============================================
echo.
echo Backend API: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py
