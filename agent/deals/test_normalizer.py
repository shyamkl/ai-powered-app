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

if __name__=="__main__":
    main()


