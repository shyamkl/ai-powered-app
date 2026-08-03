import numpy as np

from agent.learning.memory import load_memory
from agent.intelligence.embedder import embed


def cosine_similarity(a,b):

    a = np.array(a)
    b = np.array(b)

    return np.dot(a,b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )

def retrieve(text):

    memory = load_memory()

    if not memory:
        return None

    query = embed(text)

    best = None
    best_score = -1

    for item in memory:

        score = cosine_similarity(
            query,
            item["embedding"]
        )

        if score > best_score:
            best_score = score
            best = item

    return best, best_score