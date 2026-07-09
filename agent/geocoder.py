import requests

def reverse_geocode(lat,lon):

    url = (
        f"https://nominatim.openstreetmap.org/reverse"
        f"?lat={lat}&lon={lon}&format=json"
    )

    headers = {
        "User-Agent": "HappyHourAgent"
    }

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        return {}

    return r.json()