# src\RAD_trading\backtester\walk_forward.py
import pandas as pd
from .backtester import Backtester
def walk_forward_optimization(strategy_class, data, initial_balance, param_grid, train_size, test_size):
    """
    Perform walk-forward optimization.
    :param strategy_class: Strategy class to optimize
    :param data: Historical data for backtesting
    :param initial_balance: Initial account balance
    :param param_grid: Dictionary of parameters to optimize
    :param train_size: Number of periods for training
    :param test_size: Number of periods for testing
    :return: DataFrame of optimized parameters and performance for each walk-forward period
    """
    results = []
    for i in range(0, len(data) - train_size - test_size, test_size):
        train_data = data.iloc[i:i+train_size]
        test_data = data.iloc[i+train_size:i+train_size+test_size]
        # Optimize parameters on training data
        best_params = grid_search(strategy_class, param_grid, train_data, initial_balance)[0]['params']
        # Test optimized strategy on test data
        strategy = strategy_class(**best_params)
        backtester = Backtester()
        backtester.set_starting_balance(initial_balance)
        backtester.set_historical_data(test_data)
        backtester.set_on_bar(strategy.on_bar)
        trades = backtester.run_backtest()
        results.append({
            'period_start': test_data.index[0],
            'period_end': test_data.index[-1],
            'params': best_params,
            'sharpe_ratio': backtester.calculate_sharpe_ratio(),
            'total_return': (trades['balance'].iloc[-1] / initial_balance - 1) if not trades.empty else 0
        })
    return pd.DataFrame(results)
