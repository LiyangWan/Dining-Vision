from flask import Flask, request, jsonify
from apis.google_api import fetch_places, normalize
from enrichment import get_city_context
import pandas as pd
import os, time

app = Flask(__name__)

@app.route("/_health")
def health():
    return "OK", 200

@app.route("/test/google")
def test_google():
    city = request.args.get("city", "San Francisco, CA")
    raw = fetch_places(f"restaurants in {city}")
    return jsonify({"count": len(raw), "sample": raw[:3]})

@app.route("/restaurants")
def restaurants():
    city = request.args.get("city")
    if not city:
        return jsonify({"error":"?city= required"}), 400

    raw = fetch_places(f"restaurants in {city}")
    normed = [normalize(x) for x in raw]
    df = pd.DataFrame(normed)
    df["coord_key"] = df["lat"].round(4).astype(str)+"_"+df["lng"].round(4).astype(str)
    df = df.drop_duplicates(subset=["name","coord_key"]).drop(columns="coord_key")

    # save
    csv_fn = f"{city.lower().replace(' ','_')}_restaurants.csv"
    json_fn= f"{city.lower().replace(' ','_')}_restaurants.json"
    df.to_csv(csv_fn, index=False)
    df.to_json(json_fn, orient="records", lines=True)

    return jsonify(df.to_dict(orient="records"))

def build_restaurant_df(city: str) -> pd.DataFrame:
    """
    Fetches, normalizes and deduplicates Google Places restaurant data for the given city.
    """
    raw = fetch_places(f"restaurants in {city}")
    normed = [normalize(item) for item in raw]
    df = pd.DataFrame(normed)
    # dedupe by name + rounded coords
    df["coord_key"] = df["lat"].round(4).astype(str) + "_" + df["lng"].round(4).astype(str)
    df = df.drop_duplicates(subset=["name", "coord_key"]).drop(columns=["coord_key"])
    return df

@app.route("/restaurants/top")
def top_restaurants():
    """
    GET /restaurants/top?city=SF&limit=10
    GET /restaurants/top?city=NYC&limit=20&price_level=4
    Returns the top-N restaurants by rating, optionally filtered by max price_level.
    """
    city = request.args.get("city", "").strip()
    if not city:
        return jsonify({"error": "?city= required"}), 400

    # parse parameters
    limit       = int(request.args.get("limit", 10))
    price_level = request.args.get("price_level")

    df = build_restaurant_df(city)
    # only consider entries with a rating
    df = df.dropna(subset=["rating"])

    # apply price filter if provided
    if price_level is not None:
        max_price = int(price_level)
        df = df[df["price_level"].notna() & (df["price_level"] <= max_price)]

    # sort & limit
    df = df.sort_values("rating", ascending=False).head(limit)
    return jsonify(df.to_dict(orient="records"))

@app.route("/stats/city/<string:city>")
def stats_city(city):
    """
    GET /stats/city/NYC
    Returns summary statistics + enrichment for a city.
    """
    df      = build_restaurant_df(city)
    context = get_city_context(city)

    # compute averages (or None if no data)
    avg_rating = round(df["rating"].mean(), 2) if not df["rating"].dropna().empty else None
    avg_price  = round(df["price_level"].dropna().mean(), 2) if not df["price_level"].dropna().empty else None

    stats = {
        "city": city,
        **context,
        "restaurant_count": len(df),
        "average_rating": avg_rating,
        "average_price_level": avg_price
    }
    return jsonify(stats)

if __name__=="__main__":
    app.run(debug=True, port=5000)
