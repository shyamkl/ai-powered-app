from sentence_transformers import util

from agent.intelligence.embedder import embed
from agent.intelligence.category_cache import load_category_embeddings


CATEGORY_EMBEDDINGS = load_category_embeddings()


def classify_category(text: str):

    text_embedding = embed(text)

    best_category = None

    best_score = -1

    for category, embedding in CATEGORY_EMBEDDINGS.items():

        score = util.cos_sim(
            text_embedding,
            embedding
        ).item()

        if score > best_score:

            best_score = score

            best_category = category

    return best_category, best_score