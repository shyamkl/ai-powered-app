from sentence_transformers.util import cos_sim

from agent.intelligence.embedder import embed
from agent.learning.brand_embedding_memory import BrandEmbeddingMemory


memory = BrandEmbeddingMemory()


SIMILARITY_THRESHOLD = 0.90


def resolve_brand(new_brand: str):
    """
    Returns the canonical brand if a similar one already exists.
    Otherwise returns the original brand.
    """

    if not new_brand:
        return None

    vector = embed(new_brand)

    best_name = new_brand
    best_score = 0

    for item in memory.all().values():

        score = float(
            cos_sim(vector, item["embedding"])
        )

        if score > best_score:

            best_score = score
            best_name = item["name"]

    if best_score >= SIMILARITY_THRESHOLD:

        return best_name, best_score

    return new_brand, best_score