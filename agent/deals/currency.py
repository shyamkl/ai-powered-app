import re
from babel import Locale, localedata
from babel.core import UnknownLocaleError
from babel.numbers import get_currency_symbol
from decimal import Decimal, InvalidOperation

from babel.numbers import parse_decimal


class CurrencyRegistry:

    AMOUNT_PATTERN = r"\d+(?:[.,]\d+)*"

    LOCALE_ALIASES = {
        "en_TH": "th_TH",
        "en_IN": "en_IN",
        "en_US": "en_US",
        "de_DE": "de_DE",
        "ja_JP": "ja_JP",
    }

    def __init__(self, locale: str = "en"):
        locale = self.LOCALE_ALIASES.get(locale, locale)

        self.locale = Locale.parse(locale)

        self.currencies = self.locale.currencies
        self.currency_codes = set(self.currencies.keys())

        self.code_to_symbol = {}
        self.symbol_to_codes = {}

        self._build_registry()
        self._build_global_symbol_registry()

    def _build_registry(self):
        for currency_code in self.currencies:

            symbol = self.locale.currency_symbols.get(
                currency_code,
                currency_code
            )

            self.code_to_symbol[currency_code] = symbol

    def _build_global_symbol_registry(self):
        for locale_identifier in localedata.locale_identifiers():

            try:
                locale = Locale.parse(locale_identifier)
            except Exception:
                continue

            for currency_code, symbol in locale.currency_symbols.items():

                if not symbol:
                    continue

                symbol = symbol.strip()
                
                if not symbol or symbol == currency_code:
                    continue

                if symbol not in self.symbol_to_codes:
                    self.symbol_to_codes[symbol] = set()


                self.symbol_to_codes[symbol].add(currency_code)

        self.symbol_to_codes = {
            symbol: sorted(codes)
            for symbol, codes in self.symbol_to_codes.items()
        }
    def get_symbol(self, currency_code: str) -> str:
        return self.code_to_symbol.get(
            currency_code,
            currency_code
        )        
    def find_currency_candidates(self, symbol:str) -> list[str]:
        return self.symbol_to_codes.get(symbol.strip(), []) 

    def is_currency_code(self, code: str) -> bool:
        return code.upper() in self.currency_codes 

    def find_currency_codes(self, text: str)-> list[str]:
        found_codes = []

        for word in text.split():
            cleaned_word = word.strip(".,!?;:()[]{}")

            upper_word = cleaned_word.upper()

            if upper_word in self.currency_codes:
                if upper_word not in found_codes:
                    found_codes.append(upper_word)

        return found_codes  

    def find_currency_symbols(self, text: str) -> list[dict]:
        found_symbols = []

        for symbol, currency_codes  in self.symbol_to_codes.items():

            if symbol in text:
                found_symbols.append(
                    {
                        "symbol": symbol,
                        "currency_candidates": currency_codes,
                    }
                )                          

        return found_symbols   

    # def find_money_expressions(self, text: str)-> list[dict]:
    #     expressions = []

    #     symbol_pattern = (
    #         r"(?P<symbol>[^\w\s])"
    #         r"\s*"
    #         r"(?p<amount>\d+(?:[.,]\d+)?)"
    #     )     

    #     for match in re.finder(
    #         symbol_pattern,
    #         text
    #     ):

    #         symbol = match.group("symbol")
    #         amount_text = match.group("amount")

    #         candidates = self.find_currency_candidates(symbol)

    #         if candidates:
    #             expressions.append(
    #                 {
    #                     "raw":match.group(0),
    #                     "amount": float(
    #                         amount_text.replace(",", ".")
    #                     ),
    #                     "symbol": symbol,
    #                     "currency_cadidates": candidates,
    #                     "position": "symbol_before_amount",
    #                 }
    #             )
    #         return expressions  

    def parse_amount(self, amount_text: str, locale: str = "en_US")-> Decimal | None:
        locale = self.LOCALE_ALIASES.get(locale, locale)
        try:
            return parse_decimal(
                amount_text,
                locale=locale
            )      
        except(InvalidOperation, ValueError, UnknownLocaleError):
            return None


    def find_money_expressions(
        self,
        text: str,
        locale: str = "en_US"
    ) -> list[dict]:

        expressions = []

        # --------------------------------------------------
        # Pattern 1: currency symbol followed by amount
        # Example: ₹100
        # --------------------------------------------------

        for symbol in self.symbol_to_codes:

            pattern = (
                r"(?<![A-Za-z])"
                + re.escape(symbol)
                + r"\s*"
                + r"(" + self.AMOUNT_PATTERN + r")"
            )

            for match in re.finditer(
                pattern,
                text
            ):
                amount_text = match.group(1)

                amount = self.parse_amount(
                    amount_text,
                    locale=locale
                )

                if amount is None:
                    continue

                expressions.append(
                    {
                        "raw": match.group(0),
                        "amount": amount,
                        "symbol": symbol,
                        "currency_candidates":
                            self.find_currency_candidates(symbol),
                        "position":
                            "symbol_before_amount",
                    }
                )

        # --------------------------------------------------
        # Pattern 2: amount followed by currency symbol
        # Example: 100₹
        # --------------------------------------------------

        for symbol in self.symbol_to_codes:

            pattern = (
                r"(" + self.AMOUNT_PATTERN + r")"
                + r"\s*"
                + re.escape(symbol)
                + r"(?![A-Za-z])"
            )

            for match in re.finditer(
                pattern,
                text
            ):
                amount_text = match.group(1)

                amount = self.parse_amount(
                    amount_text,
                    locale=locale
                )

                if amount is None:
                    continue

                expressions.append(
                    {
                        "raw": match.group(0),
                        "amount": amount,
                        "symbol": symbol,
                        "currency_candidates":
                            self.find_currency_candidates(symbol),
                        "position":
                            "amount_before_symbol",
                    }
                )

        # --------------------------------------------------
        # Pattern 3: currency code followed by amount
        # Example: INR 100
        # --------------------------------------------------

        for code in self.currency_codes:

            pattern = (
                r"\b"
                + re.escape(code)
                + r"\b"
                + r"\s*"
                + r"(" + self.AMOUNT_PATTERN + r")"
            )

            for match in re.finditer(
                pattern,
                text,
                re.IGNORECASE
            ):
                amount_text = match.group(1)

                amount = self.parse_amount(
                    amount_text,
                    locale=locale
                )

                if amount is None:
                    continue

                expressions.append(
                    {
                        "raw": match.group(0),
                        "amount": amount,
                        "currency": code.upper(),
                        "position":
                            "code_before_amount",
                    }
                )
    # --------------------------------------------------
    # Pattern 4: amount followed by currency code
    # Example: 100 INR
    # --------------------------------------------------

        for code in self.currency_codes:

            pattern = (
                r"(" + self.AMOUNT_PATTERN + r")"
                + r"\s*"
                + r"\b"
                + re.escape(code)
                + r"\b"
            )

            for match in re.finditer(
                pattern,
                text,
                re.IGNORECASE
            ):
                amount_text = match.group(1)

                amount = self.parse_amount(
                    amount_text,
                    locale=locale
                )

                if amount is None:
                    continue

                expressions.append(
                    {
                        "raw": match.group(0),
                        "amount": amount,
                        "currency": code.upper(),
                        "position":
                            "amount_before_code",
                    }
                )
        return expressions

        
        #         if currency_code not in self.symbol_to_codes[symbol]:
        #             self.symbol_to_codes[symbol].append(currency_code)    

        # def get_symbol(self, currency_code: str) -> str:
        #     return self.code_to_symbol.get(
        #         currency_code,
        #         currency_code
        #     )

        # def find_currency_candidates(self, symbol: str)-> list[str]:
        #     return self.symbol_to_codes.get(symbol, [])
        