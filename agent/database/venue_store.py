from sqlalchemy import create_engine, text
from math import cos


from agent.config import AGENT_DATABASE_URL

DATABASE_URL = AGENT_DATABASE_URL

engine = create_engine(DATABASE_URL, pool_pre_ping=True) if DATABASE_URL else None
class VenueStore:

    def save_many(self, venues):

        if not venues or engine is None:
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
                        country,
                        website,
                        score,
                        provider,
                        image_url,
                        image_source
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
                        :country,
                        :website,
                        :score,
                        :provider,
                        :image_url,
                        :image_source
                    )

                    ON DUPLICATE KEY UPDATE

                        name=VALUES(name),
                        lat=VALUES(lat),
                        lon=VALUES(lon),
                        category=VALUES(category),
                        address=VALUES(address),
                        city=VALUES(city),
                        country=VALUES(country),
                        website=VALUES(website),
                        score=VALUES(score),
                        provider=VALUES(provider),
                        image_url=VALUES(image_url),
                        image_source=VALUES(image_source)

                    """),

                    {

                        "id": str(venue.get("id")),

                        "name": venue.get("name", ""),

                        "lat": venue.get("lat"),

                        "lon": venue.get("lon"),

                        "category": venue.get("category", ""),

                        "address": venue.get("address", ""),

                        "city": venue.get("city", ""),

                        "country": venue.get("country", ""),

                        "website": venue.get("website", ""),

                        "score": venue.get("score", 0),

                        "provider": venue.get("provider", ""),

                        "image_url": venue.get("image_url") or "",

                        "image_source": venue.get("image_source") or ""
                    }

                )
    def count(self):

        if engine is None:
            return 0

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
        radius=2000,
    ):
        if engine is None:
            return []

        print("VENUE STORE RADIUS =", radius)
        print("LAT =", lat)
        print("LON =", lon)
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
                        country,
                        website,
                        score,
                        provider,

                        image_url,
                        image_source

                    FROM ai_venues

                    WHERE

                        lat BETWEEN :min_lat AND :max_lat

                    AND

                        lon BETWEEN :min_lon AND :max_lon

                    LIMIT 5000

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

        venues = [dict(row) for row in rows[:5000]]

        for venue in venues:

            if (
                not venue.get("image_source")
                or
                venue.get("image_source") in ["", "default"]
                or
                "unsplash.com" in str(venue.get("image_url"))
            ):
                venue["needs_image_refresh"] = True
            else:
                venue["needs_image_refresh"] = False

        return venues
    
    def last_update(self, city):

        if engine is None:
            return None

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

    def update_website(self, venue_id, website):

        if engine is None or not venue_id or not website:
            return

        with engine.begin() as conn:

            conn.execute(
                text("""
                    UPDATE ai_venues
                    SET website = :website
                    WHERE id = :venue_id
                """),
                {
                    "venue_id": str(venue_id),
                    "website": website.strip(),
                }
            )