from typing import List, Dict, Any
from app.ai.fabric_classifier import calculate_fabric_compatibility, calculate_style_compatibility

class FabricTextureAgent:
    """
    SPECIALIZED SUB-AGENT 3: Fabric & Texture Density Agent
    Evaluates fabric weight, density, and structural threadwork compatibility (Silk, Satin, Velvet, Organza, Cotton).
    """
    def __init__(self):
        self.name = "Fabric & Texture Agent"
        self.code = "FABRIC_AGENT"

    def evaluate(self, garment_fabric: str, garment_style: str, design_suitable_fabrics: List[str], design_style: str, design_category: str) -> Dict[str, Any]:
        f_score = calculate_fabric_compatibility(garment_fabric, design_suitable_fabrics)
        s_score = calculate_style_compatibility(garment_style, design_style, design_category)

        combined = (f_score * 0.6) + (s_score * 0.4)
        
        if f_score >= 90:
            rationale = f"Optimal embroidery threadwork density for {garment_fabric} fabric"
        else:
            rationale = f"Suitable threadwork balance for {garment_fabric} fabric"

        return {
            "agent": self.name,
            "score": round(combined, 1),
            "fabric_score": round(f_score, 1),
            "style_score": round(s_score, 1),
            "rationale": rationale
        }
