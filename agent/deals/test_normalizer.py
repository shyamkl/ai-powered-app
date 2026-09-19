from decimal import Decimal
from agent.deals.normalizer import DealNormalizer


def main():

    normalizer = DealNormalizer()

    test_deals = [
    "Happy Hour: 50% off cocktails from 5 PM to 7 PM",

    "Buy one get one free beer every Friday",

    "30% off pizza every Monday",

    "20% off pizza and pasta every Tuesday",

    "50% off cocktails and 30% off pizza every Friday",

    "Free cake and ice cream every Sunday",
    ]

    for text in test_deals:
        print("=" * 60)
        print("INPUT:")
        print(text)

        result = normalizer.normalize(text)

        print("OUTPUT:")
        print(result)

    # text = "Happy Hour: 50% off cocktails from 5 PM to 7 PM"

    # result = normalizer.normalize(text)

    # print(result)
    print("="*60)
    print("Testing multiple discounts")

    text = "50% off cocktails and 30% off pizza every Friday"

    result = normalizer.find_discounts(text)

    print("Input: ")
    print(text)

    print("Discounts Found")
    print(result)

    print("=" *60)
    print("TESTING DISCOUNTS + ITEMS RELATIONSHIP")

    text = "50% off cocktails and 30% off pizza every Friday"

    result  = normalizer.find_offers(text)

    print("INPUT:")
    print(text)

    print("DISCOUNT + ITEM:")
    print(result)

    print(
            normalizer.find_amount_discounts("₹100 off cocktails")
    )

    print(
        normalizer.find_amount_discounts("$5 off burgers")
    )

    print(
    normalizer.find_amount_discounts(
        "€10 off pizza")
    )

    print(
        normalizer.find_amount_discounts(
            "£20 off wine"
        )
    )

    print(
        normalizer.find_amount_discounts(
            "₹25.50 off pasta"
        )
    )

    print(
        normalizer.find_amount_discounts(
            "₹100 off cocktails and ₹50 off pizza"
        )
    )

    print()
    print("=" * 60)
    print("TESTING CURRENCY IN DEAL NORMALIZER")
    print("=" * 60)

    
    currency_deals = [
        (
            "Happy Hour: 50% off cocktails for $10 in New York",
            "US",
            "en_US",
            "USD"
        ),
        (
            "30% off pizza for ₹500 in India",
            "IN",
            "en_IN",
            "INR"
        ),
        (
            "20% off beer for €5,50 in Germany",
            "DE",
            "de_DE",
            "EUR"
        ),
        (
            "Happy Hour: ¥1,000 cocktails in Japan",
            "JP",
            "ja_JP",
            "JPY"
        ),
        (
            "Happy Hour: ¥1,000 cocktails in China",
            "CN",
            "ja_JP",
            "CNY"
        ),
    ]


    for text, country_code, locale, expected_currency in currency_deals:

        print()
        print("INPUT:")
        print(text)

        result = normalizer.normalize(
            text,
            country_code=country_code,
            locale=locale
        )

        print("MONEY EXPRESSIONS:")
        print(result["money_expressions"])

        assert len(result["money_expressions"]) == 1

        actual_currency = result["money_expressions"][0]["currency"]

        assert actual_currency == expected_currency, (
                f"Expected {expected_currency}, "
                f"but got {actual_currency}"
            )

        print("PASS:", actual_currency)

        print()
        print("ALL CURRENCY NORMALIZER TESTS PASSED!")

    print()
    print("=" * 60)
    print("CURRENCY IN NORMALIZED DEALS")
    print("=" * 60)

    normalizer = DealNormalizer()

    currency_tests = [
        {
            "text": "Happy Hour: Cocktails for $10 in New York",
            "country_code": "US",
            "expected_currency": "USD",
            "expected_amount": Decimal("10"),
        },
        {
            "text": "Happy Hour: Pizza for ₹500 in India",
            "country_code": "IN",
            "expected_currency": "INR",
            "expected_amount": Decimal("500"),
        },
        {
            "text": "Happy Hour: Wine for €12.50 in Germany",
            "country_code": "DE",
            "expected_currency": "EUR",
            "expected_amount": Decimal("12.50"),
        },
        {
            "text": "Happy Hour: Beer for ฿350 in Thailand",
            "country_code": "TH",
            "expected_currency": "THB",
            "expected_amount": Decimal("350"),
        },
    ]

    for test in currency_tests:
        result = normalizer.normalize(
            test["text"],
            country_code=test["country_code"],
            locale="en_US",
        )

        print()
        print("INPUT:", test["text"])
        print("COUNTRY:", test["country_code"])
        print("MONEY EXPRESSIONS:", result["money_expressions"])

        assert len(result["money_expressions"]) == 1

        money = result["money_expressions"][0]

        assert money["currency"] == test["expected_currency"]
        assert money["amount"] == test["expected_amount"]

        print("RESOLVED CURRENCY:", money["currency"])
        print("AMOUNT:", money["amount"])

    print()
    print("CURRENCY NORMALIZER TESTS PASSED")

if __name__=="__main__":
    main()


