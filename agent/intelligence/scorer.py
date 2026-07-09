import math

class VenueScorer:

    def score(self, venue):

        score = 0

        category = str(venue.get("category", "")).lower()

        name = str(venue.get("name", "")).lower()

         # category weights

        weights = {

            "bar": 100,

            "pub": 95,

            "restaurant": 80,

            "nightclub": 75,

            "cafe": 45,

            "hotel": 35

        }

        score += weights.get(category, 10)

        # bonus keywords

        keywords = {

            "sports": 12,

            "cocktail": 15,

            "beer": 15,

            "tap": 12,

            "grill": 8,

            "lounge": 10,

            "irish": 8,

            "brew": 15

        }

        for word, bonus in keywords.items():

            if word in name:

                score += bonus

        return score