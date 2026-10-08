from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.database import get_db
from app.models.design import Feedback

router = APIRouter(prefix="/api/feedback", tags=["Customer & Expert Feedback"])

class FeedbackRequest(BaseModel):
    session_id: str
    design_code: str
    rating: str  # "like" or "dislike"
    reason: Optional[str] = None
    comment: Optional[str] = None

@router.post("")
def submit_feedback(
    payload: FeedbackRequest,
    db: Session = Depends(get_db)
):
    """Record customer or expert feedback on AI recommendations to build future dataset."""
    fb = Feedback(
        session_id=payload.session_id,
        design_code=payload.design_code,
        rating=payload.rating.lower(),
        reason=payload.reason,
        comment=payload.comment
    )
    db.add(fb)
    db.commit()
    db.refresh(fb)

    return {
        "message": "Feedback recorded successfully. Thank you for training our AI engine!",
        "feedback_id": fb.id
    }


@router.get("")
def get_feedback_stats(db: Session = Depends(get_db)):
    """Analytics view for feedback metrics."""
    total = db.query(Feedback).count()
    likes = db.query(Feedback).filter(Feedback.rating == "like").count()
    dislikes = db.query(Feedback).filter(Feedback.rating == "dislike").count()

    # Group by dislike reasons
    reasons = (
        db.query(Feedback.reason, func.count(Feedback.reason))
        .filter(Feedback.rating == "dislike")
        .group_by(Feedback.reason)
        .all()
    )

    return {
        "total_feedback_logs": total,
        "likes": likes,
        "dislikes": dislikes,
        "approval_rate": round((likes / total * 100), 1) if total > 0 else 100.0,
        "dislike_reasons_breakdown": {r[0] or "Unspecified": r[1] for r in reasons}
    }
