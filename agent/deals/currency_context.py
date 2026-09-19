from babel import Locale, localedata
from babel.numbers import get_territory_currencies


class CurrencyContextResolver:

    def __init__(self):
        self.country_to_currency = {}

        self._build_country_currency_registry()

    def _build_country_currency_registry(self):
        for locale_identifier in localedata.locale_identifiers():

            try:
                locale = Locale.parse(locale_identifier)
            except Exception:
                continue

            territory = locale.territory

            if not territory:
                continue

            try:
                currencies = get_territory_currencies(
                    territory,
                    tender= True
                )
            except Exception:
                continue

            if not currencies:
                continue

            self.country_to_currency[territory] = currencies[0]

    def get_country_currency(self, country_code: str)-> str | None:

        if not country_code:
            return None

        country_code = country_code.upper()

        return self.country_to_currency.get(country_code)

    def resolve_currency(
        self,
        candidates: list[str],
        country_code:str | None = None
    )-> str | None:

        if not candidates:
            return None

        if len(candidates) == 1:
            return candidates[0]

        if not country_code:
            return None

        country_currency = self.get_country_currency(
            country_code
        )

        if not country_currency:
            return None

        if country_currency in candidates:
            return country_currency

        return None

    def resolve_money_expression(
            self,
            expression: dict,
            country_code: str | None = None
    )  -> dict:

        candidates = expression.get(
            "currency_candidates",
            []
        )

        resolved_currency = self.resolve_currency(
            candidates,
            country_code=country_code
        )

        result = expression.copy()

        result["currency"] = resolved_currency

        return result