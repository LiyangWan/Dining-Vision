# app/main.py
from flask import Flask, request, jsonify
from apis.google_api import fetch_places, normalize
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

if __name__=="__main__":
    app.run(debug=True, port=5000)