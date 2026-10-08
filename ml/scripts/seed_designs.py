import os
import sys
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from app.config import DESIGNS_DIR
from app.database.database import engine, Base, SessionLocal
from app.models.design import Design
from app.ai.clip_model import clip_engine
from app.ai.color_analyzer import extract_dominant_colors

def create_sample_embroidery_image(filepath: str, bg_color: tuple, accent_colors: list, pattern_type: str = "floral"):
    """Generates a high-quality stylized sample embroidery design image."""
    img = Image.new("RGB", (600, 600), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Draw embroidery patterns
    if pattern_type == "floral":
        # Central neck motif + flowers
        for i in range(5):
            angle = i * (360 / 5)
            rad = np.radians(angle)
            cx, cy = 300 + int(120 * np.cos(rad)), 300 + int(120 * np.sin(rad))
            draw.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], outline=accent_colors[0], width=6)
            draw.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=accent_colors[1] if len(accent_colors) > 1 else accent_colors[0])
        # Border zari lines
        draw.arc([100, 100, 500, 500], start=0, end=360, fill=accent_colors[0], width=8)

    elif pattern_type == "peacock":
        # Paisley / peacock motif curve
        draw.polygon([(300, 150), (450, 300), (350, 480), (250, 450), (200, 300)], outline=accent_colors[0], fill=accent_colors[0])
        draw.ellipse([260, 220, 380, 340], fill=accent_colors[1] if len(accent_colors) > 1 else accent_colors[0])
        draw.arc([50, 50, 550, 550], start=45, end=135, fill=accent_colors[0], width=12)

    elif pattern_type == "temple":
        # Triangular temple border
        for x in range(50, 550, 80):
            draw.polygon([(x, 500), (x + 40, 420), (x + 80, 500)], fill=accent_colors[0], outline=accent_colors[1] if len(accent_colors) > 1 else accent_colors[0])
            draw.polygon([(x, 100), (x + 40, 180), (x + 80, 100)], fill=accent_colors[0])

    else:  # Minimalist / geometric
        draw.rectangle([150, 150, 450, 450], outline=accent_colors[0], width=10)
        draw.line([(150, 150), (450, 450)], fill=accent_colors[1] if len(accent_colors) > 1 else accent_colors[0], width=6)
        draw.line([(450, 150), (150, 450)], fill=accent_colors[1] if len(accent_colors) > 1 else accent_colors[0], width=6)

    img.save(filepath, quality=95)


SEED_DATA = [
    {
        "design_code": "EMB-0027",
        "name": "Royal Gold Zari Neckline",
        "category": "Bridal",
        "style": "Heavy Zari",
        "placement": "Neck",
        "description": "Exquisite gold zari floral embroidery around the neckline, ideal for rich silk bridal blouses.",
        "bg_color": (107, 30, 45),  # Deep Maroon
        "accent_colors": [(212, 175, 55), (220, 20, 60)],  # Gold Zari, Crimson
        "fabric_suitable": ["silk-like", "satin-like", "brocade-like"],
        "pattern_type": "floral"
    },
    {
        "design_code": "EMB-0011",
        "name": "Peacock & Paisley Border",
        "category": "Traditional",
        "style": "Peacock",
        "placement": "Sleeve",
        "description": "Vibrant peacock motif embedded with gold thread and royal blue accents.",
        "bg_color": (0, 106, 78),  # Bottle Green
        "accent_colors": [(212, 175, 55), (65, 105, 225)],  # Gold, Royal Blue
        "fabric_suitable": ["silk-like", "georgette-like", "cotton-like"],
        "pattern_type": "peacock"
    },
    {
        "design_code": "EMB-0043",
        "name": "Lotus Temple Motif",
        "category": "Temple",
        "style": "Floral",
        "placement": "Back",
        "description": "Elegant lotus threadwork with classic South Indian temple border geometry.",
        "bg_color": (255, 0, 127),  # Rani Pink
        "accent_colors": [(225, 173, 1), (255, 253, 208)],  # Mustard Gold, Ivory
        "fabric_suitable": ["silk-like", "satin-like"],
        "pattern_type": "temple"
    },
    {
        "design_code": "EMB-0008",
        "name": "Subtle Pearl Minimalist",
        "category": "Minimal",
        "style": "Minimalistic",
        "placement": "Sleeve",
        "description": "Delicate subtle silver and gold pearl highlights suited for pastel blouses.",
        "bg_color": (255, 192, 203),  # Baby Pink
        "accent_colors": [(192, 192, 192), (212, 175, 55)],  # Silver, Gold
        "fabric_suitable": ["georgette-like", "net", "silk-like"],
        "pattern_type": "geometric"
    },
    {
        "design_code": "EMB-0015",
        "name": "Heavy Kundan Back Feature",
        "category": "Bridal",
        "style": "Heavy Zari",
        "placement": "Full Blouse",
        "description": "Opulent full-back embroidery featuring gold wire zari work and ruby red stones.",
        "bg_color": (0, 0, 128),  # Navy Blue
        "accent_colors": [(212, 175, 55), (220, 20, 60)],  # Gold, Crimson
        "fabric_suitable": ["silk-like", "velvet-like", "brocade-like"],
        "pattern_type": "floral"
    },
    {
        "design_code": "EMB-0032",
        "name": "South Indian Zari Border",
        "category": "Traditional",
        "style": "Heavy Zari",
        "placement": "Border",
        "description": "Traditional gold zari border with maroon accent highlights.",
        "bg_color": (225, 173, 1),  # Mustard Yellow
        "accent_colors": [(128, 0, 0), (212, 175, 55)],  # Maroon, Gold
        "fabric_suitable": ["brocade-like", "silk-like"],
        "pattern_type": "temple"
    }
]

def seed_database():
    print("Starting embroidery design library database seeding...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        for item in SEED_DATA:
            existing = db.query(Design).filter(Design.design_code == item["design_code"]).first()
            if existing:
                print(f"Design {item['design_code']} already exists. Skipping.")
                continue

            filename = f"{item['design_code']}.jpg"
            file_path = DESIGNS_DIR / filename

            # Create image
            create_sample_embroidery_image(
                str(file_path),
                bg_color=item["bg_color"],
                accent_colors=item["accent_colors"],
                pattern_type=item["pattern_type"]
            )

            # Analyze colors & precompute embedding
            colors = extract_dominant_colors(str(file_path), k=4)
            embedding = clip_engine.generate_image_embedding(str(file_path))
            image_url = f"/storage/designs/{filename}"

            design = Design(
                design_code=item["design_code"],
                name=item["name"],
                image_url=image_url,
                category=item["category"],
                style=item["style"],
                placement=item["placement"],
                description=item["description"],
                colors=colors,
                fabric_suitable=item["fabric_suitable"],
                embedding=embedding
            )
            db.add(design)
            print(f"Successfully created design {item['design_code']} with AI pre-computed embedding.")

        db.commit()
        print("Database seeding completed successfully.")

    except Exception as e:
        db.rollback()
        print(f"Seeding failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
