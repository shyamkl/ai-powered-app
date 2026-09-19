from agent.deals.extractor import DealExtractor
from http.server import HTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from pathlib import Path

def main():

    html = """
       <html>
        <head>
            <title>ABC Restaurant</title>

            <script>
                console.log("This should be removed");
            </script>

            <style>
                body {
                    color: red;
                }
            </style>
        </head>

        <body>

            <h1>ABC Restaurant</h1>

            <p>Welcome to our restaurant.</p>

            <p>
                Happy Hour: 50% off cocktails from 5 PM to 7 PM.
            </p>

            <p>
                Buy one get one free beer every Friday.
            </p>

            <p>
                We also serve pizza and pasta.
            </p>

        </body>
    </html>

    """

    extractor = DealExtractor()

    print("=" * 60)
    print("STEP 1 : EXTRACT CLEAN TEXT")
    print("=" * 60)

    text  = extractor.extract_text(html)

    print(text)

    print()
    print("=" * 60)
    print("Find Deal candidates")
    print("=" * 60)


    candidates = extractor.find_candidates(text)

    for candidate in candidates:
        print("-", candidate)

    print()
    print("=" * 60)
    print("TOTAL CANDIDATES:", len(candidates))
    print("=" * 60)

    print()
    print("=" * 60)
    print("STEP 3 : NORMALIZE DEAL CANDIDATES")
    print("=" * 60)

    normalized_deals = extractor.normalize_candidates(
        candidates,
        country_code="US",
        locale="en_US",
    )

    for deal in normalized_deals:
        print()
        print("NORMALIZED DEAL:")
        print(deal)

    print()
    print("=" * 60)
    print("TOTAL NORMALIZED DEALS:", len(normalized_deals))
    print("=" * 60)

    print()
    print("=" * 60)
    print("STEP 4 : VALIDATE DEALS WITH DEALBASE")
    print("=" * 60)

    validated_deals = extractor.validate_deals(
        normalized_deals,
        venue_id=1,
        source_url="https://example.com/deals",
        source_hash="test-hash-extractor",
        source_type="website",
        confidence=0.95,
    )

    for deal in validated_deals:
        print()
        print("VALIDATED DEAL:")
        print(deal)

    print()
    print("=" * 60)
    print("TOTAL VALIDATED DEALS:", len(validated_deals))
    print("=" * 60)

    print()
    print("=" * 60)
    print("STEP 5 : END-TO-END EXTRACTION")
    print("=" * 60)

    extracted_deals = extractor.extract_deals(
        html,
        venue_id=1,
        source_url="https://example.com/deals",
        source_hash="test-hash-end-to-end",
        country_code="US",
        locale="en_US",
        source_type="website",
        confidence=0.95,
    )

    for deal in extracted_deals:
        print()
        print("EXTRACTED DEAL:")
        print(deal)

    print()
    print("=" * 60)
    print("TOTAL EXTRACTED DEALS:", len(extracted_deals))
    print("=" * 60)

    print()
    print("=" * 60)
    print("STEP 6 : EXTRACT DEALS FROM URL")
    print("=" * 60)

    test_file = Path(__file__).with_name("test_deal_page.html")

    class TestRequestHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(
                *args,
                directory=str(test_file.parent),
                **kwargs,
            )

        def log_message(self, format, *args):
            pass
    server = HTTPServer(
        ("localhost", 8000),
        TestRequestHandler,
    )

    server_thread = Thread(
        target=server.serve_forever,
        daemon=True,
    )

    server_thread.start()
    try:
        url = "http://localhost:8000/test_deal_page.html"

        url_deals = extractor.extract_deals_from_url(
            url=url,
            venue_id=1,
            source_hash="test-hash-url",
            country_code="US",
            locale="en_US",
            source_type="website",
            confidence=0.90,
        )

        for deal in url_deals:
            print()
            print("URL EXTRACTED DEAL:")
            print(deal)

        print()
        print("=" * 60)
        print("TOTAL URL EXTRACTED DEALS:", len(url_deals))
        print("=" * 60)

    finally:
        server.shutdown()
        server.server_close()
if __name__ == "__main__":
    main()       