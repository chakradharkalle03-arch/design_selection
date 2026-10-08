import sys
import os
from pathlib import Path

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding="utf-8")

sys.path.append(str(Path(__file__).resolve().parent.parent.parent / "backend"))

from app.database.database import SessionLocal
from app.models.design import Design
from app.ai.color_analyzer import extract_dominant_colors
from app.config import DESIGNS_DIR

def recalculate_all_design_colors():
    db = SessionLocal()
    designs = db.query(Design).all()
    print(f"Recalculating colors for {len(designs)} designs...")

    updated = 0
    for d in designs:
        if d.image_url:
            filename = Path(d.image_url).name
            img_path = DESIGNS_DIR / filename
            if img_path.exists():
                colors = extract_dominant_colors(str(img_path), k=4)
                d.colors = colors
                updated += 1

    db.commit()
    print(f"Successfully updated colors for {updated} library designs!")

if __name__ == "__main__":
    recalculate_all_design_colors()
