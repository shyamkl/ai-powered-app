from .base_provider import BaseProvider
from ..overpass import fetch_nearby
class OverpassProvider(BaseProvider):
    @property
    def provider_name(self):
        return "Overpass"

    def search(self, lat, lon, radius=3000):
 
        data = fetch_nearby(lat, lon, radius)
        venues = []

        for item in data.get("elements", []):

            if "lat" in item:
                plat = item["lat"]
                plon = item["lon"]

            elif "center" in item:
                plat = item["center"]["lat"]
                plon = item["center"]["lon"]

            else:
                continue

            tags = item.get("tags", {})
            venues.append({
                "id": item["id"],
                "name": str(tags.get("name", "")).strip(),
                "lat": plat,
                "lon": plon,
                "category": tags.get("amenity", ""),
                "address": tags.get("addr:street", ""),
                "city": tags.get("addr:city", ""),
                "image": tags.get("image"),
                "wikidata": tags.get("wikidata"),
                "wikimedia_commons": tags.get("wikimedia_commons")
            })

        return venues