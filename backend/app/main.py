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
from app.database.database import engine, Base
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

# Mount static file storage for serving images
app.mount("/storage", StaticFiles(directory=str(STORAGE_DIR)), name="storage")

# Include Routers
app.include_router(upload_router)
app.include_router(designs_router)
app.include_router(rec_router)
app.include_router(feedback_router)

@app.get("/", tags=["Health"])
@app.get("/api/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "Embroidery AI Backend",
        "engine": "CLIP + LAB Color Harmony + Fabric Analyzer"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
