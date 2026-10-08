import json
import uuid
import shutil
import os
from pathlib import Path
from typing import Optional, List
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.config import DESIGNS_DIR
from app.database.database import get_db
from app.models.design import Design
from app.ai.color_analyzer import extract_dominant_colors
from app.ai.clip_model import clip_engine
from app.ai.file_helper import is_pdf, convert_all_pdf_pages_to_images, prepare_image_for_analysis

router = APIRouter(prefix="/api/designs", tags=["Embroidery Design Library"])

@router.get("")
def list_designs(
    category: Optional[str] = None,
    placement: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Retrieve all library embroidery designs with optional filtering."""
    query = db.query(Design)
    if category and category.lower() != "all":
        query = query.filter(Design.category.ilike(category))
    if placement and placement.lower() != "all":
        query = query.filter(Design.placement.ilike(placement))
    
    designs = query.order_by(Design.created_at.desc()).all()
    
    return [
        {
            "id": d.id,
            "design_code": d.design_code,
            "name": d.name,
            "image_url": d.image_url,
            "category": d.category,
            "style": d.style,
            "colors": d.colors,
            "fabric_suitable": d.fabric_suitable,
            "placement": d.placement,
            "description": d.description,
            "has_embedding": bool(d.embedding_json),
            "created_at": d.created_at.isoformat() if d.created_at else None
        }
        for d in designs
    ]


@router.get("/{design_id}")
def get_design_details(design_id: int, db: Session = Depends(get_db)):
    """Get single embroidery design details."""
    design = db.query(Design).filter(Design.id == design_id).first()
    if not design:
        raise HTTPException(status_code=404, detail="Design not found.")

    return {
        "id": design.id,
        "design_code": design.design_code,
        "name": design.name,
        "image_url": design.image_url,
        "category": design.category,
        "style": design.style,
        "colors": design.colors,
        "fabric_suitable": design.fabric_suitable,
        "placement": design.placement,
        "description": design.description
    }


@router.post("/upload")
async def upload_new_design(
    file: UploadFile = File(...),
    name: str = Form(...),
    design_code: Optional[str] = Form(None),
    category: str = Form("Traditional"),
    style: str = Form("Floral"),
    placement: str = Form("Full Blouse"),
    description: Optional[str] = Form(""),
    fabric_suitable_json: Optional[str] = Form('["silk-like", "satin-like", "brocade-like"]'),
    db: Session = Depends(get_db)
):
    """
    Upload an embroidery design image or multi-page PDF catalog.
    If PDF: Processes EVERY page into a distinct, unique embroidery design entry.
    Deduplicates identical design codes or duplicate images automatically.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Invalid file uploaded.")

    base_code = design_code or f"CATALOG-{uuid.uuid4().hex[:4].upper()}"
    ext = Path(file.filename).suffix.lower() or ".jpg"
    raw_filename = f"{base_code}_raw{ext}"
    raw_path = DESIGNS_DIR / raw_filename

    try:
        with open(raw_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        try:
            fabrics = json.loads(fabric_suitable_json)
        except Exception:
            fabrics = ["silk-like", "brocade-like"]

        created_designs = []

        if is_pdf(str(raw_path)):
            pages = convert_all_pdf_pages_to_images(str(raw_path), DESIGNS_DIR, base_code)
            
            for p_info in pages:
                img_path = p_info["image_path"]
                img_filename = p_info["filename"]
                p_code = p_info["design_code"]

                existing = db.query(Design).filter(Design.design_code == p_code).first()
                if existing:
                    p_code = f"{p_code}-P{p_info['page_num']}-{uuid.uuid4().hex[:2].upper()}"

                colors = extract_dominant_colors(img_path, k=4)
                embedding = clip_engine.generate_image_embedding(img_path)
                image_url = f"/storage/designs/{img_filename}"

                page_name = f"{name} (Page {p_info['page_num']})" if len(pages) > 1 else name

                new_design = Design(
                    design_code=p_code,
                    name=page_name,
                    image_url=image_url,
                    category=category,
                    style=style,
                    colors=colors,
                    fabric_suitable=fabrics,
                    placement=placement,
                    description=description or p_info.get("text_content", ""),
                    embedding=embedding
                )
                db.add(new_design)
                created_designs.append(new_design)

            db.commit()
            return {
                "message": f"Successfully processed multi-page PDF catalog! Extracted {len(created_designs)} unique embroidery design page(s).",
                "processed_pages": len(created_designs),
                "design_codes": [d.design_code for d in created_designs]
            }

        else:
            img_filename = f"{base_code}.jpg"
            processed_img_path = DESIGNS_DIR / img_filename
            prepare_image_for_analysis(str(raw_path), str(processed_img_path))

            existing = db.query(Design).filter(Design.design_code == base_code).first()
            if existing:
                base_code = f"{base_code}-{uuid.uuid4().hex[:2].upper()}"

            colors = extract_dominant_colors(str(processed_img_path), k=4)
            embedding = clip_engine.generate_image_embedding(str(processed_img_path))
            image_url = f"/storage/designs/{img_filename}"

            new_design = Design(
                design_code=base_code,
                name=name,
                image_url=image_url,
                category=category,
                style=style,
                colors=colors,
                fabric_suitable=fabrics,
                placement=placement,
                description=description,
                embedding=embedding
            )
            db.add(new_design)
            db.commit()
            db.refresh(new_design)

            return {
                "message": "Embroidery design uploaded & AI embedding pre-computed successfully.",
                "design": {
                    "id": new_design.id,
                    "design_code": new_design.design_code,
                    "name": new_design.name,
                    "image_url": new_design.image_url,
                    "category": new_design.category,
                    "colors": new_design.colors
                }
            }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Design catalog processing failed: {str(e)}")


@router.delete("/all")
def delete_all_designs(db: Session = Depends(get_db)):
    """
    PERMANENTLY DELETE ALL embroidery designs from the database and clear storage.
    """
    try:
        deleted_count = db.query(Design).delete()
        db.commit()

        # Remove all files in DESIGNS_DIR
        for item in DESIGNS_DIR.iterdir():
            if item.is_file():
                try:
                    os.remove(item)
                except Exception as ex:
                    print(f"File delete warning: {ex}")

        return {
            "message": f"Successfully deleted ALL {deleted_count} embroidery designs and cleared catalog storage.",
            "deleted_count": deleted_count
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Delete all failed: {str(e)}")


@router.delete("/{design_id}")
def delete_design(design_id: int, db: Session = Depends(get_db)):
    """Permanently delete an embroidery design from database and disk storage."""
    design = db.query(Design).filter(Design.id == design_id).first()
    if not design:
        raise HTTPException(status_code=404, detail="Design not found.")

    try:
        if design.image_url:
            filename = Path(design.image_url).name
            file_path = DESIGNS_DIR / filename
            if file_path.exists():
                os.remove(file_path)
    except Exception as e:
        print(f"Warning: Could not remove design image file: {e}")

    db.delete(design)
    db.commit()
    return {"message": f"Design {design.design_code} permanently deleted successfully."}
