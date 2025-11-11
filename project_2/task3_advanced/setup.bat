@echo off
REM Health Assistant Setup Script for Windows
REM Automated setup for development environment

echo ============================================
echo   Health Assistant - Automated Setup
echo ============================================
echo.

REM Check Python installation
echo [1/7] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [OK] Found %PYTHON_VERSION%

REM Check Node.js (optional)
echo [2/7] Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Node.js not found (optional, needed for frontend)
) else (
    for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
    echo [OK] Found Node.js %NODE_VERSION%
)

REM Create virtual environment
echo [3/7] Creating Python virtual environment...
if not exist "venv" (
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)

REM Activate virtual environment
echo [4/7] Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated

REM Install Python dependencies
echo [5/7] Installing Python dependencies...
echo This may take a few minutes...
python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo [ERROR] Failed to upgrade pip and setuptools
    pause
    exit /b 1
)
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)
echo [OK] Python dependencies installed

REM Create models directory
echo [6/7] Creating models directory...
if not exist "models" mkdir models
echo [OK] Models directory created

REM Train models
echo [7/7] Training machine learning models...
echo This may take a few minutes...
python train-models-script.py
if errorlevel 1 (
    echo [ERROR] Model training failed
    echo Please check the error messages above
    pause
    exit /b 1
)
echo [OK] Models trained successfully

echo.
echo ============================================
echo   Setup Complete! 🎉
echo ============================================
echo.
echo To start the backend server:
echo   1. Activate virtual environment: venv\Scripts\activate
echo   2. Run: python app.py
echo.
echo To start the frontend (optional):
echo   1. cd frontend
echo   2. npm install
echo   3. npm start
echo.
echo Or use Docker:
echo   docker-compose up --build
echo.
pause
