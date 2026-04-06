@echo off
setlocal

:: LLM Formal Verification - One-Click Runner (Windows)
if not exist "venv" (
    echo [ERROR] Virtual environment 'venv' not found. Please run 'setup_windows.bat' first!
    pause
    exit /b 1
)

echo.
echo ======================================================
echo   Launching LLM Formal Verification Reasoning Engine...
echo ======================================================
echo.

venv\Scripts\python.exe main.py

echo.
echo ======================================================
echo   Execution Finished.
echo   Check your 'logs/' directory for results.
echo ======================================================
pause
