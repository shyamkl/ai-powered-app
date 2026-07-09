import requests

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

HEADERS = {
    "User-Agent": "HappyHourAgent/1.0"
}


def execute_query(query: str):

    response = requests.post(
        OVERPASS_URL,
        data=query,
        headers=HEADERS,
        timeout=15,
    )

    print(response.status_code)
    print(response.text[:300])

    response.raise_for_status()

    return response.json()


def fetch_nearby(lat, lon, radius=5000):

    query = f"""
    [out:json][timeout:60];
    (
      node["amenity"~"restaurant|bar|pub|cafe|nightclub"](around:{radius},{lat},{lon});
      way["amenity"~"restaurant|bar|pub|cafe|nightclub"](around:{radius},{lat},{lon});
      relation["amenity"~"restaurant|bar|pub|cafe|nightclub"](around:{radius},{lat},{lon});
    );
    out center;
    """

    return execute_query(query)