from flask import Flask, request, jsonify, render_template, redirect, url_for
from app.apis.google_api import fetch_places, normalize
from enrichment import get_city_context
import pandas as pd
import os

app = Flask(__name__)

def build_restaurant_df(city: str) -> pd.DataFrame:
    raw = fetch_places(f"restaurants in {city}")
    normed = [normalize(item) for item in raw]
    df = pd.DataFrame(normed)
    # dedupe
    df["coord_key"] = (
        df["lat"].round(4).astype(str)
        + "_"
        + df["lng"].round(4).astype(str)
    )
    return df.drop_duplicates(subset=["name", "coord_key"]).drop(columns="coord_key")


# ———————— UI ROUTES ——————————————————————————————————————————————

app_dir  = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(app_dir)
DATA_DIR = os.path.join(base_dir, "data")
os.makedirs(DATA_DIR, exist_ok=True)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/restaurants_ui", methods=["GET", "POST"])
def restaurants_ui():
    data = None
    if request.method == "POST":
        city = request.form["city"].strip()
        df = build_restaurant_df(city)
        data = df.to_dict(orient="records")

        csv_path  = os.path.join(DATA_DIR, f"{city}_restaurants.csv")
        json_path = os.path.join(DATA_DIR, f"{city}_restaurants.json")
        
        df.to_csv(csv_path, index=False)
        df.to_json(json_path, orient="records", lines=True)
    return render_template("restaurants.html", restaurants=data)


@app.route("/top_restaurants_ui", methods=["GET", "POST"])
def top_restaurants_ui():
    data = None
    if request.method == "POST":
        city = request.form["city"].strip()
        limit = int(request.form.get("limit", 10))
        price_lvl = request.form.get("price_level")
        df = build_restaurant_df(city).dropna(subset=["rating"])
        if price_lvl:
            df = df[df["price_level"].notna() & (df["price_level"] <= int(price_lvl))]
        df = df.sort_values("rating", ascending=False).head(limit)
        data = df.to_dict(orient="records")
    return render_template("top_restaurants.html", restaurants=data)


@app.route("/stats_ui", methods=["GET", "POST"])
def stats_ui():
    stats = None
    if request.method == "POST":
        city = request.form["city"].strip()
        df = build_restaurant_df(city)
        ctx = get_city_context(city)
        avg_rating = round(df["rating"].mean(), 2) if not df["rating"].dropna().empty else None
        avg_price  = round(df["price_level"].dropna().mean(), 2) if not df["price_level"].dropna().empty else None

        stats = {
            "city": city,
            **ctx,
            "restaurant_count": len(df),
            "average_rating": avg_rating,
            "average_price_level": avg_price
        }
    return render_template("stats.html", stats=stats)

@app.route("/restaurants")
def restaurants():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "?city= required"}), 400
    
    csv_path  = os.path.join(DATA_DIR, f"{city}_restaurants.csv")
    json_path = os.path.join(DATA_DIR, f"{city}_restaurants.json")
    
    df.to_csv(csv_path, index=False)
    df.to_json(json_path, orient="records", lines=True)

    df = build_restaurant_df(city)
    return jsonify(df.to_dict(orient="records"))


@app.route("/restaurants/top")
def top_restaurants():
    city = request.args.get("city", "").strip()
    limit = int(request.args.get("limit", 10))
    price_lvl = request.args.get("price_level")

    df = build_restaurant_df(city).dropna(subset=["rating"])
    if price_lvl:
        df = df[df["price_level"].notna() & (df["price_level"] <= int(price_lvl))]
    df = df.sort_values("rating", ascending=False).head(limit)
    return jsonify(df.to_dict(orient="records"))


@app.route("/stats/city/<string:city>")
def stats_city(city):
    df  = build_restaurant_df(city)
    ctx = get_city_context(city)
    avg_rating = round(df["rating"].mean(), 2) if not df["rating"].dropna().empty else None
    avg_price  = round(df["price_level"].dropna().mean(), 2) if not df["price_level"].dropna().empty else None

    return jsonify({
        "city": city,
        **ctx,
        "restaurant_count": len(df),
        "average_rating": avg_rating,
        "average_price_level": avg_price
    })


@app.route("/_health")
def health():
    return "OK", 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
