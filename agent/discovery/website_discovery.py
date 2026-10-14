import time
import requests
from difflib import SequenceMatcher


class WebsiteDiscovery:

    NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

    def __init__(
        self,
        timeout: int = 10,
        min_request_interval: float = 1.1,
    ):
        self.timeout = timeout
        self.min_request_interval = min_request_interval

        self.headers = {
            "User-Agent": (
                "HappyHourFinder/1.0 "
                "(website discovery for venue deal extraction)"
            )
        }

        # In-memory cache.
        #
        # key:
        #   normalized venue name + city
        #
        # value:
        #   discovered website
        #   OR None when no website was found
        self.cache = {}

        # Time of the last request sent to Nominatim.
        self.last_request_time = 0.0

    def discover(
        self,
        name: str,
        city: str | None = None,
        lat: float | None = None,
        lon: float | None = None,
    ) -> str | None:

        if not name:
            return None

        # --------------------------------------------------
        # CACHE CHECK
        # --------------------------------------------------

        cache_key = self._cache_key(
            name,
            city,
        )

        if cache_key in self.cache:

            cached_website = self.cache[
                cache_key
            ]

            print(
                "WEBSITE CACHE HIT:",
                name,
                "->",
                cached_website,
            )

            return cached_website

        # --------------------------------------------------
        # BUILD SEARCH QUERY
        # --------------------------------------------------

        query = name

        if city:
            query += f", {city}"

        query += ", India"

        params = {
            "q": query,
            "format": "jsonv2",
            "addressdetails": 1,
            "extratags": 1,
            "namedetails": 1,
            "limit": 5,
        }

        # --------------------------------------------------
        # RATE LIMIT
        # --------------------------------------------------

        self._wait_for_rate_limit()

        # --------------------------------------------------
        # NOMINATIM REQUEST
        # --------------------------------------------------

        try:

            response = requests.get(
                self.NOMINATIM_URL,
                params=params,
                headers=self.headers,
                timeout=self.timeout,
            )

            self.last_request_time = (
                time.monotonic()
            )

            response.raise_for_status()

            results = response.json()

        except Exception as e:

            # Cache failures as None so that the same
            # venue is not repeatedly requested during
            # the current crawler run.
            self.cache[cache_key] = None

            print(
                "Website discovery failed:",
                name,
                "|",
                e,
            )

            return None

        # --------------------------------------------------
        # FIND BEST WEBSITE
        # --------------------------------------------------

        best_url = None
        best_score = 0.0

        for result in results:

            result_name = (
                result.get("name")
                or result.get(
                    "namedetails",
                    {},
                ).get("name")
                or ""
            )

            extratags = (
                result.get(
                    "extratags",
                    {},
                )
                or {}
            )

            website = (
                extratags.get("website")
                or extratags.get(
                    "contact:website"
                )
                or extratags.get(
                    "brand:website"
                )
                or extratags.get(
                    "operator:website"
                )
            )

            if not website:
                continue

            score = self._score_match(
                name,
                result_name,
                result,
                lat,
                lon,
            )

            print(
                "OSM website candidate:",
                result_name,
                "->",
                website,
                "| score:",
                round(score, 3),
            )

            if score > best_score:

                best_score = score
                best_url = website

        # --------------------------------------------------
        # SAVE RESULT TO CACHE
        # --------------------------------------------------

        self.cache[cache_key] = best_url

        if best_url:

            print(
                "DISCOVERED WEBSITE:",
                name,
                "->",
                best_url,
            )

        else:

            print(
                "NO WEBSITE FOUND:",
                name,
            )

        return best_url

    def _wait_for_rate_limit(self):

        elapsed = (
            time.monotonic()
            - self.last_request_time
        )

        remaining = (
            self.min_request_interval
            - elapsed
        )

        if remaining > 0:

            time.sleep(
                remaining
            )

    @staticmethod
    def _cache_key(
        name: str,
        city: str | None = None,
    ) -> str:

        normalized_name = (
            WebsiteDiscovery._normalize(name)
        )

        normalized_city = (
            WebsiteDiscovery._normalize(city)
            if city
            else ""
        )

        return (
            f"{normalized_name}|"
            f"{normalized_city}"
        )

    def _score_match(
        self,
        venue_name: str,
        result_name: str,
        result: dict,
        lat: float | None,
        lon: float | None,
    ) -> float:

        name_score = SequenceMatcher(
            None,
            self._normalize(venue_name),
            self._normalize(result_name),
        ).ratio()

        location_score = 0.0

        if lat is not None and lon is not None:

            try:

                result_lat = float(
                    result.get("lat")
                )

                result_lon = float(
                    result.get("lon")
                )

                distance = (
                    (result_lat - lat) ** 2
                    +
                    (result_lon - lon) ** 2
                ) ** 0.5

                if distance < 0.002:

                    location_score = 1.0

                elif distance < 0.01:

                    location_score = 0.5

            except (
                TypeError,
                ValueError,
            ):

                pass

        return (
            name_score * 0.7
            +
            location_score * 0.3
        )

    @staticmethod
    def _normalize(
        value: str,
    ) -> str:

        return (
            value
            .lower()
            .strip()
            .replace("&", "and")
        )