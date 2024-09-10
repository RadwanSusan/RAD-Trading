# src/RAD_trading/performance_analytics/performance_metrics.py
from datetime import datetime
import numpy as np
import pandas as pd

from RAD_trading.performance_analytics.metrics import calculate_max_drawdown, calculate_sharpe_ratio
def calculate_cagr(equity_curve):
    """Calculate Compound Annual Growth Rate"""
    start_date = equity_curve.index[0]
    end_date = equity_curve.index[-1]

    # Ensure we're working with datetime objects
    if not isinstance(start_date, (pd.Timestamp, datetime)):
        start_date = pd.to_datetime(start_date)
    if not isinstance(end_date, (pd.Timestamp, datetime)):
        end_date = pd.to_datetime(end_date)

    years = (end_date - start_date).days / 365.25

    # Handle the case where the duration is zero or very small
    if years < 1/365.25:  # Less than one day
        return 0.0  # or you could return None or some other indicator

    return (equity_curve.iloc[-1] / equity_curve.iloc[0]) ** (1/years) - 1
def calculate_sortino_ratio(returns, risk_free_rate=0.02, periods_per_year=252):
    """Calculate Sortino Ratio"""
    excess_returns = returns - risk_free_rate/periods_per_year
    downside_returns = excess_returns[excess_returns < 0]
    expected_return = excess_returns.mean() * periods_per_year
    downside_std = downside_returns.std() * np.sqrt(periods_per_year)
    return expected_return / downside_std if downside_std != 0 else np.nan
def calculate_calmar_ratio(returns, max_drawdown):
    """Calculate Calmar Ratio"""
    cagr = calculate_cagr(returns.cumsum())
    return cagr / abs(max_drawdown)
def calculate_profit_factor(trades):
    """Calculate Profit Factor"""
    gross_profit = trades[trades['profit'] > 0]['profit'].sum()
    gross_loss = abs(trades[trades['profit'] < 0]['profit'].sum())
    return gross_profit / gross_loss if gross_loss != 0 else np.inf
def calculate_expectancy(trades):
    """Calculate Expectancy"""
    avg_win = trades[trades['profit'] > 0]['profit'].mean()
    avg_loss = abs(trades[trades['profit'] < 0]['profit'].mean())
    win_rate = len(trades[trades['profit'] > 0]) / len(trades)
    return (win_rate * avg_win) - ((1 - win_rate) * avg_loss)
def calculate_metrics(equity_curve, trades):
    returns = equity_curve.pct_change().dropna()
    metrics = {
        'Total Return': float(equity_curve.iloc[-1] / equity_curve.iloc[0] - 1),
        'CAGR': float(calculate_cagr(equity_curve)),
        'Sharpe Ratio': float(calculate_sharpe_ratio(returns)),
        'Sortino Ratio': float(calculate_sortino_ratio(returns)),
        'Max Drawdown': float(calculate_max_drawdown(equity_curve)),
        'Calmar Ratio': float(calculate_calmar_ratio(returns, calculate_max_drawdown(equity_curve))),
        'Profit Factor': float(calculate_profit_factor(trades)),
        'Expectancy': float(calculate_expectancy(trades)),
        'Total Trades': int(len(trades)),
        'Win Rate': float(len(trades[trades['profit'] > 0]) / len(trades)) if len(trades) > 0 else 0,
        'Average Trade': float(trades['profit'].mean()) if len(trades) > 0 else 0,
        'Best Trade': float(trades['profit'].max()) if len(trades) > 0 else 0,
        'Worst Trade': float(trades['profit'].min()) if len(trades) > 0 else 0,
    }
    return pd.Series(metrics)
