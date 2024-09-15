# src/RAD_trading/performance_analytics/performance_metrics.py
import pandas as pd
import numpy as np


def calculate_metrics(equity_curve, trades):
    """Calculate various performance metrics."""
    returns = equity_curve.pct_change().dropna()
    total_return = (equity_curve.iloc[-1] / equity_curve.iloc[0]) - 1
    sharpe_ratio = calculate_sharpe_ratio(returns)
    max_drawdown = calculate_max_drawdown(equity_curve)
    win_rate = calculate_win_rate(trades)
    return pd.Series(
        {
            "Total Return": total_return,
            "Sharpe Ratio": sharpe_ratio,
            "Max Drawdown": max_drawdown,
            "Win Rate": win_rate,
        }
    )


def calculate_sharpe_ratio(returns, risk_free_rate=0.02, periods=252):
    excess_returns = returns - risk_free_rate / periods
    if excess_returns.std() == 0:
        return 0  # Return 0 if there's no variation in returns
    return np.sqrt(periods) * excess_returns.mean() / excess_returns.std()


def calculate_max_drawdown(equity_curve):
    peak = equity_curve.cummax()
    drawdown = (equity_curve - peak) / peak
    return drawdown.min()


def calculate_win_rate(trades):
    if len(trades) == 0:
        return 0
    winning_trades = trades[trades["profit"] > 0]
    return len(winning_trades) / len(trades)
