from typing import List, Dict, Any
from app.ai.color_analyzer import calculate_deep_palette_harmony

class ColorHarmonyAgent:
    """
    SPECIALIZED SUB-AGENT 2: Color Harmony & Contrast Agent
    Evaluates CIE LAB perceptual color distance, metallic zari pop, and Indian sari color pairing rules.
    """
    def __init__(self):
        self.name = "Color Harmony & Contrast Agent"
        self.code = "COLOR_AGENT"

    def evaluate(self, garment_colors: List[Dict[str, Any]], design_colors: List[Dict[str, Any]]) -> Dict[str, Any]:
        score, details = calculate_deep_palette_harmony(garment_colors, design_colors)
        
        blouse_c = details.get("blouse_primary", "Blouse Base")
        accent_c = details.get("design_accent", "Embroidery Accents")
        has_zari = details.get("has_zari", False)
        delta_l = details.get("delta_l", 30.0)

        if has_zari:
            rationale = f"Vibrant metallic zari contrast highlighting {blouse_c} fabric with {accent_c}"
        elif delta_l > 30:
            rationale = f"High perceptual contrast (Delta-L = {delta_l}) popping against {blouse_c} fabric"
        else:
            rationale = f"Harmonious color pairing between {blouse_c} and {accent_c}"

        return {
            "agent": self.name,
            "score": round(score, 1),
            "rationale": rationale,
            "details": details
        }
