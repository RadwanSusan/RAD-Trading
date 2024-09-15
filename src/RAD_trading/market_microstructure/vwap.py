# src\RAD_trading\market_microstructure\vwap.py
import pandas as pd


def calculate_vwap(data):
    """
    Calculate tick_volume Weighted Average Price (VWAP).
    :param data: DataFrame with 'price' and 'tick_volume' columns
    :return: Series of VWAP values
    """
    v = data["tick_volume"]
    tp = (data["high"] + data["low"] + data["close"]) / 3
    return (tp * v).cumsum() / v.cumsum()
