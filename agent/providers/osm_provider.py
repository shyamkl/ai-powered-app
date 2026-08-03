import requests

from ..models.venue import Venue
from agent.providers.base_provider import BaseProvider


class OSMProvider(BaseProvider):

    @property
    def provider_name(self):
        return "OpenStreetMap"

    def search(
        self,
        latitude: float,
        longitude: float,
        radius: int = 1000,
    ) -> list[Venue]:

        overpass_url = "https://overpass-api.de/api/interpreter"

        query = f"""
        [out:json];

        (
        node["amenity"~"restaurant|cafe|bar|pub|fast_food|biergarten|food_court|ice_cream|nightclub"]
            (around:{radius},{latitude},{longitude});

        way["amenity"~"restaurant|cafe|bar|pub|fast_food|biergarten|food_court|ice_cream|nightclub"]
            (around:{radius},{latitude},{longitude});
        );

        out center tags;
        """
        print(query)
        response = requests.post(
            overpass_url,
            data={"data": query},
            headers={
                "User-Agent": "HappyHourFinder/1.0"
            },
            timeout=60,
        )

        if response.status_code != 200:
            print("Status:", response.status_code)
            print(response.text)
            return []

        data = response.json()

        data = response.json()

        venues = []

        for element in data["elements"]:

            tags = element.get("tags", {})

            if element["type"] == "node":

                lat = element.get("lat")

                lon = element.get("lon")

            else:

                center = element.get("center", {})

                lat = center.get("lat")

                lon = center.get("lon")

            venue = Venue(

                provider="OSM",

                provider_id=str(element["id"]),

                name=tags.get("name", "Unknown"),

                latitude=lat,

                longitude=lon,

                address=tags.get("addr:full", ""),

                street=tags.get("addr:street", ""),

                city=tags.get("addr:city", ""),

                postcode=tags.get("addr:postcode", ""),

                phone=tags.get("phone", ""),

                website=tags.get("website", ""),

                opening_hours=tags.get("opening_hours", ""),

                raw_categories=[

                    tags.get("amenity", ""),

                    tags.get("shop", ""),

                ],

                source_data=element,

            )

            venues.append(venue)

        return venues