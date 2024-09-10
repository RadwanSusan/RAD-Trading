# src\RAD_trading\backtesting\backtesting.py
from RAD_trading.backtester import Backtester
from RAD_trading.strategies import SMAStrategy
from RAD_trading.data_providers import MT5DataProvider
from RAD_trading.performance_analytics import calculate_sharpe_ratio, calculate_max_drawdown
from RAD_trading.visualization import plot_equity_curve, plot_drawdown
import pandas as pd
import plotly.io as pio
class BacktestingEngine:
    def __init__(self):
        self.data_provider = MT5DataProvider()
    def run_backtest(self, symbol, timeframe, start_date, end_date, initial_balance, strategy_params):
        # Fetch historical data
        data = self.data_provider.get_historical_data(symbol, timeframe, start_date, end_date)
        # Create strategy instance
        strategy = SMAStrategy(symbol, timeframe,
                               short_period=strategy_params['short_period'],
                               long_period=strategy_params['long_period'])
        # Set up and run backtester
        backtester = Backtester()
        backtester.set_starting_balance(initial_balance)
        backtester.set_historical_data(data)
        backtester.set_on_bar(strategy.on_bar)
        trades = backtester.run_backtest()
        # Calculate performance metrics
        equity_curve = trades['balance']
        returns = equity_curve.pct_change().dropna()
        sharpe_ratio = calculate_sharpe_ratio(returns)
        max_drawdown = calculate_max_drawdown(equity_curve)
        # Generate plots
        equity_plot = plot_equity_curve(equity_curve)
        drawdown_plot = plot_drawdown(equity_curve)
        # Prepare results
        results = {
            'trades': trades,
            'equity_curve': equity_curve,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'equity_plot': pio.to_json(equity_plot),
            'drawdown_plot': pio.to_json(drawdown_plot)
        }
        return results
