import os
import sys
from pathlib import Path

backend_dir = Path(__file__).resolve().parent.parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from app.database.database import SessionLocal
from app.models.design import Design
from app.ai.embedding import cosine_similarity

def clean_duplicates():
    print("Scanning embroidery design library for duplicate entries...")
    db = SessionLocal()
    try:
        all_designs = db.query(Design).order_by(Design.id.asc()).all()
        seen_images = set()
        seen_embeddings = []
        deleted_count = 0

        for d in all_designs:
            is_dup = False

            # 1. Exact image URL / file name match
            if d.image_url in seen_images:
                is_dup = True
            
            # 2. Embedding similarity > 92% match
            elif d.embedding:
                for prev_id, prev_emb in seen_embeddings:
                    sim = cosine_similarity(d.embedding, prev_emb)
                    if sim > 0.92:
                        is_dup = True
                        print(f"Design {d.id} ({d.design_code}) is visually identical (similarity={sim:.2f}) to Design {prev_id}. Deleting duplicate.")
                        break

            if is_dup:
                db.delete(d)
                deleted_count += 1
            else:
                seen_images.add(d.image_url)
                if d.embedding:
                    seen_embeddings.append((d.id, d.embedding))

        db.commit()
        print(f"Cleanup complete! Removed {deleted_count} duplicate design entries.")

    except Exception as e:
        db.rollback()
        print(f"Error cleaning duplicates: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    clean_duplicates()
