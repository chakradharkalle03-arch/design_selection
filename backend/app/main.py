import sys
from pathlib import Path

# Ensure backend directory is in sys.path for app module imports
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import STORAGE_DIR, CORS_ORIGINS
from app.database.database import engine, Base, SessionLocal
from app.database.seeder import seed_existing_catalog_designs
from app.api.upload import router as upload_router
from app.api.designs import router as designs_router
from app.api.recommendations import router as rec_router
from app.api.feedback import router as feedback_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB tables
    print("Initializing Database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database ready.")
    
    # Auto-seed existing catalog images
    try:
        db = SessionLocal()
        seed_existing_catalog_designs(db)
        db.close()
    except Exception as e:
        print(f"Catalog seeding warning: {e}")

    # Pre-load local AI CLIP model for immediate offline inference
    try:
        from app.ai.clip_model import clip_engine
        print("[AI Model] Pre-loading local AI CLIP model into memory...")
        clip_engine.load_local_model()
    except Exception as e:
        print(f"[AI Model] Model pre-load notice: {e}")

    yield

app = FastAPI(
    title="Saree & Blouse Embroidery AI Recommendation API",
    description="Multi-factor visual + color + fabric + style AI matching engine for Indian saree & blouse embroidery patterns.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS if CORS_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static file storage for serving uploaded & catalog images
app.mount("/storage", StaticFiles(directory=str(STORAGE_DIR)), name="storage")

# Include Routers
app.include_router(upload_router)
app.include_router(designs_router)
app.include_router(rec_router)
app.include_router(feedback_router)

@app.get("/api/health", tags=["Health"])
@app.head("/api/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "Embroidery AI Backend",
        "engine": "Local PyTorch CLIP + LAB Color Harmony + Fabric Analyzer"
    }

# Check if production frontend build is available to serve directly
from fastapi.responses import FileResponse
frontend_dist = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"

if frontend_dist.exists() and (frontend_dist / "index.html").exists():
    if (frontend_dist / "assets").exists():
        app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_spa(full_path: str):
        file_path = frontend_dist / full_path
        if full_path and file_path.is_file():
            return FileResponse(str(file_path))
        return FileResponse(str(frontend_dist / "index.html"))
else:
    @app.get("/", tags=["Health"])
    @app.head("/", tags=["Health"])
    def root_health():
        return {
            "status": "healthy",
            "service": "Embroidery AI Backend",
            "engine": "Local PyTorch CLIP + LAB Color Harmony + Fabric Analyzer"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8008, reload=True)
