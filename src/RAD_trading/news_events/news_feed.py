# src\RAD_trading\news_events\news_feed.py
import requests
from datetime import datetime
class NewsFeed:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2/everything"
    def get_news(self, keywords, from_date, to_date, language='en', sort_by='publishedAt'):
        params = {
            'q': keywords,
            'from': from_date.strftime('%Y-%m-%d'),
            'to': to_date.strftime('%Y-%m-%d'),
            'language': language,
            'sortBy': sort_by,
            'apiKey': self.api_key
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            return response.json()['articles']
        else:
            raise Exception(f"Failed to fetch news. Status code: {response.status_code}")
