# src\RAD_trading\data_providers\mt5_provider.py
import MetaTrader5 as mt5
import pandas as pd
from .base_provider import BaseDataProvider
class MT5DataProvider(BaseDataProvider):
    def __init__(self):
        if not mt5.initialize():
            print("initialize() failed")
            mt5.shutdown()
    def get_historical_data(self, symbol, timeframe, start_date, end_date):
        rates = mt5.copy_rates_range(symbol, timeframe, start_date, end_date)
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        return df
    def __del__(self):
        mt5.shutdown()
