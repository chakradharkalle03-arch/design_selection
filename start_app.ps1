# Single-Click Launcher for ZariVision AI (Separate Terminal Windows)
Write-Host "============================================================" -ForegroundColor Gold
Write-Host " Launching ZariVision AI App..." -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Gold

$BASE_DIR = $PSScriptRoot
$PYTHON = "$BASE_DIR\backend\venv\Scripts\python.exe"
$FRONTEND_DIR = "$BASE_DIR\frontend"

# Check if venv exists; if not, invoke run.bat to bootstrap
if (-not (Test-Path "$PYTHON")) {
    Write-Host "Setting up Python environment for first time run..." -ForegroundColor Yellow
    & "$BASE_DIR\run.bat"
    exit
}

# 1. Launch FastAPI Backend in a NEW PowerShell Window
Write-Host "Launching FastAPI Backend on Port 8008 (Separate Window)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$BASE_DIR'; & '$PYTHON' -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8008 --reload"

# 2. Check for npm
$hasNpm = Get-Command npm -ErrorAction SilentlyContinue

if ($hasNpm) {
    if (-not (Test-Path "$FRONTEND_DIR\node_modules")) {
        Write-Host "Installing frontend dependencies..." -ForegroundColor Yellow
        Start-Process powershell -Wait -ArgumentList "-Command", "Set-Location '$FRONTEND_DIR'; npm install"
    }
    Write-Host "Launching React Frontend on Port 5173 (Separate Window)..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$FRONTEND_DIR'; npm run dev"
    $TARGET_URL = "http://localhost:5173"
} else {
    Write-Host "Node.js not detected. Serving React UI via FastAPI on Port 8008..." -ForegroundColor Cyan
    $TARGET_URL = "http://localhost:8008"
}

# 3. Wait 3 seconds and open browser
Start-Sleep -Seconds 3
Write-Host "Opening web application in default browser..." -ForegroundColor Green
Start-Process "$TARGET_URL"

Write-Host "`n Servers are running! App available at $TARGET_URL" -ForegroundColor Green
