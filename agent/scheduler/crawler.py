import threading
import time
from datetime import datetime, timedelta

from .city_queue import city_queue
from ..deals.deal_pipeline import DealPipeline
from ..discovery.website_discovery import WebsiteDiscovery


class BackgroundCrawler:

    def __init__(self, provider_manager):

        self.provider_manager = provider_manager
        self.deal_pipeline = DealPipeline()
        self.website_discovery = WebsiteDiscovery()

        self.running = False
        self.thread = None

    def crawl(self):

        while self.running:

            city, lat, lon = city_queue.get()

            print("=" * 60)
            print("Refreshing:", city)

            try:

                last_update = self.provider_manager.store.last_update(
                    city
                )

                if last_update is not None:

                    age = datetime.now() - last_update

                    if age < timedelta(hours=24):

                        print(
                            city,
                            "already fresh (",
                            round(
                                age.total_seconds() / 3600,
                                1
                            ),
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

                # -----------------------------------------
                # VENUE DISCOVERY
                # -----------------------------------------

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

                # -----------------------------------------
                # DEAL EXTRACTION
                # -----------------------------------------

                print()
                print("=" * 60)
                print("DEAL EXTRACTION")
                print("=" * 60)

                deals_found = 0
                websites_processed = 0
                websites_failed = 0

                for venue in venues:

                    # -------------------------------------
                    # Get venue website
                    # -------------------------------------

                    website = (
                        venue.get("website")
                        if isinstance(venue, dict)
                        else None
                    )

                    if website:
                        website = website.strip()

                    else:

                        print(
                            "No website from provider."
                        )

                        print(
                            "Trying OpenStreetMap website discovery..."
                        )

                        website = self.website_discovery.discover(
                            name=venue.get("name"),
                            city=venue.get("city"),
                            lat=venue.get("lat"),
                            lon=venue.get("lon"),
                        )

                        if website:

                            print(
                                "Saving discovered website to database..."
                            )

                            self.provider_manager.store.update_website(
                                venue_id=venue.get("id"),
                                website=website,
                            )
                    # if not website:

                    #     print(
                    #         "Skipping deal extraction:",
                    #         "no website found"
                    #     )

                    #     continue

                    # venue_id = (
                    #     venue.get("id")
                    #     if isinstance(venue, dict)
                    #     else None
                    # )

                    # if venue_id is None:
                    #     print(
                    #         "Skipping deal extraction:",
                    #         "venue has no ID"
                    #     )
                    #     continue

                    # websites_processed += 1

                    # print()
                    # print(
                    #     "Processing deals:",
                    #     venue.get(
                    #         "name",
                    #         "Unknown venue"
                    #     )
                    # )

                    # print(
                    #     "Venue ID:",
                    #     venue_id
                    # )

                    # print(
                    #     "Website:",
                    #     website
                    # )

                    # -------------------------------------
                    # Extract and save deals
                    # -------------------------------------

                    try:

                        extracted_deals = (
                            self.deal_pipeline.process_url(
                                venue_id=venue_id,
                                url=website,
                                country_code=venue.get(
                                    "country"
                                ),
                            )
                        )

                        deals_found += len(
                            extracted_deals
                        )

                        print(
                            "Deals found:",
                            len(extracted_deals)
                        )

                    except Exception as deal_error:

                        websites_failed += 1

                        print(
                            "Deal extraction error:",
                            deal_error
                        )

                        continue
                        # ---------------------------------
                        # IMPORTANT:
                        # One broken website must NOT stop
                        # the entire crawler.
                        # ---------------------------------

                # -----------------------------------------
                # DEAL SUMMARY
                # -----------------------------------------

                print()
                print("=" * 60)
                print("DEAL EXTRACTION SUMMARY")
                print("=" * 60)

                print(
                    "Websites processed:",
                    websites_processed
                )

                print(
                    "Deals found:",
                    deals_found
                )

                print(
                    "Website failures:",
                    websites_failed
                )

            except Exception as e:

                print(
                    "Crawler Error:",
                    e
                )

            # ---------------------------------------------
            # Re-queue city
            # ---------------------------------------------

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