"""
Knowledge about venue categories.

These are semantic attributes rather than keyword lists.
The classifier will compare extracted venue facts against these profiles.
"""

VENUE_KNOWLEDGE = {

    "Restaurant": {
        "food": True,
        "coffee": False,
        "alcohol": False,
        "beer": False,
        "wine": False,
        "dessert": False,
        "music": False,
        "dance": False,
        "family": True,
    },

    "Cafe": {
        "food": True,
        "coffee": True,
        "alcohol": False,
        "beer": False,
        "wine": False,
        "dessert": True,
        "music": False,
        "dance": False,
        "family": True,
    },

    "Pub": {
        "food": True,
        "coffee": False,
        "alcohol": True,
        "beer": True,
        "wine": False,
        "dessert": False,
        "music": True,
        "dance": False,
        "family": False,
    },

    "Bar": {
        "food": False,
        "coffee": False,
        "alcohol": True,
        "beer": True,
        "wine": True,
        "dessert": False,
        "music": True,
        "dance": False,
        "family": False,
    },

    "Wine Bar": {
        "food": True,
        "coffee": False,
        "alcohol": True,
        "beer": False,
        "wine": True,
        "dessert": False,
        "music": True,
        "dance": False,
        "family": False,
    },

    "Nightclub": {
        "food": False,
        "coffee": False,
        "alcohol": True,
        "beer": True,
        "wine": True,
        "dessert": False,
        "music": True,
        "dance": True,
        "family": False,
    },

    "Fast Food": {
        "food": True,
        "coffee": False,
        "alcohol": False,
        "beer": False,
        "wine": False,
        "dessert": False,
        "music": False,
        "dance": False,
        "family": True,
    },

    "Bakery": {
        "food": True,
        "coffee": False,
        "alcohol": False,
        "beer": False,
        "wine": False,
        "dessert": True,
        "music": False,
        "dance": False,
        "family": True,
    },

    "Tea House": {
        "food": False,
        "coffee": False,
        "alcohol": False,
        "beer": False,
        "wine": False,
        "dessert": True,
        "music": False,
        "dance": False,
        "family": True,
    }

}