# src\RAD_trading\indicators\moving_averages.py
import pandas as pd
def simple_moving_average(data, period, column='close'):
    return data[column].rolling(window=period).mean()
def exponential_moving_average(data, period, column='close'):
    return data[column].ewm(span=period, adjust=False).mean()
