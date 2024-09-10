# src/RAD_trading/backtesting/optimization.py
import itertools
from concurrent.futures import ProcessPoolExecutor, as_completed
from .backtesting import BacktestingEngine
def optimize_strategy(strategy_class, symbol, timeframe, start_date, end_date, initial_balance, param_ranges, optimization_metric='sharpe_ratio'):
    engine = BacktestingEngine()
    def run_backtest_with_params(params):
        results = engine.run_backtest(strategy_class, symbol, timeframe, start_date, end_date, initial_balance, params)
        return params, results['metrics'][optimization_metric]
    param_combinations = list(itertools.product(*param_ranges.values()))
    param_dicts = [dict(zip(param_ranges.keys(), combo)) for combo in param_combinations]
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(run_backtest_with_params, params) for params in param_dicts]
        results = [future.result() for future in as_completed(futures)]
    best_params, best_metric = max(results, key=lambda x: x[1])
    return best_params, best_metric
