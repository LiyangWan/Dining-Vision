# Dining-Vision
Backend Pipeline for Restaurant Intelligence using Public APIs

# 1. Prerequisites  
Python 3.10+

# 2. Dependencies
pip install -r requirements.txt

# 3. Configure API keys
In Dining-Vision/.env file, update the variable GOOGLE_API_KEY with your own API key.

# 4. Run the Flask server
python app/main.py

# 5. API Usage Guide
Below are the available endpoints. All responses are in 5JSON.

1) Health Check:
Endpoint: GET /_health
Description: Verifies the service is running.
Response: OK (HTTP 200)

3) All Restaurants:
Endpoint: GET /restaurants?city=<CITY>
Description: Fetches, normalizes, deduplicates restaurant data for the specified city, saves CSV and JSON to data/, and returns the JSON file as a download.
Data:
The data will be saved in both .csv and .json format in Dining-Vision/data
Query Parameters:
city

Example:
curl -v "http://localhost:5000/restaurants?city=NYC"

3) Top-N Restaurants:
Endpoint: GET /restaurants/top?city=<CITY>&limit=<N>[&price_level=<P>]
Description: Returns the top-N restaurants by rating in the given city, optionally filtered by maximum price level.

Query Parameters:
city (required)
limit (optional, default 10): Number of top entries to return
price_level (optional): Maximum price_level (integer)

Examples:
curl "http://localhost:5000/restaurants/top?city=SF&limit=10"
curl "http://localhost:5000/restaurants/top?city=NYC&limit=20&price_level=4"

4) City Statistics: 
Endpoint: GET /stats/city/<CITY>
Description: Returns summary statistics (restaurant count, average rating, average price level) plus contextual enrichment (population, median income, area, etc.) for the specified city.

Path Parameter:
CITY

Example:
curl "http://localhost:5000/stats/city/NYC"

# 6. Data Directory
When running All Restaurants function, the data will be saved in both .csv and .json format in Dining-Vision/data. Examples of NYC is already inside.

# 7. Deployment
Create a new Web Service on Render.com:
Build Command: pip install -r requirements.txt
Start Command: gunicorn app.main:app --bind 0.0.0.0:$PORT
Environment Variables: GOOGLE_API_KEY

Render will provide a public URL for your service.

# 8.Scripts
A fetch_and_store.py file is provided for quick and easy test API call and All Restaurant data download
