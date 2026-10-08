import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
STORAGE_DIR = BASE_DIR / "storage"
DESIGNS_DIR = STORAGE_DIR / "designs"
UPLOADS_DIR = STORAGE_DIR / "customer_uploads"

# Ensure storage directories exist
DESIGNS_DIR.mkdir(parents=True, exist_ok=True)
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/embroidery.db")
HF_TOKEN = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_HUB_TOKEN")
MODEL_NAME = os.getenv("MODEL_NAME", "openai/clip-vit-base-patch32")
LOW_MEMORY_MODE = os.getenv("LOW_MEMORY_MODE", "true").lower() in ("true", "1", "yes")
CORS_ORIGINS = [
    origin.strip() for origin in os.getenv("CORS_ORIGINS", "*").split(",") if origin.strip()
]
