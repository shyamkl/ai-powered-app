import re


class categoryNormalizer:

    def __init__(self):

        self.category_map = {
            # -------------------------
            # CAFES
            # -------------------------

            "cafe": "Cafe",
            "café": "Cafe",
            "coffee": "Cafe",
            "coffee_shop": "Cafe",
            "coffeehouse": "Cafe",
            "coffee_house": "Cafe",
            "espresso_bar": "Cafe",
            "tea_house": "Cafe",
            "tea_shop": "Cafe",

            # -------------------------
            # RESTAURANTS
            # -------------------------

            "restaurant": "Restaurant",
            "fast_food": "Restaurant",
            "food_court": "Restaurant",
            "eatery": "Restaurant",
            "diner": "Restaurant",
            "bistro": "Restaurant",
            "canteen": "Restaurant",

            # -------------------------
            # BAKERY
            # -------------------------

            "bakery": "Bakery",
            "cake_shop": "Bakery",
            "pastry": "Bakery",
            "dessert": "Bakery",

            # -------------------------
            # BAR
            # -------------------------

            "bar": "Bar",
            "cocktail_bar": "Bar",
            "sports_bar": "Bar",
            "wine_bar": "Bar",

            # -------------------------
            # PUB
            # -------------------------

            "pub": "Pub",
            "irish_pub": "Pub",
            "gastropub": "Pub",

            # -------------------------
            # BREWERY
            # -------------------------

            "brewery": "Brewery",
            "microbrewery": "Brewery",

            # -------------------------
            # LOUNGE
            # -------------------------

            "lounge": "Lounge",
            "hookah": "Lounge",

            # -------------------------
            # SPA
            # -------------------------

            "spa": "Spa",
            "massage": "Spa",
            "wellness": "Spa",

            # -------------------------
            # NIGHT CLUB
            # -------------------------

            "nightclub": "Night Club",
            "club": "Night Club",

            # -------------------------
            # BAD CATEGORIES
            # -------------------------

            "internet_cafe": "Internet Cafe",
            "cyber_cafe": "Internet Cafe",
            "computer_shop": "Computer Shop",
            "computer": "Computer Shop",
            "bank": "Bank",
            "hospital": "Hospital",
            "school": "School",
            "office": "Office"

        }

    def normalize(self, category):

        category = str(category)

        category = category.lower()

        category = category.strip()

        category = category.replace("-","_")

        category = category.replace(" ", "_")

        category = re.sub("_+", "_", category)

        return self.category_map.get(
            category,
            "Unknown"
        )