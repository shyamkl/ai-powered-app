import os
import requests
from urllib.parse import quote
from agent.services.category_keywords import CATEGORY_KEYWORDS
import hashlib
from agent.services.pixabay_service import PixabayService

class ImageService:

    def __init__(self):
        self.pixabay = PixabayService()

    def get_image(self, venue):
        print("IMAGE SERVICE CALLED:", venue.get("name"))   
        # Already cached
        if venue.get("image_url"):
            return venue["image_url"]

        print(
            "Searching image for:",
            venue.get("name"),
            venue.get("city")
        )

        image = self.search_wikimedia(venue)

        if image:
            return image

        image = self.category_image(venue)

        if image:
            return image
        print("=" * 60)
        print("Venue:", venue["name"])

        image = self.pixabay.search(venue)

        print("Pixabay returned:", image)
        
        if image:

            local = self.download_pixabay_image(image, venue)

            if local:
                print("Using local image:", local)
                return local

            return image
        
        print("Using Default Image")

        return self.default_image(venue)
        
    # ---------------------------------------------------
    # Wikipedia -> Page Thumbnail
    # ---------------------------------------------------
    
    
    def search_wikimedia(self, venue):
        # print("Searching Commons for:", keyword)

        # data = requests.get(
        #     url,
        #     timeout=10
        # ).json()

        # print(data)

        try:

            search = f'{venue.get("name", "")} {venue.get("city", "")} restaurant'

            url = (
                "https://en.wikipedia.org/w/api.php"
                "?action=query"
                "&list=search"
                "&srsearch=" + quote(search) +
                "&format=json"
            )

            r = requests.get(url, timeout=8).json()

            results = r.get("query", {}).get("search", [])

            if not results:
                return None

            page_title = results[0]["title"]

            print("Wikipedia page:", page_title)

            return self.get_commons_image(page_title)

        except Exception as e:

            print("Wikipedia search failed:", e)

            return None

    # ---------------------------------------------------
    # Get page thumbnail
    # ---------------------------------------------------

    def get_commons_image(self, page_title):

        try:

            url = (
                "https://en.wikipedia.org/w/api.php"
                "?action=query"
                "&titles=" + quote(page_title)
                + "&prop=pageimages"
                "&pithumbsize=800"
                "&format=json"
            )

            data = requests.get(url, timeout=8).json()

            pages = data.get("query", {}).get("pages", {})

            for page in pages.values():

                thumb = page.get("thumbnail")

                if thumb:

                    print("Found image:", thumb["source"])

                    return thumb["source"]

        except Exception as e:

            print("Page image failed:", e)

        return None

    # ---------------------------------------------------
    # Nominatim (placeholder)
    # ---------------------------------------------------

    def search_nominatim(self, venue):

        try:

            query = quote(
                f'{venue.get("name", "")} {venue.get("city", "")}'
            )

            url = (
                "https://nominatim.openstreetmap.org/search"
                f"?q={query}"
                "&format=jsonv2"
                "&limit=1"
            )

            headers = {
                "User-Agent": "HappyHourFinder"
            }

            data = requests.get(
                url,
                headers=headers,
                timeout=8
            ).json()

            if not data:
                return None

            return None

        except Exception as e:

            print("Nominatim failed:", e)

            return None

    # ---------------------------------------------------
    # Default images
    # ---------------------------------------------------

    def default_image(self, venue):

        category = str(
            venue.get("category", "")
        ).lower()

        if "bar" in category:
            return "/images/default-bar.jpg"

        if "cafe" in category:
            return "/images/default-cafe.jpg"

        if "pub" in category:
            return "/images/default-bar.jpg"

        return "/images/default-restaurant.jpg"

    #----------------------------------------------------
    #----------------------------------------------------

    def category_image(self, venue):

        category = str(
            venue.get("category", "")
        ).lower()

        keywords = CATEGORY_KEYWORDS.get(
            category,
            ["restaurant food"]
        )

        search = keywords[
            int(
                hashlib.md5(
                    venue["name"].encode()
                ).hexdigest(),
                16
            ) % len(keywords)
        ]

        return self.search_wikimedia_category(search)

    def search_wikimedia_category(self, keyword):

        try:

            url = (
                "https://commons.wikimedia.org/w/api.php"
                "?action=query"
                "&generator=search"
                "&gsrsearch=" + quote(keyword) +
                "&gsrnamespace=6"
                "&prop=imageinfo"
                "&iiprop=url"
                "&format=json"
            )

            data = requests.get(
                url,
                timeout=10
            ).json()

            pages = list(
                data.get(
                    "query",
                    {}
                ).get(
                    "pages",
                    {}
                ).values()
            )

            if not pages:
                return None

            index = (
                int(
                    hashlib.md5(
                        keyword.encode()
                    ).hexdigest(),
                    16
                )
                %
                len(pages)
            )

            page = pages[index]

            info = page.get("imageinfo")

            if info:

                return info[0]["url"]

        except Exception as e:

            print(e)

        return None

    def download_pixabay_image(self, url, venue):

        try:

            os.makedirs("static/images", exist_ok=True)

            seed = venue.get("name", "") + venue.get("city", "")

            filename = hashlib.md5(seed.encode()).hexdigest() + ".jpg"

            filepath = os.path.join("static", "images", filename)

            if os.path.exists(filepath):
                return f"/static/images/{filename}"
            headers = {
                "User-Agent": "HappyHourFinder/1.0"
            }
            response = requests.get(
                url,
                headers=headers,
                timeout=20,
                stream=True
            )

            if response.status_code != 200:
                print("Download failed:", response.status_code)
                return None

            with open(filepath, "wb") as f:
                for chunk in response.iter_content(8192):
                    if chunk:
                        f.write(chunk)

            print("Saved:", filepath)

            return f"/static/images/{filename}"

        except Exception as e:

            print("Download error:", e)

            return None