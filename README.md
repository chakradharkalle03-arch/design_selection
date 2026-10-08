# ZariVision AI — Saree & Blouse Embroidery Recommendation Engine

An AI-powered web application built specifically for saree and blouse embroidery businesses. Rather than asking a generic LLM to pick a design, ZariVision AI runs a multi-factor recommendation pipeline that extracts garment characteristics (dominant colors in LAB space, fabric texture, style) and calculates weighted compatibility against pre-computed embroidery embeddings to return the **Top 4 best designs with explicit rationale**.

---

## 🌟 Key Features

1. **Multi-Factor Recommendation Engine**:
   $$\text{Final Score} = 40\% \times \text{Visual Similarity (CLIP)} + 30\% \times \text{Color Harmony (LAB)} + 15\% \times \text{Fabric Fit} + 15\% \times \text{Style Fit}$$
2. **Pre-Computed Design Library**: Generates 512-dim feature vectors upon admin upload so customer query matching takes under **100ms**.
3. **LAB Color Harmony & Zari Analysis**: Uses CIE LAB perceptual distance ($\Delta E$) and traditional embroidery contrast rules (e.g., Gold Zari boost on Maroon/Dark Blue silk).
4. **Interactive Customer Studio**: Step-by-step UI for garment upload, color palette breakdown, Top 4 match cards with score breakdown bars, and active feedback loop (👍 / 👎).
5. **Candidate Batch Consultation (Mode B)**: Compare an uploaded blouse against a specific subset of designs selected by the shop owner or customer.
6. **Analytics & Feedback Log**: Track approval ratings and reason breakdowns for future model fine-tuning.

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- **Python 3.11+**
- **Node.js v18+**

### 1. Backend Setup (FastAPI + AI Engine)

```bash
# Navigate to project root
cd design_selection

# Activate Python environment
.\backend\venv\Scripts\activate

# Install dependencies (if not already installed)
pip install -r backend/requirements.txt

# Seed sample database & precompute embeddings
python ml/scripts/seed_designs.py

# Start FastAPI server
uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload
```

FastAPI server runs at `http://127.0.0.1:8000`. API docs available at `http://127.0.0.1:8000/docs`.

### 2. Frontend Setup (React + Vite)

```bash
# In a new terminal tab
cd frontend

# Install dependencies
npm install

# Start Vite dev server
npm run dev
```

Frontend application runs at `http://localhost:5173`.

---

## 🐳 Docker & Oracle Cloud Deployment

To deploy on local Docker or Oracle Cloud Free ARM VM:

```bash
# Build and run containers
docker-compose up --build -d
```

Nginx will serve the application on port `80`, proxying requests to the FastAPI backend container on port `8000`.

---

## 📂 Project Structure

```
design_selection/
├── backend/
│   ├── app/
│   │   ├── ai/
│   │   │   ├── clip_model.py         # HuggingFace CLIP vision embedding engine
│   │   │   ├── color_analyzer.py      # K-Means & LAB color harmony Delta E
│   │   │   ├── fabric_classifier.py   # Fabric texture analysis
│   │   │   └── embedding.py           # Cosine similarity vector utility
│   │   ├── api/
│   │   │   ├── upload.py              # Garment analysis endpoint
│   │   │   ├── designs.py             # Design library management
│   │   │   ├── recommendations.py     # Top 4 matching recommendation router
│   │   │   └── feedback.py            # Active learning feedback collector
│   │   ├── models/                    # SQLAlchemy database models
│   │   └── main.py                    # Main FastAPI app entry point
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/                # React UI components
│   │   ├── pages/                     # Studio, Library, Batch, Admin pages
│   │   ├── services/api.js            # Axios client
│   │   ├── App.jsx
│   │   └── index.css                  # Dark luxury theme CSS
│   ├── package.json
│   └── vite.config.js
├── storage/
│   ├── designs/                       # Stored embroidery pattern images
│   └── customer_uploads/              # Stored customer uploaded blouse photos
├── ml/
│   └── scripts/seed_designs.py        # Database & precomputed embedding seed script
├── docker-compose.yml
├── nginx.conf
└── README.md
```
