import hashlib
import requests

from agent.config import PIXABAY_API_KEY


class PixabayService:

    URL = "https://pixabay.com/api/"

    def search(self, venue):
        print("=" * 60)
        print("PIXABAY SEARCH")
        print("API KEY:", PIXABAY_API_KEY)
        print("Venue:", venue.get("name"))
        print("Category:", venue.get("category"))
        keyword = self.build_query(venue)

        params = {
            "key": PIXABAY_API_KEY,
            "q": keyword,
            "image_type": "photo",
            "category": "food",
            "per_page": 50,
            "safesearch": "true"
        }

        try:
            print("Pixabay query:", keyword)
            r = requests.get(
                self.URL,
                params=params,
                timeout=10
            )
            print("Status:", r.status_code)
            print("Response:")
            print(r.text[:500])

            data = r.json()
            print("Total hits:", data.get("total"))
            print("Returned:", len(data.get("hits", [])))
            print("Hits:", len(data.get("hits", [])))

            hits = data.get("hits", [])

            if not hits:
                return None

            seed = (
                venue.get("name", "")
                +
                venue.get("city", "")
            )

            index = (
                int(
                    hashlib.md5(
                        seed.encode()
                    ).hexdigest(),
                    16
                )
                %
                len(hits)
            )
            print(hits[index])
            selected = hits[index]["webformatURL"]
            print(hits[index].keys())
            print("Selected image:", selected)

            return selected

        except Exception as e:

            print("Pixabay:", e)

            return None

    def build_query(self, venue):

        category = str(
            venue.get("category", "")
        ).lower()

        name = str(
            venue.get("name", "")
        ).lower()

        if "pizza" in name:
            return "wood fired pizza"

        if "burger" in name:
            return "gourmet burger"

        if "cafe" in category:
            return "coffee latte"

        if "bar" in category:
            return "craft beer"

        if "pub" in category:
            return "beer mug"

        if "bakery" in category:
            return "fresh bakery"

        if "dessert" in category:
            return "dessert cake"

        if "seafood" in category:
            return "seafood platter"

        if "vegetarian" in category:
            return "vegetarian food"

        if "vegan" in category:
            return "vegan bowl"

        if "arabian" in name:
            return "shawarma"

        if "biryani" in name:
            return "chicken biryani"

        return "restaurant food"

    # print("Selected image:")

    # print(hits[index]["webformatURL"])