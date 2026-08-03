import json
from pathlib import Path
from collections import defaultdict


DATA_DIR = Path(__file__).parent.parent / "cache"
DATA_DIR.mkdir(exist_ok=True)

BRAND_FILE = DATA_DIR / "brand_statistics.json"


class BrandStatistics:

    def __init__(self):

        self.statistics = defaultdict(lambda: defaultdict(int))

        self.load()

    # ---------------------------------------
    # Load previous learning
    # ---------------------------------------

    def load(self):

        if BRAND_FILE.exists():

            with open(BRAND_FILE, "r", encoding="utf-8") as f:

                data = json.load(f)

            for brand, categories in data.items():

                self.statistics[brand] = defaultdict(
                    int,
                    categories,
                )

    # ---------------------------------------
    # Save learning
    # ---------------------------------------

    def save(self):

        data = {
            brand: dict(categories)
            for brand, categories in self.statistics.items()
        }

        with open(BRAND_FILE, "w", encoding="utf-8") as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False,
            )

    # ---------------------------------------
    # Observe a venue
    # ---------------------------------------

    def observe(
        self,
        brand: str,
        category: str,
    ):

        if not brand or not category:
            return

        brand = brand.lower().strip()

        self.statistics[brand][category] += 1

        self.save()

    # ---------------------------------------
    # Get statistics
    # ---------------------------------------

    def get_counts(
        self,
        brand: str,
    ):

        brand = brand.lower().strip()

        return dict(
            self.statistics.get(
                brand,
                {},
            )
        )