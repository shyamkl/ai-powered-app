import requests

from agent.config import OVERPASS_URL

OVERPASS_SERVERS = [
    # This endpoint returned the live result successfully during the browser check.
    "https://overpass.openstreetmap.fr/api/interpreter",
    OVERPASS_URL,
    "https://overpass.kumi.systems/api/interpreter",
    "https://lz4.overpass-api.de/api/interpreter",
]
HEADERS = {"User-Agent": "HappyHourFinder/1.0"}


def execute_query(query: str):
    last_error = None
    for server in dict.fromkeys(OVERPASS_SERVERS):
        try:
            response = requests.post(
                server,
                data={"data": query},
                headers=HEADERS,
                timeout=(5, 25),
            )
            response.raise_for_status()
            return response.json()
        except (requests.RequestException, ValueError) as error:
            last_error = error
            print("Overpass provider failed:", server, error)

    # An unavailable public provider should result in an empty venue list,
    # rather than an unhandled API error in the frontend.
    if last_error:
        print("All Overpass endpoints failed:", last_error)
    return {"elements": []}


def fetch_nearby(lat, lon, radius=5000):

    query = f"""
    [out:json][timeout:20];
    (
      node["amenity"~"restaurant|bar|pub|cafe|nightclub"](around:{radius},{lat},{lon});
      way["amenity"~"restaurant|bar|pub|cafe|nightclub"](around:{radius},{lat},{lon});
      relation["amenity"~"restaurant|bar|pub|cafe|nightclub"](around:{radius},{lat},{lon});
    );
    out center tags;
    """

    return execute_query(query)