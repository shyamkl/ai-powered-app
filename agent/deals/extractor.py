import re

from bs4 import BeautifulSoup
from decimal import Decimal

from agent.deals.fetcher import fetch_page
from agent.deals.normalizer import DealNormalizer
from agent.deals.schema import DealBase


class DealExtractor:
    """
    Extracts possible deal- realted text from HTML

    """
    def __init__(self):
        self.normalizer = DealNormalizer()

    DEAL_KEYWORDS = [
         "happy hour",
        "happy-hour",
        "special",
        "promotion",
        "promo",
        "discount",
        "deal",
        "offer",
        "buy one get one",
        "bogo",
        "50% off",
        "30% off",
        "20% off",
        "free",
        "cocktail",
        "beer",
        "drinks",
    ]
    MONEY_PATTERN = re.compile(
        r"(?:₹|€|£|¥|₩|฿|\$)\s*\d+(?:[.,]\d+)*"
        r"|\d+(?:[.,]\d+)*\s*(?:₹|€|£|¥|₩|฿|\$)"
        r"|\b(?:USD|INR|EUR|GBP|JPY|CNY|THB|CAD|AUD)\s*\d+(?:[.,]\d+)*"
        r"|\d+(?:[.,]\d+)*\s*\b(?:USD|INR|EUR|GBP|JPY|CNY|THB|CAD|AUD)\b",
        re.IGNORECASE,
    )

    def extract_text(self, html:str)->str:
        """
        Convert HTML into clean readable text.

        """
        soup = BeautifulSoup(html, "html.parser")

        # Remove things that are normally not useful
        # for deal extraction.
        for elements in soup(
            ["script", "style", "noscript"]
        ):
            elements.decompose()

        text = soup.get_text(
            separator = " ",
            strip=True,
        )

        return text

    def find_candidates(self, text:str) ->list[str]:
        """
        Find sentence section that may contain deal

        """

        candidates = []

        parts = text.split(".")

        for part in parts:

            cleaned = part.strip()

            if not cleaned: 
                continue

            lower = cleaned.lower()
            has_deal_keyword = False

            for keyword in self.DEAL_KEYWORDS:

                pattern = rf"\b{keyword}\b"

                if re.search(pattern, lower):
                    has_deal_keyword = True
                    break
            has_money_expression = bool(
                self.MONEY_PATTERN.search(cleaned)
            )
            if has_deal_keyword or has_money_expression:
                candidates.append(cleaned)
        return candidates
    
    def normalize_candidates(
        self,
        candidates: list[str],
        country_code: str | None = None,
        locale: str = "en_US",
    )-> list[dict]:
        """
        Normalize extracted deal candidates.
        """
        normalized_deals = []

        for candidate in candidates:
            normalized = self.normalizer.normalize(
                candidate,
                country_code=country_code,
                locale=locale,
            )

            normalized_deals.append(normalized)

        return normalized_deals

    def validate_deals(
        self,
        normalized_deals: list[dict],
        venue_id: int,
        source_url: str,
        source_hash: str,
        source_type: str = "website",
        confidence: float = 0.0,
    )->list[DealBase]:

        """
        Convert normalized deal dictionaries into validated DealBase objects.
        """

        validated_deals = []

        for deal in normalized_deals:

            deal_data = {
                "venue_id": venue_id,
                "title": deal["title"],
                "description": None,
                "deal_type": deal["deal_type"],
                "category": deal["category"],
                "discount_value": (
                    Decimal(str(deal["discount_value"]))
                    if deal["discount_value"] is not None
                    else None
                ),
                 "discount_unit": deal["discount_unit"],
                "money_expressions": deal["money_expressions"],
                "items": deal["items"],
                "days": deal["days"],
                "start_time": deal["start_time"],
                "end_time": deal["end_time"],
                "source_url": source_url,
                "source_type": source_type,
                "source_text": deal["title"],
                "source_hash": source_hash,
                "confidence": confidence,
                "is_active": True,
            }

            validated_deal = DealBase(**deal_data)

            validated_deals.append(validated_deal)

        return validated_deals

    def extract_deals(
        self,
        html: str,
        venue_id: int,
        source_url: str,
        source_hash: str,
        country_code: str | None = None,
        locale: str = "en_US",
        source_type: str = "website",
        confidence: float = 0.0,
    ) -> list[DealBase]:
        """
        Run the complete deal extraction pipeline.

        HTML
        -> clean text
        -> candidate detection
        -> normalization
        -> Pydantic validation
        """

        text = self.extract_text(html)

        candidates = self.find_candidates(text)

        normalized_deals = self.normalize_candidates(
            candidates,
            country_code=country_code,
            locale=locale,
        )

        validated_deals = self.validate_deals(
            normalized_deals,
            venue_id=venue_id,
            source_url=source_url,
            source_hash=source_hash,
            source_type=source_type,
            confidence=confidence,
        )

        return validated_deals

    def extract_deals_from_url(
        self,
        url: str,
        venue_id: int,
        source_hash: str,
        country_code: str | None = None,
        locale: str = "en_US",
        source_type: str = "website",
        confidence: float = 0.0,
    ) -> list[DealBase]:
        """
        Fetch a webpage and extract deals from it.

        URL
        -> fetch HTML
        -> extract deals
        """

        html = fetch_page(url)

        return self.extract_deals(
            html=html,
            venue_id=venue_id,
            source_url=url,
            source_hash=source_hash,
            country_code=country_code,
            locale=locale,
            source_type=source_type,
            confidence=confidence,
        )