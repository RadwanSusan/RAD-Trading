# src/RAD_trading/backtesting/monte_carlo.py
import numpy as np
import pandas as pd
def monte_carlo_simulation(trades, initial_balance, num_simulations=1000):
    # Ensure trade returns are numerical
    trade_returns = pd.to_numeric(trades['profit'] / trades['entry_price'], errors='coerce')
    # Remove any NaN values that might have resulted from the conversion
    trade_returns = trade_returns.dropna()
    simulated_returns = np.random.choice(trade_returns, size=(num_simulations, len(trade_returns)), replace=True)
    simulated_equity_curves = initial_balance * (1 + simulated_returns).cumprod(axis=1)
    final_balances = simulated_equity_curves[:, -1]
    results = {
        'mean_final_balance': np.mean(final_balances),
        'median_final_balance': np.median(final_balances),
        '5th_percentile': np.percentile(final_balances, 5),
        '95th_percentile': np.percentile(final_balances, 95),
        'probability_of_profit': np.mean(final_balances > initial_balance),
        'max_drawdown': calculate_max_drawdown(pd.DataFrame(simulated_equity_curves.T)).mean()
    }
    return results, simulated_equity_curves
def calculate_max_drawdown(equity_curve):
    rolling_max = equity_curve.cummax()
    drawdown = (equity_curve - rolling_max) / rolling_max
    return drawdown.min()
