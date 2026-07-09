from sqlalchemy import create_engine, text
from math import cos


DATABASE_URL = "mysql+pymysql://root:463165Shyam@127.0.0.1/restaurant_ai_backup"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)


class VenueStore:

    def save_many(self, venues):

        if not venues:
            return

        with engine.begin() as conn:

            for venue in venues:

                conn.execute(

                    text("""

                    INSERT INTO ai_venues
                    (
                        id,
                        name,
                        lat,
                        lon,
                        category,
                        address,
                        city,
                        score,
                        provider
                    )

                    VALUES
                    (
                        :id,
                        :name,
                        :lat,
                        :lon,
                        :category,
                        :address,
                        :city,
                        :score,
                        :provider
                    )

                    ON DUPLICATE KEY UPDATE

                        name=VALUES(name),
                        lat=VALUES(lat),
                        lon=VALUES(lon),
                        category=VALUES(category),
                        address=VALUES(address),
                        city=VALUES(city),
                        score=VALUES(score),
                        provider=VALUES(provider)

                    """),

                    {

                        "id": str(venue.get("id")),

                        "name": venue.get("name", ""),

                        "lat": venue.get("lat"),

                        "lon": venue.get("lon"),

                        "category": venue.get("category", ""),

                        "address": venue.get("address", ""),

                        "city": venue.get("city", ""),

                        "score": venue.get("score", 0),

                        "provider": venue.get("provider", "")

                    }

                )

    def count(self):

        with engine.begin() as conn:

            return conn.execute(

                text(
                    "SELECT COUNT(*) FROM ai_venues"
                )

            ).scalar()

    

    def nearby(
        self,
        lat,
        lon,
        radius=2000
    ):

        # Convert metres to degrees
        lat_delta = radius / 111320

        lon_delta = radius / (
            111320 * max(cos(lat * 3.1415926535 / 180), 0.01)
        )

        with engine.begin() as conn:

            rows = conn.execute(
                

              text("""

                     SELECT

                        id,
                        name,
                        lat,
                        lon,
                        category,
                        address,
                        city,
                        score,
                        provider

                    FROM ai_venues

                    WHERE

                        lat BETWEEN :min_lat AND :max_lat

                    AND

                        lon BETWEEN :min_lon AND :max_lon

                    LIMIT 500

                    """),


                {

                    "min_lat": lat - lat_delta,
                    "max_lat": lat + lat_delta,

                    "min_lon": lon - lon_delta,
                    "max_lon": lon + lon_delta

                }

            ).mappings().all()

            rows = sorted(
                    rows,
                    key=lambda r: r["score"],
                    reverse=True
                )

        return [dict(row) for row in rows[:200]]
    def last_update(self, city):

        with engine.begin() as conn:

            result = conn.execute(

            text("""

            SELECT MAX(updated_at)

            FROM ai_venues

            WHERE city = :city

            """),

            {
                "city": city
            }

        ).scalar()

        return result