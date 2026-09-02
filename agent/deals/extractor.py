from bs4 import BeautifulSoup


class DealExtractor:
    """
    Extracts possible deal- realted text from HTML

    """

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

            for keyword in self.DEAL_KEYWORDS:

                if keyword in lower:

                    candidates.append(cleaned)

                    break


        return candidates