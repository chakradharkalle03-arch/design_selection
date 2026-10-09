import os
from pathlib import Path
from sqlalchemy.orm import Session
from app.config import DESIGNS_DIR
from app.models.design import Design
from app.ai.color_analyzer import extract_dominant_colors
from app.ai.clip_model import clip_engine

def seed_existing_catalog_designs(db: Session):
    """
    Scans DESIGNS_DIR for any pre-loaded catalog images and populates
    them into the database if not already present.
    """
    if not DESIGNS_DIR.exists():
        return

    valid_exts = {".jpg", ".jpeg", ".png", ".webp"}
    image_files = [
        f for f in DESIGNS_DIR.iterdir()
        if f.is_file() and f.suffix.lower() in valid_exts and not f.name.endswith("_raw.pdf")
    ]

    if not image_files:
        return

    added_count = 0
    for img_path in image_files:
        file_name = img_path.name
        code = img_path.stem.replace("_", "-")
        
        existing = db.query(Design).filter(Design.design_code == code).first()
        if existing:
            continue

        try:
            colors = extract_dominant_colors(str(img_path), k=4)
            embedding = clip_engine.generate_image_embedding(str(img_path))
            image_url = f"/storage/designs/{file_name}"
            name = code.replace("CATALOG-", "Catalog ").replace("-P", " Page ").replace("-", " ")

            design = Design(
                design_code=code,
                name=name,
                image_url=image_url,
                category="Traditional",
                style="Floral",
                colors=colors,
                fabric_suitable=["silk-like", "satin-like", "brocade-like"],
                placement="Full Blouse",
                description=f"Authentic embroidery design pattern from {name}",
                embedding=embedding
            )
            db.add(design)
            added_count += 1
        except Exception as e:
            print(f"Error seeding design {file_name}: {e}")

    if added_count > 0:
        db.commit()
        print(f"✅ Successfully auto-seeded {added_count} shop catalog designs into database!")
