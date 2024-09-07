# src\RAD_trading\indicators\bollinger_bands.py
import pandas as pd
import numpy as np
def bollinger_bands(data, period=20, num_std=2, column='close'):
    sma = data[column].rolling(window=period).mean()
    std = data[column].rolling(window=period).std()
    upper_band = sma + (std * num_std)
    lower_band = sma - (std * num_std)
    return pd.DataFrame({'middle': sma, 'upper': upper_band, 'lower': lower_band})
