from .base_provider import BaseProvider
from ..overpass import fetch_nearby
from ..models.venue import Venue
from ..services.deduplicator import deduplicate
from ..intelligence.hybrid_classifier import classify

print("LOADED OVERPASS PROVIDER V2")
class OverpassProvider(BaseProvider):
    @property
    def provider_name(self):
        return "Overpass"

    def search(self, lat, lon, radius=3000):
 
        data = fetch_nearby(lat, lon, radius)
        print(data)
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
            if tags.get("name") == 2020 or isinstance(tags.get("name"), int):
                print("="*60)
                print("RAW OSM TAGS")
                print(tags)
                print("="*60)
            if len(venues) == 0:
                from pprint import pprint
                pprint(tags)
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