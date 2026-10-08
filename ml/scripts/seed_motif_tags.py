import sys
import os
from pathlib import Path

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding="utf-8")

sys.path.append(str(Path(__file__).resolve().parent.parent.parent / "backend"))

from app.database.database import SessionLocal
from app.models.design import Design
from app.ai.motif_classifier import classify_garment_motif
from app.config import DESIGNS_DIR

def seed_design_motifs():
    db = SessionLocal()
    designs = db.query(Design).all()
    print(f"Classifying print motifs for {len(designs)} designs...")

    updated = 0
    for d in designs:
        if d.image_url:
            filename = Path(d.image_url).name
            img_path = DESIGNS_DIR / filename
            if img_path.exists():
                motif_info = classify_garment_motif(str(img_path))
                setattr(d, "motif_info", motif_info)
                updated += 1

    db.commit()
    print(f"Successfully attached motif classifications to {updated} library designs!")

if __name__ == "__main__":
    seed_design_motifs()
