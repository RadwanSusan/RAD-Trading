# src\RAD_trading\utils.py
import pandas as pd
import numpy as np
def calculate_sharpe_ratio(returns, risk_free_rate=0.02, periods=252):
    """
    Calculate the Sharpe ratio of a returns series.
    :param returns: pandas Series of returns
    :param risk_free_rate: risk-free rate, default is 2%
    :param periods: number of periods in a year, default is 252 (trading days)
    :return: Sharpe ratio
    """
    excess_returns = returns - risk_free_rate / periods
    return np.sqrt(periods) * excess_returns.mean() / excess_returns.std()
def calculate_sortino_ratio(returns, risk_free_rate=0.02, periods=252):
    """
    Calculate the Sortino ratio of a returns series.
    :param returns: pandas Series of returns
    :param risk_free_rate: risk-free rate, default is 2%
    :param periods: number of periods in a year, default is 252 (trading days)
    :return: Sortino ratio
    """
    excess_returns = returns - risk_free_rate / periods
    downside_returns = excess_returns[excess_returns < 0]
    return np.sqrt(periods) * excess_returns.mean() / downside_returns.std()
def calculate_max_drawdown(equity_curve):
    """
    Calculate the maximum drawdown of an equity curve.
    :param equity_curve: pandas Series of equity values
    :return: Maximum drawdown as a percentage
    """
    peak = equity_curve.cummax()
    drawdown = (equity_curve - peak) / peak
    return drawdown.min()
def resample_ohlc(df, timeframe):
    """
    Resample OHLC data to a new timeframe.
    :param df: pandas DataFrame with 'open', 'high', 'low', 'close', and 'volume' columns
    :param timeframe: new timeframe as a string (e.g., '4H', '1D')
    :return: resampled DataFrame
    """
    resampled = df.resample(timeframe).agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    })
    return resampled.dropna()
