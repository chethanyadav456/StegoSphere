@echo off
echo ==========================================
echo         StegoSphere Setup (Windows)
echo ==========================================

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in your PATH.
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b
)

:: Create virtual environment if it doesn't exist
if not exist venv (
    echo [INFO] Creating virtual environment...
    python -m venv venv
) else (
    echo [INFO] Virtual environment already exists.
)

:: Activate virtual environment
call venv\Scripts\activate

:: Install requirements
if exist requirements.txt (
    echo [INFO] Installing/Updating dependencies...
    pip install -r requirements.txt
) else (
    echo [ERROR] requirements.txt not found! Cannot install dependencies.
    pause
    exit /b
)

echo.
echo ==========================================
echo        Setup Complete! Starting App...
echo ==========================================
python main.py
pause