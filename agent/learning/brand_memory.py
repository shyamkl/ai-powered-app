import json
from pathlib import Path
from collections import defaultdict


DATA_DIR = Path(__file__).parent.parent / "cache"
DATA_DIR.mkdir(exist_ok=True)

MEMORY_FILE = DATA_DIR / "brand_memory.json"


class BrandMemory:

    def __init__(self):

        self.memory = defaultdict(int)

        self.load()

    def load(self):

        if MEMORY_FILE.exists():

            with open(MEMORY_FILE, "r", encoding="utf-8") as f:

                data = json.load(f)

            self.memory.update(data)

    def save(self):

        with open(MEMORY_FILE, "w", encoding="utf-8") as f:

            json.dump(
                dict(self.memory),
                f,
                indent=4,
                ensure_ascii=False,
            )

    def observe(self, brand):

        if not brand:
            return

        brand = brand.lower().strip()

        self.memory[brand] += 1

        self.save()

    def frequency(self, brand):

        brand = brand.lower().strip()

        return self.memory.get(brand, 0)

    def all_brands(self):

        return dict(self.memory)