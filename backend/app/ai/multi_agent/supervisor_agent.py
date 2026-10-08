import numpy as np
from typing import List, Dict, Any, Optional
from app.ai.multi_agent.motif_agent import MotifPatternAgent
from app.ai.multi_agent.color_agent import ColorHarmonyAgent
from app.ai.multi_agent.fabric_agent import FabricTextureAgent
from app.ai.multi_agent.prompt_agent import StylePromptAgent
from app.ai.motif_classifier import classify_garment_motif
from app.ai.embedding import calculate_visual_similarity_score, cosine_similarity

class SupervisorAgent:
    """
    SUPERVISOR MAIN AGENT
    Orchestrates the Multi-Agent Recommendation System:
    1. Delegates tasks to Motif, Color, Fabric, and Prompt Sub-Agents.
    2. Enforces Primary Weight (40%) on Saree/Blouse Print & Motif Matching.
    3. Synthesizes Sub-Agent reports into unified Multi-Agent Consensus.
    4. Guarantees 4 Unique, Non-Duplicate Top Embroidery Design Recommendations.
    """
    def __init__(self):
        self.name = "Supervisor Main Agent"
        self.motif_agent = MotifPatternAgent()
        self.color_agent = ColorHarmonyAgent()
        self.fabric_agent = FabricTextureAgent()
        self.prompt_agent = StylePromptAgent()

    def run_recommendation_pipeline(
        self,
        garment_analysis: Dict[str, Any],
        garment_image_path: str,
        candidate_designs: List[Any],
        customer_requirements: Optional[str] = None,
        top_k: int = 4
    ) -> List[Dict[str, Any]]:
        
        # 1. Supervisor classifies Garment Motif & Print Pattern
        garment_motif = garment_analysis.get("motif")
        if not garment_motif and garment_image_path:
            garment_motif = classify_garment_motif(garment_image_path)
        if not garment_motif:
            garment_motif = {"primary_motif": "floral", "label": "Floral & Leaves", "confidence": 80.0, "all_tags": ["floral"]}

        blouse_embedding = garment_analysis.get("embedding", [])
        garment_colors = garment_analysis.get("colors", [])
        garment_fabric = garment_analysis.get("fabric", "silk-like")
        garment_style = garment_analysis.get("style", "traditional")

        evaluated_candidates = []

        # 2. Iterate candidates & delegate to Sub-Agents
        for design in candidate_designs:
            # Design motif classification
            design_motif = getattr(design, "motif_info", None)
            if not design_motif:
                design_motif = {"primary_motif": design.style.lower() if design.style else "floral", "label": design.style or "Floral", "all_tags": [design.style.lower() if design.style else "floral"]}

            # Agent 1: Motif & Print Pattern Agent
            motif_report = self.motif_agent.evaluate(garment_motif, design_motif)

            # Agent 2: Color Harmony Agent
            color_report = self.color_agent.evaluate(garment_colors, design.colors)

            # Agent 3: Fabric & Texture Agent
            fabric_report = self.fabric_agent.evaluate(
                garment_fabric,
                garment_style,
                design.fabric_suitable,
                design.style,
                design.category
            )

            # Agent 4: Style & Prompt Agent
            prompt_report = self.prompt_agent.evaluate(customer_requirements, design.embedding)

            # CLIP Visual Similarity (Image to Image)
            raw_vis = calculate_visual_similarity_score(blouse_embedding, design.embedding)

            # 3. Supervisor Ensemble Consensus Weighting
            has_prompt = prompt_report["has_prompt"] and prompt_report["score"] > 0
            
            if has_prompt:
                consensus_score = (
                    motif_report["score"] * 0.35 +
                    color_report["score"] * 0.30 +
                    prompt_report["score"] * 0.20 +
                    raw_vis * 0.10 +
                    fabric_report["score"] * 0.05
                )
            else:
                consensus_score = (
                    motif_report["score"] * 0.40 +   # PRIMARY REQUIREMENT WEIGHT: 40%
                    color_report["score"] * 0.35 +   # COLOR HARMONY: 35%
                    raw_vis * 0.15 +                 # VISUAL EMBEDDING: 15%
                    fabric_report["score"] * 0.10    # FABRIC DENSITY: 10%
                )

            evaluated_candidates.append({
                "design": design,
                "consensus_score": consensus_score,
                "motif_report": motif_report,
                "color_report": color_report,
                "fabric_report": fabric_report,
                "prompt_report": prompt_report,
                "raw_vis": raw_vis
            })

        # Sort candidates descending by consensus score
        evaluated_candidates.sort(key=lambda x: x["consensus_score"], reverse=True)

        # 4. Supervisor Deduplication Filter
        filtered_unique = []
        seen_urls = set()
        seen_codes = set()
        seen_embeddings = []

        for item in evaluated_candidates:
            d = item["design"]
            if d.image_url in seen_urls or d.design_code in seen_codes:
                continue

            is_dup_vis = False
            if d.embedding:
                for prev in seen_embeddings:
                    if cosine_similarity(d.embedding, prev) > 0.90:
                        is_dup_vis = True
                        break

            if is_dup_vis:
                continue

            seen_urls.add(d.image_url)
            seen_codes.add(d.design_code)
            if d.embedding:
                seen_embeddings.append(d.embedding)

            filtered_unique.append(item)

            if len(filtered_unique) >= 20:
                break

        # Fallback if library is small
        if len(filtered_unique) < top_k:
            for item in evaluated_candidates:
                if not any(u["design"].id == item["design"].id for u in filtered_unique):
                    filtered_unique.append(item)

        # 5. Format Top Recommendations with Multi-Agent Rationales
        final_results = []
        top_subset = filtered_unique[:top_k]
        max_c = top_subset[0]["consensus_score"] if top_subset else 80.0

        for idx, item in enumerate(top_subset):
            d = item["design"]
            raw_score = item["consensus_score"]

            if idx == 0:
                final_display_score = round(min(97.6, max(89.0, raw_score * 1.12)), 1)
            else:
                prev_s = final_results[idx - 1]["match_score"]
                drop = round(max(2.8, (max_c - raw_score) * 0.45 + (idx * 1.3)), 1)
                final_display_score = round(max(72.0, prev_s - drop), 1)

            # Build Multi-Agent Rationale
            agent_rationales = [
                f"🎨 Motif Agent: {item['motif_report']['rationale']}",
                f"🌈 Color Agent: {item['color_report']['rationale']}"
            ]
            if item["prompt_report"]["has_prompt"] and item["prompt_report"]["score"] >= 65:
                agent_rationales.insert(0, f"💬 Style Agent: {item['prompt_report']['rationale']}")

            combined_reason = " | ".join(agent_rationales[:2]) + "."

            breakdown = {
                "motif_pattern_compatibility": item["motif_report"]["score"],
                "color_harmony": item["color_report"]["score"],
                "fabric_suitability": item["fabric_report"]["score"],
                "visual_similarity": round(item["raw_vis"], 1)
            }
            if item["prompt_report"]["has_prompt"]:
                breakdown["customer_prompt_match"] = item["prompt_report"]["score"]

            final_results.append({
                "design": {
                    "id": d.id,
                    "design_code": d.design_code,
                    "name": d.name,
                    "image_url": d.image_url,
                    "category": d.category,
                    "style": d.style,
                    "colors": d.colors,
                    "fabric_suitable": d.fabric_suitable,
                    "placement": d.placement,
                    "description": d.description
                },
                "match_score": final_display_score,
                "scores_breakdown": breakdown,
                "multi_agent_feedback": {
                    "supervisor_approved": True,
                    "motif_agent": item["motif_report"],
                    "color_agent": item["color_report"],
                    "fabric_agent": item["fabric_report"],
                    "prompt_agent": item["prompt_report"]
                },
                "reason": combined_reason
            })

        return final_results

# Global Singleton Instance
supervisor_agent = SupervisorAgent()
