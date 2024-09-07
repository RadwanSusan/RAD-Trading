# src\RAD_trading\reporting\performance_report.py
import pandas as pd
from ..performance_analytics.metrics import calculate_sharpe_ratio, calculate_max_drawdown, calculate_win_rate
def generate_performance_report(trades, equity_curve):
    total_trades = len(trades)
    profitable_trades = len(trades[trades['profit'] > 0])
    loss_making_trades = len(trades[trades['profit'] < 0])
    total_profit = trades['profit'].sum()
    average_profit = trades['profit'].mean()
    largest_profit = trades['profit'].max()
    largest_loss = trades['profit'].min()
    win_rate = calculate_win_rate(trades)
    sharpe_ratio = calculate_sharpe_ratio(equity_curve.pct_change())
    max_drawdown = calculate_max_drawdown(equity_curve)
    report = pd.DataFrame({
        'Metric': ['Total Trades', 'Profitable Trades', 'Loss-making Trades', 'Total Profit',
                   'Average Profit', 'Largest Profit', 'Largest Loss', 'Win Rate',
                   'Sharpe Ratio', 'Max Drawdown'],
        'Value': [total_trades, profitable_trades, loss_making_trades, total_profit,
                  average_profit, largest_profit, largest_loss, win_rate,
                  sharpe_ratio, max_drawdown]
    })
    return report
