# SipatGov Backend API Launcher - PowerShell Version
# Right-click and select "Run with PowerShell" to execute

Write-Host "=========================================`n" -ForegroundColor Green
Write-Host "   SipatGov Backend API Server Launcher" -ForegroundColor Green
Write-Host "=========================================`n" -ForegroundColor Green

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[INFO] Python found: $pythonVersion" -ForegroundColor Cyan
} catch {
    Write-Host "[ERROR] Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.10+ from https://python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if .env file exists
if (-Not (Test-Path ".env")) {
    Write-Host "[WARNING] .env file not found" -ForegroundColor Yellow
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "[INFO] Created .env from .env.example" -ForegroundColor Cyan
        Write-Host "[INFO] Please edit .env with your database credentials" -ForegroundColor Yellow
    }
}

Write-Host "[INFO] Checking required packages..." -ForegroundColor Cyan
$fastapi = pip show fastapi 2>&1
if ($null -eq $fastapi) {
    Write-Host "[INFO] Installing dependencies..." -ForegroundColor Cyan
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to install dependencies" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host "[INFO] Starting SipatGov Backend API..." -ForegroundColor Cyan
Write-Host "[INFO] Server will be available at http://localhost:8000" -ForegroundColor Green
Write-Host "[INFO] API documentation at http://localhost:8000/docs" -ForegroundColor Green
Write-Host "[INFO] Press Ctrl+C to stop the server`n" -ForegroundColor Cyan

# Set environment variables
$env:PYTORCH_CUDA_ALLOC_CONF = "max_split_size_mb:512"
$env:TOKENIZERS_PARALLELISM = "false"

# Start the server
python main.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Server failed to start" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
