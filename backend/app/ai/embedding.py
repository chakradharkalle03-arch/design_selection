import numpy as np

def cosine_similarity(vec_a: list, vec_b: list) -> float:
    """
    Calculate cosine similarity between two feature vectors.
    Returns float in range [0.0, 1.0].
    """
    if not vec_a or not vec_b:
        return 0.5

    a = np.array(vec_a, dtype=np.float32)
    b = np.array(vec_b, dtype=np.float32)

    # Truncate or pad if dimensions mismatch
    min_dim = min(len(a), len(b))
    a = a[:min_dim]
    b = b[:min_dim]

    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    if norm_a == 0 or norm_b == 0:
        return 0.5

    sim = float(np.dot(a, b) / (norm_a * norm_b))
    # Map [-1.0, 1.0] to [0.0, 1.0] for similarity score percentage
    scaled = (sim + 1.0) / 2.0
    return float(scaled)


def calculate_visual_similarity_score(blouse_embedding: list, design_embedding: list) -> float:
    """Returns visual similarity percentage score (0.0 to 100.0)."""
    sim = cosine_similarity(blouse_embedding, design_embedding)
    return round(sim * 100.0, 1)
