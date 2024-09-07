# src\RAD_trading\market_analysis\correlation.py
import pandas as pd
def calculate_correlation_matrix(price_data):
    """
    Calculate correlation matrix for multiple symbols.
    :param price_data: DataFrame with columns as symbols and rows as price data
    :return: Correlation matrix
    """
    return price_data.corr()
