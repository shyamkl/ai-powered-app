from agent.deals.fetcher import fetch_page


url = "https://example.com"

print("=" * 60)
print("TEST FETCHER")
print("=" * 60)

html = fetch_page(url)

print("URL:", url)
print("HTML LENGTH:", len(html))

print()
print("FIRST 500 CHARACTERS:")
print(html[:500])

print()
print("=" * 60)
print("FETCH TEST PASSED")
print("=" * 60)