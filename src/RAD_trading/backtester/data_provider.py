# src\RAD_trading\backtester\data_provider.py
import MetaTrader5 as mt5
import pandas as pd
def get_ohlc_history(symbol, timeframe, start_date, end_date):
    mt5.initialize()
    rates = mt5.copy_rates_range(symbol, timeframe, start_date, end_date)
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df
