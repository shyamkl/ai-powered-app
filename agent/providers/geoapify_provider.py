import requests

from providers.base_provider import BaseProvider
from config import GEOAPIFY_API_KEY


class GeoapifyProvider(BaseProvider):

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
                "name": props.get("name", "Unknown"),
                "lat": props.get("lat"),
                "lon": props.get("lon"),
                "category": category,
                "address": props.get("formatted", ""),
                "city": props.get("city", "")
            })

        print("Geoapify returned:", len(venues), "venues")

        return venues