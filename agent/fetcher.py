import requests
from config import OVERPASS_URL
from math import radians,sin,cos,sqrt,atan2


def fetch_nearby(lat: float, lon: float, radius: int = 2000):

    query = f"""
    [out:json];

    (
     node["amenity"="restaurant"](around:{radius},{lat},{lon});
     node["amenity"="bar"](around:{radius},{lat},{lon});
     node["amenity"="pub"](around:{radius},{lat},{lon});
     node["amenity"="cafe"](around:{radius},{lat},{lon});
    );

    out body;

    """

    response = requests.post(
        OVERPASS_URL,
        data=query,
        headers={
            "User-Agent":"HappyHourFinder-Agent"
        },
        timeout=60,
    )

    response.raise_for_status()
    
    data = response.json()

    venues = []

    for item in data.get("elements", []):
        tags = item.get("tags", {})

        dist = distance_km(
            lat,
            lon,
            item["lat"],
            item["lon"]
        )
        venues.append({
            "id": item["id"],

            "name": tags.get("name", "Unknown Venue"),

            "lat": item["lat"],

            "lon": item["lon"],

            "category": tags.get("amenity", "venue"),

            "address": tags.get("addr:street", ""),

            "city": tags.get("addr:city", ""),
            "distance": round(dist,2)
        })

        venues.sort(
        key=lambda x: x["distance"]
    )
    return venues[:100]
        
def distance_km(
    lat1,
    lon1,
    lat2,
    lon2
): 
   
    R = 6371

    dlat = radians(lat2-lat1)
    dlon = radians(lon2-lon1)

    a= (
        sin(dlat/2)**2
        +
        cos(radians(lat1))
        *
        cos(radians(lat2))
        *
        sin(dlon/2)**2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1-a)
    )

    return R*c