import re

from .keywords import CATEGORY_KEYWORDS
from .currency import CurrencyRegistry
from .currency_context import CurrencyContextResolver


class DealNormalizer:
    """
    Converts deal text into structured information.
    """
    def __init__(self):
        self.currency_registry = CurrencyRegistry()
        self.currency_context = CurrencyContextResolver()

    DAYS = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    def find_amount_discounts(self, text:str)-> list[dict]:
        matches = []

        pattern = r"(₹|\$|€|£)\s*(\d+(?:\.\d+)?)\s*off"
        for match in re.finditer(pattern, text, re.IGNORECASE):
            currency = match.group(1)
            amount = float(match.group(2))

            if currency == "₹":
                unit = "INR"
            elif currency == "$":
                unit =  "USD"
            elif currency == "€":
                unit = "EUR"
            elif currency == "£":
                unit = "GBP"

            matches.append(
                {
                    "discount_value": amount,
                    "discount_unit" : unit,
                }
            )                  
        return matches

    def find_money_expressions(
        self,
        text: str,
        country_code: str | None = None,
        locale: str = "en_Us"
    )-> list[dict]:
        """
        Find money expressions and resolve their currency
        using optional country context.
        """

        expressions = self.currency_registry.find_money_expressions(
            text,
            locale=locale
        )

        resolved_expressions = []

        for expression in expressions:

            resolved = self.currency_context.resolve_money_expression(
                expression,
                country_code=country_code
            )

            resolved_expressions.append(resolved)

        return resolved_expressions    

        
    def normalize(self, text: str, country_code: str | None = None, locale: str = "en_Us") -> dict:
        """
        Convert one deal sentence into structured information.
        """

        result = {
            "title": text,
            "deal_type": "Unknown",
            "category": None,
            "discount_value": None,
            "discount_unit": None,
            "items": [],
            "days": [],
            "start_time": None,
            "end_time": None,
            "offers": [],
            "money_expressions": [],
        }

        lower_text = text.lower()

        # -------------------------------------------------
        # DEAL TYPE
        # -------------------------------------------------

        if "happy hour" in lower_text or "happy-hour" in lower_text:
            result["deal_type"] = "happy_hour"

        elif (
            "buy one get one" in lower_text
            or "bogo" in lower_text
        ):
            result["deal_type"] = "bogo"

        elif "free" in lower_text:
            result["deal_type"] = "free_item"

        elif "%" in text and "off" in lower_text:
            result["deal_type"] = "percentage_discount"

        elif self.find_money_expressions(
            text,
            country_code=country_code,
            locale=locale,
        ):
            result["deal_type"] = "fixed_price"

        # -------------------------------------------------
        # DISCOUNT
        # -------------------------------------------------

        discount_match = re.search(
            r"(\d+)\s*%",
            text
        )

        if discount_match:
            result["discount_value"] = int(
                discount_match.group(1)
            )
            result["discount_unit"] = "%"

        # -------------------------------------------------
        # CATEGORY + ITEMS
        # -------------------------------------------------

        matched_categories = []
        matched_items = []

        lower_text = text.lower()

        for category, items in CATEGORY_KEYWORDS.items():

            category_found = False

            for canonical_item, variants in items.items():

                for variant in variants:

                    pattern = r"\b" + re.escape(variant) + r"\b"

                    if re.search(pattern, lower_text, re.IGNORECASE):

                        category_found = True

                        if canonical_item not in matched_items:
                            matched_items.append(canonical_item)

                        break

            if category_found:

                if category not in matched_categories:
                    matched_categories.append(category)

            # -------------------------------------------------
            # Store category
            # -------------------------------------------------

                if len(matched_categories) == 1:

                    result["category"] = matched_categories[0]

                elif len(matched_categories) > 1:

                    result["category"] = matched_categories

                else:

                    result["category"] = None

            # -------------------------------------------------
            # Store items
            # -------------------------------------------------


                result["items"] = matched_items
                

        # -------------------------------------------------
        # DAYS
        # -------------------------------------------------

        result["days"] = self.find_days(text)

        # -------------------------------------------------
        # TIME RANGE
        # -------------------------------------------------

        start_time, end_time = self.find_time_range(text)

        result["start_time"] = start_time
        result["end_time"] = end_time

        # -------------------------------------------------
        # DISCOUNT + ITEM RELATIONSHIP
        # -------------------------------------------------

        result["offers"] = self.find_offers(text)

        # -------------------------------------------------
        # MONEY EXPRESSIONS
        # -------------------------------------------------


        result["money_expressions"] = self.find_money_expressions(
            text,
            country_code = country_code,
            locale=locale
        )

        return result

    # =================================================
    # FIND DAYS
    # =================================================

    def find_days(self, text: str) -> list[str]:
        """
        Find weekdays mentioned in the deal text.
        """

        found_days = []

        lower_text = text.lower()

        for day in self.DAYS:

            if day.lower() in lower_text:
                found_days.append(day)

        return found_days

    # =================================================
    # FIND TIME RANGE
    # =================================================

    def find_time_range(
        self,
        text: str
    ) -> tuple[str | None, str | None]:
        """
        Find a start and end time from deal text.

        Examples:

        5 PM to 7 PM
        5 PM - 7 PM
        17:00 to 19:00
        """

        pattern = r"""
            (\d{1,2}(?::\d{2})?\s*(?:AM|PM|am|pm)?)
            \s*
            (?:to|-)
            \s*
            (\d{1,2}(?::\d{2})?\s*(?:AM|PM|am|pm)?)
        """

        match = re.search(
            pattern,
            text,
            re.VERBOSE
        )

        if not match:
            return None, None

        start_time = match.group(1).strip()
        end_time = match.group(2).strip()

        return start_time, end_time

    # =================================================
    # FIND ALL DISCOUNTS
    # =================================================

    def find_discounts(self, text: str) -> list[int]:
        """
        Find all percentage discounts mentioned
        in the deal text.
        """

        matches = re.findall(
            r"(\d+)\s*%",
            text
        )

        return [
            int(value)
            for value in matches
        ]

    # =================================================
    # FIND OFFERS
    # =================================================

    def find_offers(self, text: str) -> list[dict]:
        """
        Connect each percentage discount with the
        item(s) belonging to that discount.

        Examples:

        30% off pizza
        -> 30% pizza

        20% off pizza and pasta
        -> 20% pizza
        -> 20% pasta

        50% off cocktails and 30% off pizza
        -> 50% cocktails
        -> 30% pizza
        """

        offers = []

        # -------------------------------------------------
        # Find all percentage discounts
        # -------------------------------------------------

        discount_matches = list(
            re.finditer(
                r"(\d+)\s*%\s*off",
                text,
                re.IGNORECASE
            )
        )

        if not discount_matches:
            return offers

        # -------------------------------------------------
        # Find all known items
        # -------------------------------------------------

        item_matches = []

        lower_text = text.lower()

        for category, items in CATEGORY_KEYWORDS.items():

            for canonical_item, variants in items.items():

                for variant in variants:

                    pattern = r"\b" + re.escape(variant) + r"\b"

                    for match in re.finditer(
                        pattern,
                        lower_text
                    ):
                        item_matches.append(
                            {
                                "item": canonical_item,
                                "category": category,
                                "start": match.start(),
                                "end": match.end()

                                    }
                        )

        item_matches.sort(
            key=lambda x: x["start"]
        )
       
        # -------------------------------------------------
        # Connect discounts to their items
        # -------------------------------------------------

        for index, discount in enumerate(discount_matches):

            discount_value = int(
                discount.group(1)
            )

            discount_end = discount.end()

            # The next discount marks the end
            # of the current discount section.
            if index + 1 < len(discount_matches):
                next_discount_start = (
                    discount_matches[index + 1].start()
                )
            else:
                next_discount_start = len(text)

            section_items = []

            for item in item_matches:

                if (
                    item["start"] >= discount_end
                    and item["start"] < next_discount_start
                ):
                    section_items.append(item)

            # Create one offer for every item
            # in this discount section.
            seen_items = set()

            for item in section_items:

                canonical_item = item["item"]

                if canonical_item in seen_items:
                    continue

                seen_items.add(canonical_item)
                
                offers.append(
                    {
                        "discount_value": discount_value,
                        "discount_unit": "%",
                        "item": item["item"],
                    }
                )

        return offers