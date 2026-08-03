import pickle
from pathlib import Path

from agent.classifier.category_knowledge import CATEGORY_KNOWLEDGE
from agent.intelligence.embedder import embed

CACHE_DIR = Path(__file__).parent.parent / "cache"
CACHE_FILE = CACHE_DIR / "category_embeddings.pkl"


def load_category_embeddings():
    """
    Loads cached embeddings if available.
    Otherwise builds semantic embeddings from the
    CATEGORY_KNOWLEDGE descriptions.
    """

    CACHE_DIR.mkdir(exist_ok=True)

    # -----------------------------
    # Load cache
    # -----------------------------
    if CACHE_FILE.exists():

        with open(CACHE_FILE, "rb") as f:
            print("✓ Loaded category embedding cache")
            return pickle.load(f)

    # -----------------------------
    # Build new cache
    # -----------------------------
    print("Building embedding cache...")

    embeddings = {}

    for category, description in CATEGORY_KNOWLEDGE.items():

        embeddings[category] = embed(description)

    with open(CACHE_FILE, "wb") as f:
        pickle.dump(embeddings, f)

    print("✓ Embedding cache saved")

    return embeddings