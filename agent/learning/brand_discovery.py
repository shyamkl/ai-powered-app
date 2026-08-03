import re


LOCATION_WORDS = {
    "downtown",
    "airport",
    "mall",
    "plaza",
    "center",
    "centre",
    "station",
    "terminal",
    "north",
    "south",
    "east",
    "west",
    "city",
    "express",
    "drive",
    "drive-thru",
}


def discover_brand(name: str):

    """
    Extract the most probable brand from a venue name.
    """

    if not name:
        return ""

    # Remove extra spaces
    name = re.sub(r"\s+", " ", name).strip()

    words = name.split()

    cleaned = []

    for word in words:

        if word.lower() in LOCATION_WORDS:
            break

        cleaned.append(word)

    # Maximum first 3 words
    return " ".join(cleaned[:3])