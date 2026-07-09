from math import radians, sin, cos, sqrt, atan2


def distance(lat1, lon1, lat2, lon2):
    R = 6371000

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1))
        * cos(radians(lat2))
        * sin(dlon / 2) ** 2
    )

    return R * 2 * atan2(sqrt(a), sqrt(1 - a))


def deduplicate(venues):

    result = []

    seen_names = {}

    for venue in venues:

        raw_name = venue.get("name", "")

        # Debug invalid names
        if not isinstance(raw_name, str):
            print("=" * 60)
            print("INVALID VENUE")
            print("Name Type :", type(raw_name))
            print("Name Value:", raw_name)
            print("Full Venue:", venue)
            print("=" * 60)

        name = str(raw_name).strip().lower()

        if not name:
            continue

        if name not in seen_names:

            seen_names[name] = venue

            result.append(venue)

            continue

        existing = seen_names[name]

        if distance(
            venue["lat"],
            venue["lon"],
            existing["lat"],
            existing["lon"]
        ) < 30:

            continue

        seen_names[name + "_" + str(venue["id"])] = venue

        result.append(venue)
 
    return result