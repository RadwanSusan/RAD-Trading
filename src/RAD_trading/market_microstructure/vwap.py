# src\RAD_trading\market_microstructure\vwap.py
import pandas as pd
def calculate_vwap(data):
    """
    Calculate Volume Weighted Average Price (VWAP).
    :param data: DataFrame with 'price' and 'volume' columns
    :return: Series of VWAP values
    """
    v = data['volume']
    tp = (data['high'] + data['low'] + data['close']) / 3
    return (tp * v).cumsum() / v.cumsum()
