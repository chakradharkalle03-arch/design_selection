@echo off
setlocal enabledelayedexpansion
title ZariVision AI - One-Click Launcher

echo ====================================================================
echo                 ZARIVISION AI - ONE-CLICK LAUNCHER
echo ====================================================================
echo.

:: 1. Locate Python
set "PYTHON_EXE="
where python >nul 2>nul
if %errorlevel% equ 0 (
    set "PYTHON_EXE=python"
) else (
    where py >nul 2>nul
    if %errorlevel% equ 0 (
        set "PYTHON_EXE=py"
    ) else (
        if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
            set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
        ) else if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
            set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
        ) else if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" (
            set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
        )
    )
)

if "%PYTHON_EXE%"=="" (
    echo [ERROR] Python was not found on your system!
    echo Please install Python 3.10 or higher from: https://www.python.org/downloads/
    echo (Make sure to check "Add Python to PATH" during installation)
    echo.
    pause
    exit /b 1
)

echo [1/4] Found Python: %PYTHON_EXE%

:: 2. Setup / Verify Virtual Environment
set "VENV_DIR=%~dp0backend\venv"
set "VENV_PYTHON=%VENV_DIR%\Scripts\python.exe"

if not exist "%VENV_PYTHON%" (
    echo [2/4] Setting up Python virtual environment in backend\venv...
    "%PYTHON_EXE%" -m venv "%VENV_DIR%"
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo [2/4] Installing backend and AI dependencies (this may take 2-3 minutes on first run)...
    "%VENV_PYTHON%" -m pip install --upgrade pip
    "%VENV_PYTHON%" -m pip install -r "%~dp0backend\requirements.txt"
) else (
    echo [2/4] Python virtual environment ready.
)

:: 3. Download & Verify Local CLIP AI Model
echo [3/4] Verifying local AI model (openai/clip-vit-base-patch32)...
"%VENV_PYTHON%" "%~dp0backend\download_model.py"
if %errorlevel% neq 0 (
    echo [WARNING] Model verification had a notice, continuing launch...
)

:: 4. Check for Node.js / Frontend
echo [4/4] Starting servers...
where npm >nul 2>nul
set "HAS_NPM=%errorlevel%"

if %HAS_NPM% equ 0 (
    if not exist "%~dp0frontend\node_modules" (
        echo Installing React frontend dependencies...
        pushd "%~dp0frontend"
        call npm install
        popd
    )
    
    echo Starting FastAPI Backend (Port 8008) in separate window...
    start powershell -NoExit -Command "Set-Location '%~dp0'; & '%VENV_PYTHON%' -m uvicorn app.main:app --app-dir '%~dp0backend' --host 127.0.0.1 --port 8008 --reload"
    
    echo Starting React Frontend Dev Server (Port 5173) in separate window...
    start powershell -NoExit -Command "Set-Location '%~dp0frontend'; npm run dev"
    
    timeout /t 4 >nul
    echo Opening http://localhost:5173 in browser...
    start http://localhost:5173
) else (
    echo [INFO] Node.js not detected. Serving production React build directly via FastAPI!
    start powershell -NoExit -Command "Set-Location '%~dp0'; & '%VENV_PYTHON%' -m uvicorn app.main:app --app-dir '%~dp0backend' --host 127.0.0.1 --port 8008"
    
    timeout /t 3 >nul
    echo Opening http://localhost:8008 in browser...
    start http://localhost:8008
)

echo.
echo ====================================================================
echo  SUCCESS: ZariVision AI is running!
echo  Open http://localhost:5173 (or http://localhost:8008) in your browser.
echo ====================================================================
