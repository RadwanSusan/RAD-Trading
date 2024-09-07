# src\RAD_trading\machine_learning\feature_engineering.py
import pandas as pd
import numpy as np
def create_features(data):
    """
    Create features for machine learning models.
    :param data: DataFrame with OHLCV data
    :return: DataFrame with engineered features
    """
    df = data.copy()
    # Technical indicators
    df['SMA_10'] = df['close'].rolling(window=10).mean()
    df['SMA_30'] = df['close'].rolling(window=30).mean()
    df['RSI'] = calculate_rsi(df['close'])
    df['MACD'], df['MACD_signal'], _ = calculate_macd(df['close'])
    # Price momentum
    df['returns'] = df['close'].pct_change()
    df['lag_1_return'] = df['returns'].shift(1)
    df['lag_2_return'] = df['returns'].shift(2)
    # Volatility
    df['volatility'] = df['returns'].rolling(window=20).std()
    # Target variable (next day return)
    df['target'] = df['returns'].shift(-1)
    return df.dropna()
def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))
def calculate_macd(prices, fast_period=12, slow_period=26, signal_period=9):
    fast_ema = prices.ewm(span=fast_period, adjust=False).mean()
    slow_ema = prices.ewm(span=slow_period, adjust=False).mean()
    macd = fast_ema - slow_ema
    signal = macd.ewm(span=signal_period, adjust=False).mean()
    histogram = macd - signal
    return macd, signal, histogram
