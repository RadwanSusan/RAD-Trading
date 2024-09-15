# src\RAD_trading\high_frequency\tick_data_analysis.py
import pandas as pd
import numpy as np


def analyze_tick_data(tick_data):
    """
    Analyze high-frequency tick data.
    :param tick_data: DataFrame of tick data with columns 'timestamp', 'price', 'tick_volume'
    :return: Dictionary of tick data analysis results
    """
    tick_data["timestamp"] = pd.to_datetime(tick_data["timestamp"])
    tick_data["return"] = tick_data["price"].pct_change()
    results = {
        "mean_return": tick_data["return"].mean(),
        "volatility": tick_data["return"].std() * np.sqrt(len(tick_data)),
        "skewness": tick_data["return"].skew(),
        "kurtosis": tick_data["return"].kurtosis(),
        "mean_volume": tick_data["tick_volume"].mean(),
        "median_volume": tick_data["tick_volume"].median(),
        "volume_volatility": tick_data["tick_volume"].std(),
        "price_volume_correlation": tick_data["price"].corr(tick_data["tick_volume"]),
    }
    # Calculate inter-trade durations
    tick_data["duration"] = tick_data["timestamp"].diff().dt.total_seconds()
    results["mean_duration"] = tick_data["duration"].mean()
    results["median_duration"] = tick_data["duration"].median()
    return results
