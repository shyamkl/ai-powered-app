import requests
from urllib.parse import quote


class ImageProvider:

    def get_image(self, venue):

        # Already cached?
        if venue.get("image_url"):
            return venue["image_url"]

        # OSM image tag
        image = self.osm_image(venue)
        if image:
            return image

        # Wikimedia using Wikidata
        image = self.wikimedia_image(venue)
        if image:
            return image

        # Fallback by category
        return self.default_image(venue)

    # ----------------------------------------------------
    # OSM image tag
    # ----------------------------------------------------

    def osm_image(self, venue):

        image = venue.get("image")

        if image:
            return image

        return None

    # ----------------------------------------------------
    # Wikimedia Commons
    # ----------------------------------------------------

    def wikimedia_image(self, venue):

        wikidata = venue.get("wikidata")

        if not wikidata:
            return None

        try:

            url = (
                "https://www.wikidata.org/wiki/Special:EntityData/"
                f"{wikidata}.json"
            )

            data = requests.get(url, timeout=10).json()

            entity = data["entities"][wikidata]

            claims = entity.get("claims", {})

            if "P18" not in claims:
                return None

            filename = claims["P18"][0]["mainsnak"]["datavalue"]["value"]

            filename = filename.replace(" ", "_")

            return (
                "https://commons.wikimedia.org/wiki/Special:FilePath/"
                + quote(filename)
            )

        except Exception:

            return None

    # ----------------------------------------------------
    # Default category image
    # ----------------------------------------------------

    def default_image(self, venue):

        category = str(
            venue.get("category", "")
        ).lower()

        if "bar" in category:
            return "/images/default-bar.jpg"

        if "pub" in category:
            return "/images/default-bar.jpg"

        if "cafe" in category:
            return "/images/default-cafe.jpg"

        return "/images/default-restaurant.jpg"