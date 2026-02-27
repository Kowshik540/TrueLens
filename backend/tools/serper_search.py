import requests
import os
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def search_claim(query: str) -> list:
    """
    Takes a search query string.
    Returns a list of top results from Google via Serper API.
    Each result has: title, snippet, link
    """
    try:
        response = requests.post(
            "https://google.serper.dev/search",
            headers={
                "X-API-KEY": SERPER_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "q": query,
                "num": 5
            }
        )

        data = response.json()
        results = []

        for item in data.get("organic", []):
            results.append({
                "title":   item.get("title", ""),
                "snippet": item.get("snippet", ""),
                "link":    item.get("link", "")
            })

        return results

    except Exception as e:
        print(f"Serper search error: {e}")
        return []