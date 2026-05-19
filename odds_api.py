import requests
from config import ODDS_API_KEY

def get_odds():
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds"

    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "eu",
        "markets": "h2h"
    }

    return requests.get(url, params=params).json()