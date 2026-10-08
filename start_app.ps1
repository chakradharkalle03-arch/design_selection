# Single-Click Launcher for ZariVision AI (Separate Terminal Windows)
Write-Host "============================================================" -ForegroundColor Gold
Write-Host "🚀 Launching ZariVision AI App (Separate Logs Windows)..." -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Gold

$BASE_DIR = $PSScriptRoot
$PYTHON = "$BASE_DIR\backend\venv\Scripts\python.exe"
$FRONTEND_DIR = "$BASE_DIR\frontend"

# 1. Launch FastAPI Backend in a NEW PowerShell Window
Write-Host "▶️ Launching FastAPI Backend on Port 8008 (Separate Window)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$BASE_DIR'; & '$PYTHON' -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8008 --reload"

# 2. Launch React Frontend in a NEW PowerShell Window
Write-Host "▶️ Launching React Frontend on Port 5173 (Separate Window)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$FRONTEND_DIR'; npm run dev"

# 3. Wait 3 seconds and open browser
Start-Sleep -Seconds 3
Write-Host "🌐 Opening web application in default browser..." -ForegroundColor Green
Start-Process "http://localhost:5173"

Write-Host "`n✅ Both servers are running in separate PowerShell windows!" -ForegroundColor Green
Write-Host "Web app available at http://localhost:5173" -ForegroundColor Gold
