from concurrent.futures import ThreadPoolExecutor, as_completed
import time

from providers.overpass_provider import OverpassProvider
from providers.geoapify_provider import GeoapifyProvider
from services.deduplicator import deduplicate
from intelligence.ranking import ProviderRanker
from config import MAX_VENUES_PER_SEARCH, MAX_PARALLEL_PROVIDERS
from intelligence.scorer import VenueScorer
from providers.cache.cache_manager import CacheManager
from database.venue_store import VenueStore
from database.search_logger import SearchLogger
from services.venue_filter import is_valid_venue
from intelligence.category_normalizer import categoryNormalizer
from intelligence.venue_validator import is_valid_category

class ProviderManager:

    def __init__(self):

        self.providers = [
            GeoapifyProvider(),
            OverpassProvider(),
        ]
        self.scorer = VenueScorer()
        self.stats = {}
        self.ranker = ProviderRanker()
        self.scorer = VenueScorer()
        self.cache = CacheManager()
        self.store = VenueStore()
        self.normalizer = categoryNormalizer()
        self.logger = SearchLogger()
    def update_stats(self, provider_name, venue_count):

        if provider_name not in self.stats:
            self.stats[provider_name] = {
                "requests": 0,
                "venues": 0
            }

        self.stats[provider_name]["requests"] += 1
        self.stats[provider_name]["venues"] += venue_count

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

            self.ranker.update(
                provider.__class__.__name__,
                0,
                999,
                False
            )

            print(provider.__class__.__name__, e)

            return []

    def get_ranked_providers(self):

        return sorted(
            self.providers,
            key=lambda p: self.ranker.score(
                p.__class__.__name__
            ),
            reverse=True
        )

    def search(self, lat, lon, radius=2000):
        total_start = time.time()

        print("1. search started")
        # ----------------------------
# Try local database first
# ----------------------------

        cached = self.store.nearby(
            lat,
            lon,
            radius
        )

        if len(cached) >= MAX_VENUES_PER_SEARCH:

            print(
                "Database hit:",
                len(cached),
                "venues"
            )

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

            print("Search time:", round(elapsed,3),"seconds")

            return cached[:MAX_VENUES_PER_SEARCH]

        print("Database miss")
        cached = self.cache.get(
            lat,
            lon,
            radius
        )

        if cached is not None:

            print("CACHE HIT")

            elapsed = time.time() - total_start

            self.logger.log(
                latitude=lat,
                longitude=lon,
                radius=radius,
                response_time=elapsed,
                venue_count=len(cached),
                cache_hit=True,
                database_hit=False
            )

            print("Search time:", round(elapsed,3),"seconds")

            return cached

        print("CACHE MISS")
        total_start = time.time()
        all_results = []

        ranked = self.get_ranked_providers()

        print("2. providers:", len(ranked))

        with ThreadPoolExecutor(max_workers=MAX_PARALLEL_PROVIDERS) as executor:

            futures = [

                executor.submit(
                    self.search_provider,
                    provider,
                    lat,
                    lon,
                    radius
                )

                for provider in ranked[:MAX_PARALLEL_PROVIDERS]

            ]

            print("3. futures submitted")

            for future in as_completed(futures):

                print("4. future completed")

                results = future.result()

                print("5. got", len(results), "venues")

                all_results.extend(results)
                print("6. deduplicating")
                if len(all_results) >= MAX_VENUES_PER_SEARCH:
                    break
        print("Deduplicating", len(all_results)) 
        provider_time = time.time()

        print(
            "Provider fetch:",
            round(provider_time - total_start, 2),
            "seconds"
        )         
        filtered = []

        for venue in all_results:

            if is_valid_venue(venue):
                filtered.append(venue)

            print(
                "Filtered:",
                len(filtered),
                "of",
                len(all_results)
            )    

            clean = deduplicate(filtered)
        
        print("Deduplicated:", len(clean))
        print("scoring...")
        dedupe_time = time.time()

        for venue in clean:
            
            venue["name"] = str(
                venue.get("name","")
            )

            venue["category"] = str(
                venue.get("category", "")
            )

            venue["address"] = str(
                venue.get("address", "")
            )

            venue["city"] = str(
                venue.get("city", "")
            )

        print(
            "Deduplicate:",
            round(dedupe_time - provider_time, 2),
            "seconds"
        )
        for venue in clean:
            category = self.normalizer.normalize(
                venue.get("category", "")
            )
            venue["category"] = category

            if not is_valid_category(category):
                continue
            venue["score"] = self.scorer.score(venue)
        print("Scoring complete")
        clean.sort(

            key=lambda v: v["score"],

            reverse=True

        )
        print("Saving to database...")

        self.store.save_many(clean)

        print(
            "Database now contains",
            self.store.count(),
            "venues"
        )
        print("9. returning", len(clean))
        end = time.time()

        elapsed = end - total_start

        print(
            "Total:",
            round(elapsed,2),
            "seconds"
        )

        self.logger.log(
            latitude=lat,
            longitude=lon,
            radius=radius,
            response_time=elapsed,
            venue_count=len(clean),
            cache_hit=False,
            database_hit=False
        )

        return clean[:MAX_VENUES_PER_SEARCH]
                # print("Database miss")

                # all_results = []
    def get_stats(self):
        return self.stats

    def get_best_provider(self):
        return self.ranker.best_provider()

    def get_provider_scores(self):
        return self.ranker.history 