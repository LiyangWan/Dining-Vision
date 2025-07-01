import os
import time
import requests
import pandas as pd
# import sys
# from dotenv import load_dotenv


GOOGLE_API_KEY = 'Your API Here'
GOOGLE_PLACES_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"

CITIES = [
    "Champaign, IL" # ,
    # "New York, NY",
    # "Los Angeles, CA"
]

def fetch_google_places(query: str, api_key: str,page_limit: int = 3, delay: float = 2.0) -> list:
    params = {"query": query, "key": api_key}
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
        params = {"pagetoken": token, "key": api_key}
    return results

def normalize_google(item: dict) -> dict:
    return {
        "name": item.get("name"),
        "rating": item.get("rating"),
        "price_level": item.get("price_level"),
        "lat": item["geometry"]["location"]["lat"],
        "lng": item["geometry"]["location"]["lng"],
        "source": "google"
    }

def aggregate_restaurants(city: str) -> pd.DataFrame:
    """
    1) Fetch raw Google Place results
    2) Normalize fields
    3) Deduplicate by name + rounded coords
    """
    raw = fetch_google_places(f"restaurants in {city}", GOOGLE_API_KEY)
    normed = [normalize_google(r) for r in raw]
    df = pd.DataFrame(normed)

    # dedup by name + rounded coords
    df["coord_key"] = (
        df["lat"].round(4).astype(str)
        + "_"
        + df["lng"].round(4).astype(str)
    )
    df = df.drop_duplicates(subset=["name", "coord_key"])
    return df.drop(columns="coord_key")

# Save functions
def save_to_csv(df: pd.DataFrame, city: str):
    filename = f"{city.lower().replace(' ','_')}_restaurants.csv"
    df.to_csv(filename, index=False)
    print(f"[saved CSV] {filename}")

def save_to_json(df: pd.DataFrame, city: str):
    filename = f"{city.lower().replace(' ','_')}_restaurants.json"
    df.to_json(filename, orient="records", lines=True)
    print(f"[saved JSON] {filename}")

# Main Execution
def fetch_and_store_data(city: str):
    print(f"Fetching restaurant data for: {city}")
    df = aggregate_restaurants(city)
    if df.empty:
        print("No data returned.")
        return df
    save_to_csv(df, city)
    save_to_json(df, city)
    print(f"Done. {len(df)} unique restaurants saved.")
    return df

# if __name__ == "__main__":
#     if len(sys.argv) >= 2:
#         city_input = " ".join(sys.argv[1:])
#     else:
#         city_input = input("Enter city (e.g. 'New York, NY'): ").strip()
#     fetch_and_store_data(city_input)

if __name__ == "__main__":
    for city in CITIES:
        fetch_and_store_data(city)