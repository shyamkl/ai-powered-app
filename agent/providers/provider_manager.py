from concurrent.futures import ThreadPoolExecutor, as_completed
import time

from .geoapify_provider import GeoapifyProvider
from .overpass_provider import OverpassProvider

from ..config import (
    MAX_PARALLEL_PROVIDERS,
    MAX_VENUES_PER_SEARCH,
)

from ..services.deduplicator import deduplicate
from ..services.venue_filter import is_valid_venue

from ..intelligence.scorer import VenueScorer
from ..intelligence.ranking import ProviderRanker
from ..intelligence.category_normalizer import categoryNormalizer
from ..intelligence.venue_validator import is_valid_category

from .cache.cache_manager import CacheManager

from ..database.venue_store import VenueStore
from ..database.search_logger import SearchLogger

from agent.services.image_service import ImageService


class ProviderManager:

    def __init__(self):

        self.providers = [
            GeoapifyProvider(),
            OverpassProvider(),
        ]

        self.cache = CacheManager()

        self.store = VenueStore()

        self.logger = SearchLogger()

        self.scorer = VenueScorer()

        self.normalizer = categoryNormalizer()

        self.image_service = ImageService()

        self.ranker = ProviderRanker()

        self.stats = {}

    # ---------------------------------------------------
    # Provider Statistics
    # ---------------------------------------------------

    def update_stats(self, provider_name, venue_count):

        if provider_name not in self.stats:

            self.stats[provider_name] = {
                "requests": 0,
                "venues": 0
            }

        self.stats[provider_name]["requests"] += 1
        self.stats[provider_name]["venues"] += venue_count

    # ---------------------------------------------------
    # Search One Provider
    # ---------------------------------------------------

    def search_provider(
        self,
        provider,
        lat,
        lon,
        radius
    ):

        start = time.time()

        try:

            results = provider.search(
                lat,
                lon,
                radius
            )

            elapsed = time.time() - start

            self.ranker.update(
                provider.__class__.__name__,
                len(results),
                elapsed,
                True
            )

            self.update_stats(
                provider.__class__.__name__,
                len(results)
            )

            return results

        except Exception as e:

            print(
                provider.__class__.__name__,
                e
            )

            self.ranker.update(
                provider.__class__.__name__,
                0,
                999,
                False
            )

            return []

    # ---------------------------------------------------

    def get_ranked_providers(self):

        return sorted(
            self.providers,
            key=lambda p: self.ranker.score(
                p.__class__.__name__
            ),
            reverse=True
        )

    def search(self, lat, lon, radius=5000):

        total_start = time.time()

        print("1. Search started")

        # --------------------------------------------------
        # DATABASE CACHE
        # --------------------------------------------------

        cached = self.store.nearby(
            lat,
            lon,
            radius = 5000
        )

        if cached:

            print("=" * 60)
            print("DATABASE HIT")
            print(f"Loaded {len(cached)} venues from MySQL")
            for v in cached[:10]:
                print(
                    "DEBUG IMAGE:",
                    v.get("name"),
                    v.get("image_url"),
                    v.get("image_source"),
                    v.get("needs_image_refresh")
                )
                print("=" * 60)
            for venue in cached:

                venue["score"] = self.scorer.score(venue)

            cached.sort(
                key=lambda v: v["score"],
                reverse=True
            )

            elapsed = time.time() - total_start

            self.logger.log(
                latitude=lat,
                longitude=lon,
                radius=radius,
                response_time=elapsed,
                venue_count=len(cached),
                cache_hit=False,
                database_hit=True
            )

            print("Returning database venues only.")

            for venue in cached:

                if venue.get("needs_image_refresh"):

                    image = self.image_service.get_image(venue)

                    venue["image_url"] = image

                    if image:

                        if image.startswith("http"):
                            venue["image_source"] = "pixabay"

                        elif image.startswith("/static"):
                            venue["image_source"] = "local"

                        else:
                            venue["image_source"] = "default"

                    else:
                        venue["image_source"] = "default"

            self.store.save_many(cached)
            print("AFTER SAVE:")
            for v in cached[:5]:
                print(
                v["name"],
                v["image_url"],
                v["image_source"]
                )
            return cached[:MAX_VENUES_PER_SEARCH]
        
            # print("Database miss")

        # --------------------------------------------------
        # MEMORY CACHE
        # --------------------------------------------------

        cached = self.cache.get(
            lat,
            lon,
            radius
        )

        if cached is not None:

            print("Cache hit")

            self.logger.log(
                latitude=lat,
                longitude=lon,
                radius=radius,
                response_time=time.time() - total_start,
                venue_count=len(cached),
                cache_hit=True,
                database_hit=False
            )

            return cached

        print("Cache miss")

        # --------------------------------------------------
        # PROVIDER SEARCH
        # --------------------------------------------------

        providers = self.get_ranked_providers()

        all_results = []

        with ThreadPoolExecutor(
            max_workers=MAX_PARALLEL_PROVIDERS
        ) as executor:

            futures = [

                executor.submit(
                    self.search_provider,
                    provider,
                    lat,
                    lon,
                    radius
                )

                for provider in providers
            ]

            for future in as_completed(futures):

                results = future.result()

                all_results.extend(results)

                if len(all_results) >= MAX_VENUES_PER_SEARCH:
                    break

        print(
            "Fetched",
            len(all_results),
            "venues"
        )

        # --------------------------------------------------
        # FILTER INVALID
        # --------------------------------------------------

        filtered = []

        for venue in all_results:

            venue["name"] = str(
                venue.get("name", "")
            ).strip()

            venue["category"] = str(
                venue.get("category", "")
            ).strip()

            venue["address"] = str(
                venue.get("address", "")
            ).strip()

            venue["city"] = str(
                venue.get("city", "")
            ).strip()

            if is_valid_venue(venue):
                filtered.append(venue)

        print(
            "Filtered:",
            len(filtered)
        )

        # --------------------------------------------------
        # REMOVE DUPLICATES
        # --------------------------------------------------

        clean = deduplicate(filtered)

        print(
            "Deduplicated:",
            len(clean)
        )

        # --------------------------------------------------
        # SCORE + IMAGES
        # --------------------------------------------------

        scored = []

        for venue in clean:

            category = self.normalizer.normalize(
                venue.get("category", "")
            )

            venue["category"] = category

            if not is_valid_category(category):
                continue

            image = None

            if not venue.get("image_url"):
                image = self.image_service.get_image(venue)
                venue["image_url"] = image
            else:
                image = venue["image_url"]


            venue["image_source"] = (
                "pixabay"
                if image and (
                    image.startswith("http")
                    or image.startswith("/static/images")
                )
                else "default"
            )

            venue["score"] = self.scorer.score(venue)

            print(
                venue["name"],
                "->",
                venue["image_url"]
            )

            scored.append(venue)

        scored.sort(
            key=lambda x: x["score"],
            reverse=True
        )
            # --------------------------------------------------
        # SAVE TO DATABASE
        # --------------------------------------------------

        print("Saving", len(scored), "venues to database...")

        needs_save = any(not v.get("id") for v in clean)

        if needs_save:
            self.store.save_many(clean)

        print(
            "Database now contains",
            self.store.count(),
            "venues"
        )

        # --------------------------------------------------
        # SAVE TO CACHE
        # --------------------------------------------------

        self.cache.set(
            lat,
            lon,
            radius,
            scored
        )

        # --------------------------------------------------
        # LOG SEARCH
        # --------------------------------------------------

        elapsed = time.time() - total_start

        self.logger.log(
            latitude=lat,
            longitude=lon,
            radius=radius,
            response_time=elapsed,
            venue_count=len(scored),
            cache_hit=False,
            database_hit=False
        )

        print(
            "Total:",
            round(elapsed, 2),
            "seconds"
        )

        print(
            "Returning",
            len(scored),
            "venues"
        )

        return scored[:MAX_VENUES_PER_SEARCH]

        # --------------------------------------------------

    def get_stats(self):
        return self.stats

    def get_best_provider(self):
        return self.ranker.best_provider()

    def get_provider_scores(self):
        return self.ranker.history    