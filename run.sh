#!/usr/bin/env bash
set -e

echo "===================================================================="
echo "                ZARIVISION AI - ONE-CLICK LAUNCHER"
echo "===================================================================="
echo ""

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$BASE_DIR"

# 1. Check Python
PYTHON_CMD=""
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo "[ERROR] Python 3 was not found! Please install Python 3.10+."
    exit 1
fi

echo "[1/4] Found Python: $PYTHON_CMD ($($PYTHON_CMD --version))"

# 2. Virtual Environment
VENV_DIR="$BASE_DIR/backend/venv"
VENV_PYTHON="$VENV_DIR/bin/python"

if [ ! -f "$VENV_PYTHON" ]; then
    echo "[2/4] Creating Python virtual environment in backend/venv..."
    $PYTHON_CMD -m venv "$VENV_DIR"
    echo "[2/4] Installing backend and AI requirements..."
    "$VENV_PYTHON" -m pip install --upgrade pip
    "$VENV_PYTHON" -m pip install -r "$BASE_DIR/backend/requirements.txt"
else
    echo "[2/4] Python virtual environment ready."
fi

# 3. Download & Verify Local Model
echo "[3/4] Verifying local AI model (openai/clip-vit-base-patch32)..."
"$VENV_PYTHON" "$BASE_DIR/backend/download_model.py"

# 4. Start Servers
echo "[4/4] Starting application servers..."
if command -v npm &>/dev/null; then
    if [ ! -d "$BASE_DIR/frontend/node_modules" ]; then
        echo "Installing frontend dependencies..."
        (cd "$BASE_DIR/frontend" && npm install)
    fi

    echo "Starting FastAPI Backend on port 8008..."
    "$VENV_PYTHON" -m uvicorn app.main:app --app-dir "$BASE_DIR/backend" --host 0.0.0.0 --port 8008 --reload &
    BACKEND_PID=$!

    echo "Starting React Frontend on port 5173..."
    (cd "$BASE_DIR/frontend" && npm run dev -- --host 0.0.0.0) &
    FRONTEND_PID=$!

    sleep 3
    URL="http://localhost:5173"
else
    echo "[INFO] Node.js not detected. Serving production React build directly via FastAPI!"
    "$VENV_PYTHON" -m uvicorn app.main:app --app-dir "$BASE_DIR/backend" --host 0.0.0.0 --port 8008 &
    BACKEND_PID=$!

    sleep 3
    URL="http://localhost:8008"
fi

echo ""
echo "===================================================================="
echo " SUCCESS: ZariVision AI is running at: $URL"
echo " Press Ctrl+C to stop all servers."
echo "===================================================================="

# Open browser if desktop environment available
if command -v xdg-open &>/dev/null; then
    xdg-open "$URL" &>/dev/null || true
elif command -v open &>/dev/null; then
    open "$URL" &>/dev/null || true
fi

trap "kill $BACKEND_PID ${FRONTEND_PID:-} 2>/dev/null || true; exit 0" SIGINT SIGTERM
wait
