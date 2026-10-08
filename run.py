import os
import sys
import time
import subprocess
import webbrowser
from pathlib import Path

# Ensure UTF-8 output encoding for Windows terminal compatibility
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent
VENV_PYTHON = BASE_DIR / "backend" / "venv" / "Scripts" / "python.exe"

if not VENV_PYTHON.exists():
    VENV_PYTHON = sys.executable

def main():
    print("=" * 60)
    print("Launching ZariVision AI App in Separate PowerShell Windows...")
    print("=" * 60)

    # Command for Window 1 (FastAPI Backend)
    backend_cmd = f'Start-Process powershell -ArgumentList "-NoExit", "-Command", "& \'{VENV_PYTHON}\' -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8008 --reload"'
    print("[1/2] Opening Separate Window for FastAPI Backend Logs (Port 8008)...")
    subprocess.run(["powershell", "-Command", backend_cmd], cwd=str(BASE_DIR))

    # Command for Window 2 (React Frontend)
    frontend_dir = BASE_DIR / "frontend"
    frontend_cmd = f'Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location \'{frontend_dir}\'; npm run dev"'
    print("[2/2] Opening Separate Window for React Frontend Logs (Port 5173)...")
    subprocess.run(["powershell", "-Command", frontend_cmd], cwd=str(BASE_DIR))

    # Wait 3 seconds for servers to start
    print("\n⏳ Initializing servers... Opening web app in your default browser in 3 seconds...\n")
    time.sleep(3)

    app_url = "http://localhost:5173"
    try:
        webbrowser.open(app_url)
    except Exception as e:
        print(f"Browser open notice: {e}")

    print("=" * 60)
    print("✅ Web App opened at http://localhost:5173")
    print("Both Backend & Frontend terminals are running in separate PowerShell windows.")
    print("=" * 60)

if __name__ == "__main__":
    main()
