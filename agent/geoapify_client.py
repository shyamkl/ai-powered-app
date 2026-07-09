import requests

from config import GEOAPIFY_API_KEY

BASE_URL = "https://api.geoapify.com/v2/places"


def search_places(lat, lon, radius):

    categories = ",".join([
        "catering.restaurant",
        "catering.bar",
        "catering.pub",
        "catering.cafe"
    ])

    params = {
        "categories": categories,
        "filter": f"circle:{lon},{lat},{radius}",
        "limit": 500,
        "apiKey": GEOAPIFY_API_KEY
    }

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    return response.json()