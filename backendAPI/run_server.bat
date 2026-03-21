@echo off
REM SipatGov Backend API Launcher for Windows
REM This batch file launches the FastAPI server with GPU support

title SipatGov Backend API Server

echo.
echo =========================================
echo   SipatGov Backend API Server Launcher
echo =========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from python.org
    pause
    exit /b 1
)

echo [INFO] Python found
python --version
echo.

REM Check if .env file exists
if not exist .env (
    echo [WARNING] .env file not found, using defaults
    copy .env.example .env
    echo [INFO] Created .env from .env.example
)

echo.
echo [INFO] Checking required packages...
pip show fastapi >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Installing dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo [INFO] Starting SipatGov Backend API...
echo [INFO] Server will be available at http://localhost:8000
echo [INFO] API documentation at http://localhost:8000/docs
echo [INFO] Press Ctrl+C to stop the server
echo.

REM Set environment variables for GPU optimization
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
set TOKENIZERS_PARALLELISM=false

REM Start the server
python main.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Server failed to start
    pause
    exit /b 1
)

pause
