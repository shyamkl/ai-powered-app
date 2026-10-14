import hashlib
import json

from .extractor import DealExtractor
from .fetcher import fetch_page
from ..database.deal_store import DealStore


class DealPipeline:

    def __init__(self):
        self.extractor = DealExtractor()
        self.store = DealStore()

    def process_url(
        self,
        venue_id: int,
        url: str,
        country_code: str | None = None,
        locale: str | None = None,
    ):
        """
        Fetch a venue source, extract deals,
        create stable deal hashes, and persist
        the normalized deals.
        """

        print()
        print("===================================")
        print("DEAL PIPELINE")
        print("===================================")

        print("VENUE ID:", venue_id)
        print("URL:", url)

        # -----------------------------------------
        # Fetch source page
        # -----------------------------------------

        html = fetch_page(url)

        print(
            "HTML LENGTH:",
            len(html)
        )

        # -----------------------------------------
        # Create page/source hash
        # -----------------------------------------

        page_hash = hashlib.sha256(
            html.encode("utf-8")
        ).hexdigest()

        print(
            "PAGE HASH:",
            page_hash
        )

        # -----------------------------------------
        # Extract deals
        #
        # We already fetched the HTML above,
        # so call extract_deals() directly instead
        # of fetching the URL a second time.
        # -----------------------------------------

        deals = self.extractor.extract_deals(
            html=html,
            venue_id=venue_id,
            source_url=url,
            source_hash=page_hash,
            country_code=country_code,
            locale=locale,
        )

        print(
            "EXTRACTED DEALS:",
            len(deals)
        )

        saved_deals = []
        current_hashes = []

        # -----------------------------------------
        # Save extracted deals
        # -----------------------------------------

        for deal in deals:

            deal_data = self._prepare_deal(
                deal,
                venue_id=venue_id,
                url=url,
                page_hash=page_hash,
            )

            current_hashes.append(
                deal_data["source_hash"]
            )

            deal_id = self.store.save_deal(
                deal_data
            )

            # -------------------------------------
            # Source event uses PAGE HASH
            #
            # This records which webpage version
            # produced the deal.
            # -------------------------------------

            self.store.save_source_event(
                deal_id=deal_id,
                source_url=deal_data["source_url"],
                source_type=deal_data["source_type"],
                source_text=deal_data["source_text"],
                source_hash=page_hash,
                confidence=deal_data["confidence"],
                status="success",
            )

            saved_deals.append(
                {
                    "id": deal_id,
                    **deal_data,
                }
            )

        # -----------------------------------------
        # Deactivate deals no longer found
        # -----------------------------------------

        self.store.deactivate_old_deals(
            venue_id=venue_id,
            source_url=url,
            current_hashes=current_hashes,
        )

        print(
            "SAVED DEALS:",
            len(saved_deals)
        )

        print("===================================")

        return saved_deals

    # -------------------------------------------------
    # PREPARE DEAL
    # -------------------------------------------------

    @staticmethod
    def _prepare_deal(
        deal,
        venue_id: int,
        url: str,
        page_hash: str,
    ):
        """
        Convert DealBase into a database dictionary
        and create a unique stable hash for this
        individual deal.

        page_hash identifies the source webpage.
        source_hash identifies the individual deal.
        """

        data = deal.model_dump()

        data["venue_id"] = venue_id

        data["source_url"] = (
            data.get("source_url")
            or url
        )

        data["source_type"] = (
            data.get("source_type")
            or "website"
        )

        # -----------------------------------------
        # Build stable deal identity
        # -----------------------------------------

        identity = {
            "venue_id": venue_id,
            "source_url": data["source_url"],
            "title": data.get("title"),
            "description": data.get("description"),
            "deal_type": data.get("deal_type"),
            "category": data.get("category"),
            "discount_value": (
                str(data.get("discount_value"))
                if data.get("discount_value") is not None
                else None
            ),
            "discount_unit": data.get(
                "discount_unit"
            ),
            "items": data.get("items", []),
            "days": data.get("days", []),
            "start_time": data.get("start_time"),
            "end_time": data.get("end_time"),
        }

        identity_json = json.dumps(
            identity,
            sort_keys=True,
            default=str,
            ensure_ascii=False,
        )

        deal_hash = hashlib.sha256(
            (
                page_hash + "|" + identity_json
            ).encode("utf-8")
        ).hexdigest()

        data["source_hash"] = deal_hash

        return data