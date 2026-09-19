import requests

def fetch_page(url:str) -> str:
    """
    Fetch HTML content from a webpage URL.
    """
    headers = {
        "User-Agent":(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        )
    }
    response = requests.get(
        url,
        headers=headers,
        timeout=10,
    )

    response.raise_for_status()

    return response.text
    
