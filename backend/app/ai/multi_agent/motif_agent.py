from typing import Dict, Any
from app.ai.motif_classifier import calculate_motif_similarity

class MotifPatternAgent:
    """
    SPECIALIZED SUB-AGENT 1: Motif & Print Pattern Agent
    Analyzes saree / blouse print design (Floral, Peacock, Paisley, Temple Border, Heavy Zari, Cutwork)
    and computes structural pattern compatibility.
    """
    def __init__(self):
        self.name = "Motif & Print Pattern Agent"
        self.code = "MOTIF_AGENT"

    def evaluate(self, garment_motif: Dict[str, Any], design_motif: Dict[str, Any]) -> Dict[str, Any]:
        score = calculate_motif_similarity(garment_motif, design_motif)
        
        g_label = garment_motif.get("label", "Floral Print")
        d_label = design_motif.get("label", "Embroidery Motif")
        
        if score >= 90:
            rationale = f"Excellent motif alignment: {g_label} print pairs seamlessly with {d_label} embroidery"
        elif score >= 80:
            rationale = f"Harmonious motif pairing between {g_label} saree print and {d_label} embroidery"
        else:
            rationale = f"Moderate pattern contrast between {g_label} and {d_label}"

        return {
            "agent": self.name,
            "score": round(score, 1),
            "rationale": rationale,
            "garment_motif": g_label,
            "design_motif": d_label
        }
