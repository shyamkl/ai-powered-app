import threading
import time
from datetime import datetime, timedelta
from .city_queue import city_queue


class BackgroundCrawler:

    def __init__(self, provider_manager):

        self.provider_manager = provider_manager
        self.running = False
        self.thread = None

    def crawl(self):

        while self.running:

            city, lat, lon = city_queue.get()

            print("=" * 60)
            print("Refreshing:", city)

            try:

                last_update = self.provider_manager.store.last_update(city)

                if last_update is not None:

                    age = datetime.now() - last_update

                    if age < timedelta(hours=24):

                        print(
                            city,
                            "already fresh (",
                            round(age.total_seconds() / 3600, 1),
                            "hours old)"
                        )

                        city_queue.put(
                            (
                                city,
                                lat,
                                lon
                            )
                        )

                        print("Sleeping 60 seconds...\n")

                        time.sleep(60)

                        continue

                start = time.time()

                venues = self.provider_manager.search(
                    lat,
                    lon
                )

                elapsed = round(
                    time.time() - start,
                    2
                )

                print(
                    city,
                    "->",
                    len(venues),
                    "venues |",
                    elapsed,
                    "seconds"
                )

            except Exception as e:

                print(
                    "Crawler Error:",
                    e
                )

            city_queue.put(
                (
                    city,
                    lat,
                    lon
                )
            )

            print("Sleeping 60 seconds...\n")

            time.sleep(60)

    def start(self):

        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self.crawl,
            daemon=True
        )

        self.thread.start()

        print("Background crawler started.")

    def stop(self):

        self.running = False

        print("Background crawler stopped.")