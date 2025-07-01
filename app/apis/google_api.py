import time, requests
from os import getenv
from dotenv import load_dotenv

load_dotenv()
GOOGLE_PLACES_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
API_KEY = getenv("GOOGLE_API_KEY")


def fetch_places(query: str, page_limit: int = 3, delay: float = 2.0) -> list:
    params = {"query": query, "key": API_KEY}
    results = []

    for _ in range(page_limit):
        resp = requests.get(GOOGLE_PLACES_URL, params=params)
        resp.raise_for_status()
        data = resp.json()
        results.extend(data.get("results", []))
        token = data.get("next_page_token")
        if not token:
            break

        time.sleep(delay)
        params = {"pagetoken": token, "key": API_KEY}
    return results

def normalize(item: dict) -> dict:
    return {
        "name": item.get("name"),
        "rating": item.get("rating"),
        "price_level": item.get("price_level"),
        "lat": item["geometry"]["location"]["lat"],
        "lng": item["geometry"]["location"]["lng"],
        "source": "google"
    }
