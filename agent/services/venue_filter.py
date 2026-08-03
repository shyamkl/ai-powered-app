# categories we actually want

ALLOWED_CATEGORIES = {
     "restaurant",
    "cafe",
    "coffee",
    "coffee_shop",
    "bar",
    "pub",
    "brewery",
    "wine_bar",
    "cocktail_bar",
    "food_court",
    "fast_food",
    "pizza",
    "bakery",
    "ice_cream",
    "dessert",
    "juice_bar",
    "tea_house",
    "bistro",
    "steakhouse",
    "seafood",
    "vegetarian",
    "vegan",
}

# Things we never want

BLOCKED_WORDS = {
    "internet cafe",
    "internet_cafe",
    "cyber cafe",
    "cyber_cafe",
    "cybercafe",
    "internet center",
    "internet centre",
    "gaming cafe",
    "gaming_cafe",
    "gaming center",
    "gaming centre",
    "computer centre", 
    "computer center",
    "browsing centre",
    "browsing center",
    "photocopy",
    "xerox",
    "printer",
    "typing centre",
    "typing center"

}

def is_valid_venue(venue):

    name = str(
        venue.get("name", "")
    ).lower()

    category = str(
        venue.get("category", "")
    ).lower()

    address = str(
        venue.get("address", "")
    ).lower()

    text = f"{name} {category} {address}"

    for word in BLOCKED_WORDS:

        if word in text:
            return False
        

    return True     