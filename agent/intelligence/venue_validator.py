BAD_CATEGORIES = {
     "Internet Cafe",

    "Computer Shop",

    "Bank",

    "Hospital",

    "School",

    "Office",
}


GOOD_CATEGORIES = {
     "Cafe",

    "Restaurant",

    "Bakery",

    "Bar",

    "Pub",

    "Brewery",

    "Lounge",

    "Spa",

    "Night Club"

}

def is_valid_category(category):

    if category in BAD_CATEGORIES:

        return False
    
    if category in GOOD_CATEGORIES:

        return True
    
    return False