import requests
from urllib.parse import quote


class PhotoService:

    def get_photo(self, venue: dict) -> str:

        # 1. Direct OSM image tag
        image = venue.get("image")
        if image:
            return image

        # 2. Wikimedia Commons tag
        commons = venue.get("wikimedia_commons")
        if commons:
            commons_name = commons.replace("File:", "")
            return (
                "https://commons.wikimedia.org/wiki/Special:FilePath/"
                + quote(commons_name)
            )

        # 3. Search Wikimedia by venue name
        name = venue.get("name", "").strip()

        if name:
            url = "https://commons.wikimedia.org/w/api.php"

            params = {
                "action": "query",
                "generator": "search",
                "gsrsearch": name,
                "gsrlimit": 1,
                "prop": "imageinfo",
                "iiprop": "url",
                "format": "json",
            }

            try:
                r = requests.get(url, params=params, timeout=5)
                data = r.json()

                pages = data.get("query", {}).get("pages", {})

                for page in pages.values():
                    imageinfo = page.get("imageinfo")
                    if imageinfo:
                        return imageinfo[0].get("url")

            except Exception:
                pass

        # 4. Category fallback
        category = str(venue.get("category", "")).lower()

        if "bar" in category or "pub" in category:
            return "/images/default-bar.jpg"

        if "cafe" in category or "coffee" in category:
            return "/images/default-cafe.jpg"

        return "/images/default-restaurant.jpg"