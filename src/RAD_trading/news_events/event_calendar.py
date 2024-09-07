# src\RAD_trading\news_events\event_calendar.py
import pandas as pd
import requests
from datetime import datetime, timedelta
class EconomicCalendar:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.tradingeconomics.com/calendar"
    def get_events(self, countries, from_date, to_date):
        params = {
            'c': ','.join(countries),
            'd1': from_date.strftime('%Y-%m-%d'),
            'd2': to_date.strftime('%Y-%m-%d'),
            'api_key': self.api_key
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            events = response.json()
            return pd.DataFrame(events)
        else:
            raise Exception(f"Failed to fetch economic events. Status code: {response.status_code}")
