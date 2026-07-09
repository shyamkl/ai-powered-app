import time


class CacheManager:

    def __init__(self):

        self.cache = {}

        self.ttl = 300      # 5 minutes

    def make_key(
        self,
        lat,
        lon,
        radius
    ):

        return (
            round(lat, 3),
            round(lon, 3),
            radius
        )

    def get(
        self,
        lat,
        lon,
        radius
    ):

        key = self.make_key(
            lat,
            lon,
            radius
        )

        if key not in self.cache:
            return None

        timestamp, value = self.cache[key]

        if time.time() - timestamp > self.ttl:

            del self.cache[key]

            return None

        return value

    def set(
        self,
        lat,
        lon,
        radius,
        value
    ):

        key = self.make_key(
            lat,
            lon,
            radius
        )

        self.cache[key] = (
            time.time(),
            value
        )