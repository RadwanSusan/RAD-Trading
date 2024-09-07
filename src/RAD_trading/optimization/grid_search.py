# src\RAD_trading\optimization\grid_search.py
import itertools
from ..backtester import Backtester
def grid_search(strategy_class, param_grid, data, initial_balance):
    results = []
    param_combinations = list(itertools.product(*param_grid.values()))
    for params in param_combinations:
        param_dict = dict(zip(param_grid.keys(), params))
        strategy = strategy_class(**param_dict)
        backtester = Backtester()
        backtester.set_starting_balance(initial_balance)
        backtester.set_historical_data(data)
        backtester.set_on_bar(strategy.on_bar)
        trades = backtester.run_backtest()
        final_balance = trades['balance'].iloc[-1] if not trades.empty else initial_balance
        sharpe_ratio = backtester.calculate_sharpe_ratio()
        results.append({
            'params': param_dict,
            'final_balance': final_balance,
            'sharpe_ratio': sharpe_ratio
        })
    return sorted(results, key=lambda x: x['sharpe_ratio'], reverse=True)
