from database import engine
from math import radians, sin, cos, sqrt, atan2


class VenueStore:

    def __init__(self):

        self.conn = sqlite3.connect(
            "venues.db",
            check_same_thread=False
        )

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS venues(

            id TEXT PRIMARY KEY,
            name TEXT,
            lat REAL,
            lon REAL,
            category TEXT,
            address TEXT,
            city TEXT

        )
        """)
        self.conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_lat
        ON venues(lat)
        """)

        self.conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_lon
        ON venues(lon)
        """)

        self.conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_name
        ON venues(name)
        """)
        self.conn.commit()

    def save_many(self, venues):

        cursor = self.conn.cursor()

        for venue in venues:

            venue_id = venue.get("id")

            if venue_id is None:
                continue

            venue_id = str(venue_id)

            cursor.execute("""
                INSERT OR REPLACE INTO venues
                VALUES (?,?,?,?,?,?,?)
            """, (
                venue_id,
                venue.get("name", ""),
                venue.get("lat"),
                venue.get("lon"),
                venue.get("category", ""),
                venue.get("address", ""),
                venue.get("city", "")
            ))

            # except Exception as e:

            print("\nFAILED VENUE")
            print(venue)
            print(e)

            self.conn.commit()

    def count(self):

        cursor = self.conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM venues"
        )

        return cursor.fetchone()[0]

    def distance(self, lat1, lon1, lat2, lon2):

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

    def nearby(self, lat, lon, radius=10000):

        cursor = self.conn.cursor()

       # Approximate conversion:
# 1 degree latitude ≈ 111 km

        lat_delta = radius / 111000

        lon_delta = radius / (
            111000 *
            cos(radians(lat))
        )

        min_lat = lat - lat_delta
        max_lat = lat + lat_delta

        min_lon = lon - lon_delta
        max_lon = lon + lon_delta

        cursor.execute("""

            SELECT
                id,
                name,
                lat,
                lon,
                category,
                address,
                city

            FROM venues

            WHERE

                lat BETWEEN ? AND ?

            AND

                lon BETWEEN ? AND ?

        """, (

            min_lat,
            max_lat,
            min_lon,
            max_lon

        ))

        venues = []

        for row in cursor.fetchall():

            distance = self.distance(
                lat,
                lon,
                row[2],
                row[3]
            )

            if distance <= radius:

                venues.append({

                    "id": row[0],
                    "name": row[1],
                    "lat": row[2],
                    "lon": row[3],
                    "category": row[4],
                    "address": row[5],
                    "city": row[6]

                })

        return venues