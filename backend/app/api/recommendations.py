from typing import Optional, List
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.design import GarmentUpload, Design
from app.services.recommendation_service import rank_embroidery_designs

router = APIRouter(prefix="/api/recommend", tags=["Recommendation Engine"])

class RecommendRequest(BaseModel):
    upload_id: str
    customer_requirements: Optional[str] = None  # Custom user text prompt requirements
    design_ids: Optional[List[int]] = None
    top_k: Optional[int] = 4

@router.post("")
def recommend_designs(
    payload: RecommendRequest,
    db: Session = Depends(get_db)
):
    """
    Main Recommendation API:
    Compares customer blouse/saree upload against pre-computed embroidery embeddings,
    evaluates LAB color contrast, fabric texture, AND customer text requirements prompt.
    Returns Top 4 matching embroidery designs with reasons.
    """
    garment = db.query(GarmentUpload).filter(GarmentUpload.id == payload.upload_id).first()
    if not garment:
        raise HTTPException(status_code=404, detail="Garment upload session not found.")

    query = db.query(Design)
    if payload.design_ids and len(payload.design_ids) > 0:
        query = query.filter(Design.id.in_(payload.design_ids))
    
    candidate_designs = query.all()

    if not candidate_designs:
        raise HTTPException(status_code=400, detail="No embroidery designs available in library to match.")

    garment_analysis = {
        "embedding": garment.embedding,
        "colors": garment.colors,
        "fabric": garment.fabric,
        "style": garment.style
    }

    results = rank_embroidery_designs(
        garment_analysis=garment_analysis,
        candidate_designs=candidate_designs,
        customer_requirements=payload.customer_requirements,
        top_k=payload.top_k or 4
    )

    return {
        "session_id": garment.id,
        "customer_requirements": payload.customer_requirements,
        "garment": {
            "image_url": garment.image_url,
            "type": garment.garment_type,
            "colors": garment.colors,
            "fabric": garment.fabric,
            "style": garment.style
        },
        "total_library_designs_analyzed": len(candidate_designs),
        "top_recommendations": results
    }


@router.post("/all")
def recommend_all_library(
    upload_id: str,
    customer_requirements: Optional[str] = None,
    top_k: int = 4,
    db: Session = Depends(get_db)
):
    """Convenience endpoint to match against entire shop design library."""
    req = RecommendRequest(
        upload_id=upload_id,
        customer_requirements=customer_requirements,
        top_k=top_k
    )
    return recommend_designs(payload=req, db=db)
