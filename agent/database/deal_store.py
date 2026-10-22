from sqlalchemy import create_engine, text


from agent.config import AGENT_DATABASE_URL

DATABASE_URL = AGENT_DATABASE_URL

engine = create_engine(DATABASE_URL, pool_pre_ping=True) if DATABASE_URL else None


class DealStore:

    # -------------------------------------------------
    # SAVE / UPDATE DEAL
    # -------------------------------------------------

    def save_deal(self, deal):
        if engine is None:
            return None

        """
        Save a normalized deal into ai_deals.

        If the same source_hash already exists,
        update the existing deal instead of creating
        a duplicate.
        """

        if not deal:
            return None

        with engine.begin() as conn:

            existing = conn.execute(
                text("""
                    SELECT id
                    FROM ai_deals
                    WHERE source_hash = :source_hash
                    LIMIT 1
                """),
                {
                    "source_hash": deal["source_hash"]
                }
            ).scalar()

            if existing:

                conn.execute(
                    text("""
                        UPDATE ai_deals

                        SET
                            venue_id = :venue_id,
                            title = :title,
                            description = :description,
                            deal_type = :deal_type,
                            category = :category,
                            discount_value = :discount_value,
                            discount_unit = :discount_unit,
                            items = :items,
                            days = :days,
                            start_time = :start_time,
                            end_time = :end_time,
                            source_url = :source_url,
                            source_type = :source_type,
                            source_text = :source_text,
                            confidence = :confidence,
                            is_active = :is_active,
                            verified_at = :verified_at,
                            last_seen_at = CURRENT_TIMESTAMP,
                            updated_at = CURRENT_TIMESTAMP

                        WHERE id = :id
                    """),
                    {
                        "id": existing,
                        "venue_id": deal["venue_id"],
                        "title": deal["title"],
                        "description": deal.get("description"),
                        "deal_type": deal.get(
                            "deal_type",
                            "unknown"
                        ),
                        "category": deal.get("category"),
                        "discount_value": self._decimal_to_string(
                            deal.get("discount_value")
                        ),
                        "discount_unit": deal.get(
                            "discount_unit"
                        ),
                        "items": self._json_value(
                            deal.get("items", [])
                        ),
                        "days": self._json_value(
                            deal.get("days", [])
                        ),
                        "start_time": deal.get("start_time"),
                        "end_time": deal.get("end_time"),
                        "source_url": deal["source_url"],
                        "source_type": deal.get(
                            "source_type",
                            "website"
                        ),
                        "source_text": deal.get(
                            "source_text"
                        ),
                        "confidence": deal.get(
                            "confidence",
                            0.0
                        ),
                        "is_active": deal.get(
                            "is_active",
                            True
                        ),
                        "verified_at": deal.get(
                            "verified_at"
                        )
                    }
                )

                return existing

            result = conn.execute(
                text("""
                    INSERT INTO ai_deals
                    (
                        venue_id,
                        title,
                        description,
                        deal_type,
                        category,
                        discount_value,
                        discount_unit,
                        items,
                        days,
                        start_time,
                        end_time,
                        source_url,
                        source_type,
                        source_text,
                        source_hash,
                        confidence,
                        is_active,
                        verified_at
                    )

                    VALUES
                    (
                        :venue_id,
                        :title,
                        :description,
                        :deal_type,
                        :category,
                        :discount_value,
                        :discount_unit,
                        :items,
                        :days,
                        :start_time,
                        :end_time,
                        :source_url,
                        :source_type,
                        :source_text,
                        :source_hash,
                        :confidence,
                        :is_active,
                        :verified_at
                    )
                """),
                {
                    "venue_id": deal["venue_id"],
                    "title": deal["title"],
                    "description": deal.get("description"),
                    "deal_type": deal.get(
                        "deal_type",
                        "unknown"
                    ),
                    "category": deal.get("category"),
                    "discount_value": self._decimal_to_string(
                        deal.get("discount_value")
                    ),
                    "discount_unit": deal.get(
                        "discount_unit"
                    ),
                    "items": self._json_value(
                        deal.get("items", [])
                    ),
                    "days": self._json_value(
                        deal.get("days", [])
                    ),
                    "start_time": deal.get("start_time"),
                    "end_time": deal.get("end_time"),
                    "source_url": deal["source_url"],
                    "source_type": deal.get(
                        "source_type",
                        "website"
                    ),
                    "source_text": deal.get(
                        "source_text"
                    ),
                    "source_hash": deal["source_hash"],
                    "confidence": deal.get(
                        "confidence",
                        0.0
                    ),
                    "is_active": deal.get(
                        "is_active",
                        True
                    ),
                    "verified_at": deal.get(
                        "verified_at"
                    )
                }
            )

            return result.lastrowid

    # -------------------------------------------------
    # SAVE SOURCE EVENT
    # -------------------------------------------------

    def save_source_event(
        self,
        deal_id,
        source_url,
        source_type,
        source_text,
        source_hash,
        confidence,
        status="success",
        verified_at=None
    ):
        if engine is None:
            return None

        """
        Save a crawl/verification event into
        ai_deal_source_events.
        """

        with engine.begin() as conn:

            result = conn.execute(
                text("""
                    INSERT INTO ai_deal_source_events
                    (
                        deal_id,
                        source_url,
                        source_type,
                        source_text,
                        source_hash,
                        confidence,
                        status,
                        verified_at
                    )

                    VALUES
                    (
                        :deal_id,
                        :source_url,
                        :source_type,
                        :source_text,
                        :source_hash,
                        :confidence,
                        :status,
                        :verified_at
                    )
                """),
                {
                    "deal_id": deal_id,
                    "source_url": source_url,
                    "source_type": source_type,
                    "source_text": source_text,
                    "source_hash": source_hash,
                    "confidence": confidence,
                    "status": status,
                    "verified_at": verified_at
                }
            )

            return result.lastrowid

    # -------------------------------------------------
    # GET DEALS FOR VENUE
    # -------------------------------------------------

    def get_venue_deals(
        self,
        venue_id,
        active_only=True
    ):
        if engine is None:
            return []

        """
        Return deals belonging to a venue.
        """

        with engine.begin() as conn:

            query = """
                SELECT
                    id,
                    venue_id,
                    title,
                    description,
                    deal_type,
                    category,
                    discount_value,
                    discount_unit,
                    items,
                    days,
                    start_time,
                    end_time,
                    source_url,
                    source_type,
                    source_text,
                    source_hash,
                    confidence,
                    is_active,
                    verified_at,
                    first_seen_at,
                    last_seen_at,
                    created_at,
                    updated_at

                FROM ai_deals

                WHERE venue_id = :venue_id
            """

            if active_only:
                query += """
                    AND is_active = 1
                """

            query += """
                ORDER BY updated_at DESC
            """

            rows = conn.execute(
                text(query),
                {
                    "venue_id": venue_id
                }
            ).mappings().all()

            return [
                dict(row)
                for row in rows
            ]

    # -------------------------------------------------
    # GET DEAL BY ID
    # -------------------------------------------------

    def get_deal(self, deal_id):
        if engine is None:
            return None


        with engine.begin() as conn:

            row = conn.execute(
                text("""
                    SELECT *
                    FROM ai_deals
                    WHERE id = :deal_id
                    LIMIT 1
                """),
                {
                    "deal_id": deal_id
                }
            ).mappings().first()

            if not row:
                return None

            return dict(row)

    # -------------------------------------------------
    # DEACTIVATE DEAL
    # -------------------------------------------------

    def deactivate_deal(self, deal_id):
        if engine is None:
            return None


        with engine.begin() as conn:

            conn.execute(
                text("""
                    UPDATE ai_deals

                    SET
                        is_active = 0,
                        updated_at = CURRENT_TIMESTAMP

                    WHERE id = :deal_id
                """),
                {
                    "deal_id": deal_id
                }
            )

    # -------------------------------------------------
    # DEACTIVATE OLD DEALS
    # -------------------------------------------------

    def deactivate_old_deals(
        self,
        venue_id,
        source_url,
        current_hashes
    ):
        if engine is None:
            return None

        """
        Deactivate deals from a source that were not
        found during the latest extraction.

        This lets the crawler remove deals that have
        disappeared from a website.
        """

        if not current_hashes:
            return

        with engine.begin() as conn:

            placeholders = ", ".join(
                f":hash_{i}"
                for i in range(len(current_hashes))
            )

            params = {
                "venue_id": venue_id,
                "source_url": source_url
            }

            for i, source_hash in enumerate(current_hashes):
                params[f"hash_{i}"] = source_hash

            conn.execute(
                text(f"""
                    UPDATE ai_deals

                    SET
                        is_active = 0,
                        updated_at = CURRENT_TIMESTAMP

                    WHERE venue_id = :venue_id

                    AND source_url = :source_url

                    AND source_hash NOT IN (
                        {placeholders}
                    )

                    AND is_active = 1
                """),
                params
            )

    # -------------------------------------------------
    # COUNT DEALS
    # -------------------------------------------------

    def count(self):
        if engine is None:
            return 0


        with engine.begin() as conn:

            return conn.execute(
                text("""
                    SELECT COUNT(*)
                    FROM ai_deals
                """)
            ).scalar()

    # -------------------------------------------------
    # HELPERS
    # -------------------------------------------------

    @staticmethod
    def _decimal_to_string(value):

        if value is None:
            return None

        return str(value)

    @staticmethod
    def _json_value(value):

        import json

        if value is None:
            return json.dumps([])

        return json.dumps(value)
