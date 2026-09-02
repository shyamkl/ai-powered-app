from agent.deals.fetcher import fetch_page

html = fetch_page("https://youtube.com")
print(html[:500])