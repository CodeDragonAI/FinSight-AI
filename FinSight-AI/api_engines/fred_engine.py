import os
from dotenv import load_dotenv
load_dotenv()

import requests

FRED_API_KEY = os.getenv("FRED_API_KEY")

BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

def get_fred_data(series_id: str):
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "sort_order": "desc",
        "limit": 1
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "observations" in data and data["observations"]:
        latest = data["observations"][0]
        return f"{series_id}: {latest['value']} (Date: {latest['date']})"
    
    return "No data found"





