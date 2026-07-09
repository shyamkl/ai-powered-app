from providers.base_provider import BaseProvider
from overpass import fetch_nearby


class OverpassProvider(BaseProvider):

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

            venues.append({
                "id": item["id"],
                "name": tags.get("name", "Unknown"),
                "lat": plat,
                "lon": plon,
                "category": tags.get("amenity", ""),
                "address": tags.get("addr:street", ""),
                "city": tags.get("addr:city", "")
            })

        return venues