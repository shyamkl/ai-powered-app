import pickle
from pathlib import Path

from agent.intelligence.embedder import embed


CACHE_DIR = Path(__file__).parent.parent / "cache"
CACHE_DIR.mkdir(exist_ok=True)

FILE = CACHE_DIR / "brand_embeddings.pkl"


class BrandEmbeddingMemory:

    def __init__(self):

        self.memory = {}

        self.load()

    # ------------------------

    def load(self):

        if FILE.exists():

            with open(FILE, "rb") as f:

                self.memory = pickle.load(f)

    # ------------------------

    def save(self):

        with open(FILE, "wb") as f:

            pickle.dump(self.memory, f)

    # ------------------------

    def observe(self, brand):

        brand = brand.strip()

        if not brand:

            return

        key = brand.lower()

        if key not in self.memory:

            self.memory[key] = {

                "name": brand,

                "embedding": embed(brand),

                "count": 1,

            }

        else:

            self.memory[key]["count"] += 1

        self.save()

    # ------------------------

    def all(self):

        return self.memory