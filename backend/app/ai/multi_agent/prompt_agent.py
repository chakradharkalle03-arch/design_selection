from typing import Dict, Any, Optional
from app.ai.embedding import cosine_similarity
from app.ai.clip_model import clip_engine

class StylePromptAgent:
    """
    SPECIALIZED SUB-AGENT 4: Customer Requirement & Style Prompt Agent
    Evaluates customer prompt instructions against candidate visual embeddings.
    """
    def __init__(self):
        self.name = "Style & Prompt Agent"
        self.code = "PROMPT_AGENT"

    def evaluate(self, customer_requirements: Optional[str], design_embedding: list) -> Dict[str, Any]:
        if not customer_requirements or not customer_requirements.strip() or not design_embedding:
            return {
                "agent": self.name,
                "score": 0.0,
                "has_prompt": False,
                "rationale": "No custom requirements prompt specified"
            }

        text_emb = clip_engine.generate_text_embedding(customer_requirements.strip())
        sim = cosine_similarity(text_emb, design_embedding)
        prompt_score = round(sim * 100.0, 1)

        req_snippet = customer_requirements.strip()[:35]
        rationale = f"Matches customer requirement prompt ('{req_snippet}...')"

        return {
            "agent": self.name,
            "score": prompt_score,
            "has_prompt": True,
            "rationale": rationale
        }
