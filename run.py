import os
import sys
import time
import shutil
import subprocess
import webbrowser
from pathlib import Path

# Safe console encoding
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent

# Locate venv python
if sys.platform == "win32":
    VENV_PYTHON = BASE_DIR / "backend" / "venv" / "Scripts" / "python.exe"
else:
    VENV_PYTHON = BASE_DIR / "backend" / "venv" / "bin" / "python"

def setup_environment():
    global VENV_PYTHON
    if not VENV_PYTHON.exists():
        print("[1/3] Creating Python virtual environment in backend/venv...")
        subprocess.check_call([sys.executable, "-m", "venv", str(BASE_DIR / "backend" / "venv")])
        print("[1/3] Installing backend and local AI dependencies...")
        subprocess.check_call([str(VENV_PYTHON), "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([str(VENV_PYTHON), "-m", "pip", "install", "-r", str(BASE_DIR / "backend" / "requirements.txt")])
    else:
        print("[1/3] Virtual environment ready.")

    print("[2/3] Verifying local AI CLIP model weights...")
    try:
        subprocess.check_call([str(VENV_PYTHON), str(BASE_DIR / "backend" / "download_model.py")])
    except Exception as e:
        print(f"Model verification notice: {e}")

def main():
    print("=" * 65)
    print("       ZariVision AI - Local Offline Recommendation Engine")
    print("=" * 65)

    setup_environment()

    has_npm = shutil.which("npm") is not None
    print("[3/3] Starting servers...")

    if sys.platform == "win32":
        if has_npm:
            frontend_dir = BASE_DIR / "frontend"
            if not (frontend_dir / "node_modules").exists():
                print("Installing React frontend dependencies...")
                subprocess.run(["npm", "install"], cwd=str(frontend_dir), shell=True)

            print("Launching FastAPI Backend (Port 8008) in separate window...")
            backend_cmd = f'Start-Process powershell -ArgumentList "-NoExit", "-Command", "& \'{VENV_PYTHON}\' -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8008 --reload"'
            subprocess.run(["powershell", "-Command", backend_cmd], cwd=str(BASE_DIR))

            print("Launching React Frontend (Port 5173) in separate window...")
            frontend_cmd = f'Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location \'{frontend_dir}\'; npm run dev"'
            subprocess.run(["powershell", "-Command", frontend_cmd], cwd=str(BASE_DIR))

            app_url = "http://localhost:5173"
        else:
            print("[INFO] Node.js not detected: Serving built React UI directly via FastAPI on Port 8008!")
            backend_cmd = f'Start-Process powershell -ArgumentList "-NoExit", "-Command", "& \'{VENV_PYTHON}\' -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8008"'
            subprocess.run(["powershell", "-Command", backend_cmd], cwd=str(BASE_DIR))
            app_url = "http://localhost:8008"
    else:
        if has_npm:
            frontend_dir = BASE_DIR / "frontend"
            if not (frontend_dir / "node_modules").exists():
                subprocess.run(["npm", "install"], cwd=str(frontend_dir))
            backend_proc = subprocess.Popen([str(VENV_PYTHON), "-m", "uvicorn", "app.main:app", "--app-dir", "backend", "--host", "0.0.0.0", "--port", "8008", "--reload"])
            frontend_proc = subprocess.Popen(["npm", "run", "dev"], cwd=str(frontend_dir))
            app_url = "http://localhost:5173"
        else:
            backend_proc = subprocess.Popen([str(VENV_PYTHON), "-m", "uvicorn", "app.main:app", "--app-dir", "backend", "--host", "0.0.0.0", "--port", "8008"])
            app_url = "http://localhost:8008"

    time.sleep(3)
    try:
        webbrowser.open(app_url)
    except Exception:
        pass

    print("-" * 65)
    print(f"[READY] ZariVision AI running at {app_url}")
    print("=" * 65)

if __name__ == "__main__":
    main()
