@echo off
setlocal

echo ======================================================
echo   LLM Formal Verification - Windows Setup (Friend Mode)
echo ======================================================

:: 1. Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.9+ from python.org.
    echo [ERROR] Ensure 'Add Python to PATH' is checked during installation.
    pause
    exit /b %errorlevel%
)

:: 2. Create Virtual Environment
echo [1/3] Creating virtual environment (venv)...
python -m venv venv
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create venv.
    pause
    exit /b %errorlevel%
)

:: 3. Install Requirements
echo [2/3] Installing dependencies (this may take a few minutes)...
venv\Scripts\python.exe -m pip install --upgrade pip >nul
venv\Scripts\pip.exe install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install requirements.
    pause
    exit /b %errorlevel%
)

:: 4. Verify Directories
echo [3/3] Finalizing setup...
if not exist "les_cours" mkdir les_cours
if not exist "logs" mkdir logs

echo.
echo ======================================================
echo   SUCCESS! Setup is complete.
echo   To run the reasoning engine, just double-click 'run_windows.bat'.
echo ======================================================
pause
