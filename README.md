# ZariVision AI — Saree & Blouse Embroidery Recommendation Engine

An AI-powered web application built specifically for saree and blouse embroidery businesses. Rather than asking a generic LLM to pick a design, ZariVision AI runs a multi-factor recommendation pipeline that extracts garment characteristics (dominant colors in CIE LAB space, fabric texture, style) and calculates weighted compatibility against pre-computed embroidery embeddings to return the **Top 4 best designs with explicit rationale**.

---

## ⚡ 1-Click Quick Start (Zero Friction)

Anyone who clones this repository can launch the entire application with a single command or double-click.

### Step 1: Clone the repository
```bash
git clone https://github.com/chakradharkalle03-arch/design_selection.git
cd design_selection
```

### Step 2: Run with 1-Click

#### 🪟 Windows (Recommended)
Simply **double-click** `run.bat` or in Command Prompt / PowerShell:
```cmd
run.bat
```
*(This automatically creates the Python virtual environment, installs packages, downloads the local AI model, and opens your browser).*

#### 🐧 Linux & 🍎 macOS
```bash
chmod +x run.sh
./run.sh
```

#### 🐍 Any Platform (via Python)
```bash
python run.py
```

#### 🐳 Docker (Optional)
```bash
docker compose up --build
```

---

## 🤖 100% Local Offline AI Model (No API Key Required)

- **Engine**: Local PyTorch Hugging Face CLIP (`openai/clip-vit-base-patch32`).
- **Zero API Dependency**: Computations run 100% locally on your machine (CPU or GPU).
- **No Token Needed**: Does not require any Hugging Face token, payment, or cloud router.
- **Pre-download Helper**: Model weights (~600MB) download automatically on first run, or you can pre-download them with:
  ```bash
  python backend/download_model.py
  ```
- **Instant Matching**: Pre-computes 512-dim visual and style embeddings so matching is fast (<100ms).

---

## 💡 Zero-Node.js Requirement for End Users

- **Production Frontend Included**: The repository contains pre-built frontend assets in `frontend/dist`.
- If **Node.js** is installed on the machine, `run.bat` launches both the FastAPI backend (`http://localhost:8008`) and the React Vite dev server (`http://localhost:5173`) with live hot-reloading.
- If **Node.js is NOT installed**, FastAPI serves the complete interactive React UI directly on `http://localhost:8008`. You only need Python to run the full application!

---

## 🌟 Key Features

1. **Multi-Factor Recommendation Engine**:
   $$\text{Final Score} = 40\% \times \text{Visual Similarity (CLIP)} + 30\% \times \text{Color Harmony (LAB)} + 15\% \times \text{Fabric Fit} + 15\% \times \text{Style Fit}$$
2. **Pre-Computed Design Catalog**: Generates 512-dim feature vectors upon admin catalog upload for instantaneous customer matching.
3. **LAB Color Harmony & Zari Analysis**: Uses CIE LAB perceptual distance ($\Delta E$) and traditional embroidery contrast rules (e.g., Gold Zari boost on Maroon/Dark Blue silk).
4. **Interactive Customer Studio**: Step-by-step UI for garment upload, color palette breakdown, Top 4 match cards with score breakdown bars, and feedback loop (👍 / 👎).
5. **Multi-File & PDF Catalog Importer**: Ingest entire design books from single or multi-page PDFs with live progress tracking.
6. **Candidate Batch Consultation**: Compare an uploaded blouse against specific subsets of designs chosen by the shop owner or customer.
7. **Analytics & Feedback Log**: Track customer approval ratings and reason breakdowns for future preference learning.

---

## 🛠️ Manual Developer Setup

If you prefer to run backend and frontend separately:

### Backend Setup (FastAPI + Local CLIP)
```bash
# Navigate to project root
cd design_selection

# Setup and activate virtualenv
python -m venv backend/venv
# Windows:
.\backend\venv\Scripts\activate
# Linux/macOS:
source backend/venv/bin/activate

# Install backend dependencies
pip install -r backend/requirements.txt

# Download / verify local AI model
python backend/download_model.py

# Start FastAPI server on port 8008
uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8008 --reload
```
API Documentation is available at: `http://127.0.0.1:8008/docs`

### Frontend Setup (React + Vite)
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at: `http://localhost:5173` (proxies `/api` requests to backend on port 8008).

---

## 📂 Project Structure

```
design_selection/
├── backend/
│   ├── app/
│   │   ├── ai/
│   │   │   ├── clip_model.py         # Local PyTorch CLIP vision & text embedding engine
│   │   │   ├── color_analyzer.py     # K-Means & LAB color harmony Delta E
│   │   │   ├── fabric_classifier.py  # Fabric texture analysis
│   │   │   ├── file_helper.py        # PDF & Multi-page image extractor
│   │   │   └── embedding.py          # Vector cosine similarity
│   │   ├── api/
│   │   │   ├── upload.py             # Customer blouse/saree analysis endpoint
│   │   │   ├── designs.py            # Design catalog management & PDF importer
│   │   │   ├── recommendations.py    # Top 4 matching recommendation router
│   │   │   └── feedback.py           # Customer feedback loop
│   │   ├── database/                 # SQLAlchemy database & catalog seeder
│   │   ├── models/                   # Database schemas
│   │   └── main.py                   # FastAPI server & SPA static host
│   ├── download_model.py             # Local CLIP model downloader & verification
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/               # Navbar, match cards, modals
│   │   ├── pages/                    # SinglePageStudio, Catalog, Batch Consultation
│   │   └── services/api.js           # API communication client
│   ├── dist/                         # Pre-built production frontend
│   └── package.json
├── storage/                          # Local designs, catalog, and customer uploads
├── run.bat                           # 1-Click Windows Launcher
├── run.sh                            # 1-Click Linux/macOS Launcher
├── run.py                            # 1-Click Python Launcher
├── docker-compose.yml
└── README.md
```

---

## 📄 License
MIT License. Created for Saree & Blouse Embroidery Businesses.
