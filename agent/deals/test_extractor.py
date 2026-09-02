from agent.deals.extractor import DealExtractor

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

if __name__ == "__main__":
    main()       