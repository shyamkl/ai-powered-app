import requests

from .base_provider import BaseProvider
from ..models.venue import Venue
from ..config import GEOAPIFY_API_KEY


class GeoapifyProvider(BaseProvider):
    @property
    def provider_name(self):
        return "Geoapify"

    URL = "https://api.geoapify.com/v2/places"

    def search(self, lat, lon, radius=5000):

        categories = ",".join([
            "catering.restaurant",
            "catering.bar",
            "catering.pub",
            "catering.cafe"
        ])

        params = {
            "categories": categories,
            "filter": f"circle:{lon},{lat},{radius}",
            "limit": 500,
            "apiKey": GEOAPIFY_API_KEY
        }

        response = requests.get(
            self.URL,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        print("Geoapify features:", len(data.get("features", [])))

        venues = []

        for feature in data.get("features", []):
            if len(venues) == 0:
                from pprint import pprint
                pprint(feature["properties"])

            props = feature.get("properties", {})

            category = "unknown"

            for c in props.get("categories", []):

                if "restaurant" in c:
                    category = "restaurant"
                    break

                elif "pub" in c:
                    category = "pub"
                    break

                elif "bar" in c:
                    category = "bar"
                    break

                elif "cafe" in c:
                    category = "cafe"
                    break

            venues.append({
                "id": props.get("place_id"),
                "name": str(props.get("name", "Unknown")).strip(),
                "lat": props.get("lat"),
                "lon": props.get("lon"),
                "category": category,
                "address": props.get("formatted", ""),
                "city": props.get("city", ""),
                "wikidata": props.get("wikidata"),
                "image": props.get("image"),
                "wikimedia_commons":  props.get("wikimedia_commons"),
                "osm_id": props.get("datasource", {})
                    .get("raw", {})
                    .get("osm_id"),

                "osm_type": props.get("datasource", {})
                                .get("raw", {})
                                .get("osm_type"),
            })
            print(
                venues[-1]["name"],
                venues[-1]["image"],
                venues[-1]["wikidata"]
            )
        print("Geoapify returned:", len(venues), "venues")

        return venues