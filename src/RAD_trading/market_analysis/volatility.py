# src\RAD_trading\market_analysis\volatility.py
import numpy as np
def calculate_historical_volatility(returns, window=252):
    """
    Calculate historical volatility.
    :param returns: Series of price returns
    :param window: Number of periods to consider for volatility calculation
    :return: Series of historical volatility
    """
    return returns.rolling(window=window).std() * np.sqrt(window)
