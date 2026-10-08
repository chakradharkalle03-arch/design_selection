import uuid
import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import UPLOADS_DIR
from app.database.database import get_db
from app.models.design import GarmentUpload
from app.ai.color_analyzer import extract_dominant_colors
from app.ai.fabric_classifier import classify_fabric_and_style
from app.ai.motif_classifier import classify_garment_motif
from app.ai.clip_model import clip_engine
from app.ai.file_helper import prepare_image_for_analysis

router = APIRouter(prefix="/api", tags=["Garment Upload & Analysis"])

@router.post("/analyze-garment")
async def analyze_garment(
    file: UploadFile = File(...),
    garment_type: str = Form("blouse"),
    db: Session = Depends(get_db)
):
    """
    Step 1 API: Upload customer blouse/saree photo OR PDF catalog page.
    Converts PDF pages automatically to rendered images, extracts dominant colors,
    detects fabric texture & motif print patterns, and generates CLIP embeddings.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Invalid file uploaded.")

    upload_id = f"session_{uuid.uuid4().hex[:10]}"
    ext = Path(file.filename).suffix.lower() or ".jpg"
    raw_filename = f"{upload_id}_raw{ext}"
    img_filename = f"{upload_id}.jpg"

    raw_path = UPLOADS_DIR / raw_filename
    processed_img_path = UPLOADS_DIR / img_filename

    try:
        # Save uploaded raw file (PDF or Image)
        with open(raw_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Convert PDF or normalize image to JPEG for AI pipeline
        prepare_image_for_analysis(str(raw_path), str(processed_img_path))

        # 1. Color extraction on rendered image
        dominant_colors = extract_dominant_colors(str(processed_img_path), k=4)

        # 2. Fabric & style analysis
        fabric_info = classify_fabric_and_style(str(processed_img_path))

        # 3. Motif & Saree Print Pattern Classification
        motif_info = classify_garment_motif(str(processed_img_path))

        # 4. CLIP embedding generation
        embedding = clip_engine.generate_image_embedding(str(processed_img_path))

        image_url = f"/storage/customer_uploads/{img_filename}"

        # Save record in DB
        garment_record = GarmentUpload(
            id=upload_id,
            filename=img_filename,
            image_url=image_url,
            garment_type=garment_type,
            fabric=fabric_info["fabric"],
            style=fabric_info["style"],
            colors=dominant_colors,
            embedding=embedding
        )
        db.add(garment_record)
        db.commit()
        db.refresh(garment_record)

        return {
            "upload_id": garment_record.id,
            "filename": garment_record.filename,
            "image_url": garment_record.image_url,
            "garment_type": garment_record.garment_type,
            "colors": garment_record.colors,
            "fabric": garment_record.fabric,
            "style": garment_record.style,
            "motif": motif_info,
            "confidence": fabric_info["confidence"],
            "is_pdf": ext == ".pdf"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Garment analysis failed: {str(e)}")
