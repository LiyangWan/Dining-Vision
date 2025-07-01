CITY_CONTEXT = {
    "New York, NY": {
        "population": 8_398_748,
        "median_income": 63_000,
        "area_km2": 783.8,
        "timezone": "America/New_York",
        "avg_annual_temp_c": 13.3,
        "median_home_price_usd": 680_000,
        "safety_index": 46.6,             # 0 (safe) to 100 (unsafe)
        "public_transport_score": 85.0,   # 0–100
        "gdp_per_capita_usd": 85_000,
        "tourism_index": 90.0             # 0–100
    },
        "NYC": {
        "population": 8_398_748,
        "median_income": 63_000,
        "area_km2": 783.8,
        "timezone": "America/New_York",
        "avg_annual_temp_c": 13.3,
        "median_home_price_usd": 680_000,
        "safety_index": 46.6,             # 0 (safe) to 100 (unsafe)
        "public_transport_score": 85.0,   # 0–100
        "gdp_per_capita_usd": 85_000,
        "tourism_index": 90.0             # 0–100
    },
    "San Francisco, CA": {
        "population": 883_305,
        "median_income": 112_000,
        "area_km2": 121.4,
        "timezone": "America/Los_Angeles",
        "avg_annual_temp_c": 14.1,
        "median_home_price_usd": 1_300_000,
        "safety_index": 40.1,
        "public_transport_score": 75.0,
        "gdp_per_capita_usd": 130_000,
        "tourism_index": 85.0
    },
        "SF": {
        "population": 883_305,
        "median_income": 112_000,
        "area_km2": 121.4,
        "timezone": "America/Los_Angeles",
        "avg_annual_temp_c": 14.1,
        "median_home_price_usd": 1_300_000,
        "safety_index": 40.1,
        "public_transport_score": 75.0,
        "gdp_per_capita_usd": 130_000,
        "tourism_index": 85.0
    },
    "Champaign, IL": {
        "population": 88_909,
        "median_income": 45_000,
        "area_km2": 56.5,
        "timezone": "America/Chicago",
        "avg_annual_temp_c": 11.6,
        "median_home_price_usd": 250_000,
        "safety_index": 55.0,
        "public_transport_score": 30.0,
        "gdp_per_capita_usd": 45_000,
        "tourism_index": 45.0
    },
}


def get_city_context(city: str) -> dict:
    default = {
        "population": None,
        "median_income": None,
        "area_km2": None,
        "timezone": None,
        "avg_annual_temp_c": None,
        "median_home_price_usd": None,
        "safety_index": None,
        "public_transport_score": None,
        "gdp_per_capita_usd": None,
        "tourism_index": None
    }
    return CITY_CONTEXT.get(city, default)