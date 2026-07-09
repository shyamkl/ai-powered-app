import random
import requests

OVERPASS_SERVERS = [
    "https://overpass.kumi.systems/api/interpreter",
    "https://lz4.overpass-api.de/api/interpreter",
    "https://overpass-api.de/api/interpreter",
    "https://overpass.openstreetmap.fr/api/interpreter",
]

HEADERS = {
    "User-Agent": "HappyHourAgent/1.0"
}


def execute_query(query: str):

    servers = OVERPASS_SERVERS.copy()
    random.shuffle(servers)

    last_error = None

    for server in servers:

        try:

            print(f"Trying {server}")

            response = requests.post(
                server,
                data={"data": query},
                headers=HEADERS,
                timeout=90
            )

            response.raise_for_status()

            print(f"SUCCESS -> {server}")

            return response.json()

        except Exception as e:

            print(f"FAILED -> {server}")
            print(e)

            last_error = e

    raise Exception(last_error)