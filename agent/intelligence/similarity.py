from sklearn.metrics.pairwise import cosine_similarity

from agent.intelligence.embedder import embed
from agent.intelligence.category_cache import load_category_embeddings


category_vectors = load_category_embeddings()


def top_categories(text, top_k=5):

    query = embed(text)

    scores = []

    for category, vector in category_vectors.items():

        similarity = cosine_similarity(
            [query],
            [vector]
        )[0][0]

        scores.append(
            (
                category,
                float(similarity)
            )
        )

    scores.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return scores[:top_k]


def best_category(text):

    return top_categories(text, 1)[0]