from sqlalchemy import create_engine, text

DATABASE_URL = "mysql+pymysql://root:463165Shyam@127.0.0.1/restaurant_ai_backup"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)


class SearchLogger:

    def log(
        self,
        latitude,
        longitude,
        radius,
        response_time,
        venue_count,
        cache_hit,
        database_hit
    ):

        with engine.begin() as conn:

            conn.execute(

                text("""

                INSERT INTO search_logs(

                    latitude,

                    longitude,

                    radius,

                    response_time,

                    venue_count,

                    cache_hit,

                    database_hit

                )

                VALUES(

                    :latitude,

                    :longitude,

                    :radius,

                    :response_time,

                    :venue_count,

                    :cache_hit,

                    :database_hit

                )

                """),

                {

                    "latitude": latitude,

                    "longitude": longitude,

                    "radius": radius,

                    "response_time": response_time,

                    "venue_count": venue_count,

                    "cache_hit": cache_hit,

                    "database_hit": database_hit

                }

            )