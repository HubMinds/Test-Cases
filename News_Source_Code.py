import requests
import os
from dotenv import load_dotenv

def fetch_news_headlines(country="", source="", category="", query=""):
    load_dotenv()
    api_key = os.getenv("NEWS_KEY")

    url = "https://newsapi.org/v2/top-headlines"
    params = {"apiKey": api_key}

    if source:
        params["sources"] = source
    elif country:
        params["country"] = country
    elif category:
        params["category"] = category
    elif query:
        params["q"] = query

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data["totalResults"] > 0:
            return data["articles"]
        else:
            return []
    else:
        return None
