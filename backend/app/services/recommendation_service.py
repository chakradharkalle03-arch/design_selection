import numpy as np
from typing import List, Dict, Any, Optional
from app.ai.embedding import calculate_visual_similarity_score, cosine_similarity
from app.ai.color_analyzer import calculate_deep_palette_harmony
from app.ai.fabric_classifier import calculate_fabric_compatibility, calculate_style_compatibility
from app.ai.clip_model import clip_engine

def generate_dynamic_recommendation_reason(
    final_score: float,
    color_score: float,
    color_analysis: dict,
    fabric_score: float,
    style_score: float,
    prompt_score: float,
    customer_requirements: str,
    garment_colors: list,
    design_name: str,
    design_category: str,
    design_colors: list,
    garment_fabric: str
) -> str:
    """
    Dynamically generates tailored AI rationale combining color contrast, motif texture,
    and customer text prompt requirements.
    """
    blouse_color = color_analysis.get("blouse_primary", "blouse base")
    design_accents = color_analysis.get("design_accent", "embroidery accents")
    delta_e = color_analysis.get("delta_e", 40.0)
    delta_l = color_analysis.get("delta_l", 30.0)
    has_zari = color_analysis.get("has_zari", False)
    is_dark = color_analysis.get("is_dark_blouse", False)

    reasons = []

    if customer_requirements and prompt_score >= 70:
        reasons.append(f"Satisfies requirement ('{customer_requirements[:40]}...')")

    if has_zari:
        reasons.append(f"Luxurious {design_accents} threadwork provides vibrant metallic contrast against {blouse_color} fabric")
    elif delta_l > 30:
        reasons.append(f"Striking visual contrast (Delta-L = {delta_l}) popping against {blouse_color} fabric")
    elif color_score >= 80:
        reasons.append(f"Perceptual color contrast (Delta-E = {delta_e}) highlighting {blouse_color} with {design_accents}")
    else:
        reasons.append(f"Harmonious color pairing between {blouse_color} and {design_accents}")

    if fabric_score >= 90:
        reasons.append(f"Optimal threadwork density for {garment_fabric} fabric")

    return " - ".join(reasons[:2]) + "."


from app.ai.multi_agent.supervisor_agent import supervisor_agent

def rank_embroidery_designs(
    garment_analysis: Dict[str, Any],
    candidate_designs: List[Any],
    customer_requirements: Optional[str] = None,
    top_k: int = 4
) -> List[Dict[str, Any]]:
    """
    MULTI-AGENT SUPERVISOR SELECTION ENGINE:
    Delegates to Supervisor Agent which orchestrates Motif, Color, Fabric, and Prompt Sub-Agents.
    Prioritizes Saree/Blouse Motif & Print Pattern matching (40% weight).
    """
    garment_img_path = ""
    if garment_analysis.get("image_url"):
        img_name = garment_analysis["image_url"].split("/")[-1]
        from app.config import UPLOADS_DIR
        garment_img_path = str(UPLOADS_DIR / img_name)

    return supervisor_agent.run_recommendation_pipeline(
        garment_analysis=garment_analysis,
        garment_image_path=garment_img_path,
        candidate_designs=candidate_designs,
        customer_requirements=customer_requirements,
        top_k=top_k
    )
