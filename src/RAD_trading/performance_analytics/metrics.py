# src\RAD_trading\performance_analytics\metrics.py
import numpy as np
import pandas as pd
def calculate_sharpe_ratio(returns, risk_free_rate=0.02, periods_per_year=252):
    excess_returns = returns - risk_free_rate / periods_per_year
    return np.sqrt(periods_per_year) * excess_returns.mean() / excess_returns.std()
def calculate_max_drawdown(equity_curve):
    rolling_max = equity_curve.cummax()
    drawdown = (equity_curve - rolling_max) / rolling_max
    return drawdown.min()
def calculate_win_rate(trades):
    total_trades = len(trades)
    winning_trades = len(trades[trades['profit'] > 0])
    return winning_trades / total_trades if total_trades > 0 else 0
