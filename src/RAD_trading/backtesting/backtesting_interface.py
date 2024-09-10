# src/RAD_trading/backtesting/backtesting_interface.py
from .backtesting import BacktestingEngine
from ..strategies.strategy_loader import load_strategies
from .optimization import optimize_strategy
from .monte_carlo import monte_carlo_simulation
import pandas as pd
class BacktestingInterface:
    def __init__(self):
        self.engine = BacktestingEngine()
        self.strategies = load_strategies()
    def list_strategies(self):
        return list(self.strategies.keys())
    def get_strategy_parameters(self, strategy_name):
        if strategy_name not in self.strategies:
            raise ValueError(f"Strategy '{strategy_name}' not found")
        strategy = self.strategies[strategy_name]('DUMMY', 'DUMMY')
        return strategy.get_parameters()
    def run_backtest(self, strategy_name, symbol, timeframe, start_date, end_date, initial_balance, strategy_params):
        if strategy_name not in self.strategies:
            raise ValueError(f"Strategy '{strategy_name}' not found")
        strategy_class = self.strategies[strategy_name]
        results = self.engine.run_backtest(strategy_class, symbol, timeframe, start_date, end_date, initial_balance, strategy_params)
        return results
    def compare_strategies(self, backtest_params, strategies_to_compare):
        results = {}
        for strategy_name, strategy_params in strategies_to_compare.items():
            results[strategy_name] = self.run_backtest(
                strategy_name,
                backtest_params['symbol'],
                backtest_params['timeframe'],
                backtest_params['start_date'],
                backtest_params['end_date'],
                backtest_params['initial_balance'],
                strategy_params
            )
        comparison = pd.DataFrame({
            strategy: {
                'Sharpe Ratio': results[strategy]['sharpe_ratio'],
                'Max Drawdown': results[strategy]['max_drawdown'],
                'Final Balance': results[strategy]['equity_curve'].iloc[-1]
            } for strategy in strategies_to_compare
        })
        return comparison, results
    def optimize_strategy(self, strategy_name, symbol, timeframe, start_date, end_date, initial_balance, param_ranges, optimization_metric='sharpe_ratio'):
        if strategy_name not in self.strategies:
            raise ValueError(f"Strategy '{strategy_name}' not found")
        strategy_class = self.strategies[strategy_name]
        best_params, best_metric = optimize_strategy(
            strategy_class, symbol, timeframe, start_date, end_date,
            initial_balance, param_ranges, optimization_metric
        )
        return best_params, best_metric
    def run_monte_carlo(self, backtest_results, num_simulations=1000):
        initial_balance = float(backtest_results['equity_curve'].iloc[0])
        trades = backtest_results['trades']
        # Ensure trade data are numerical
        trades['entry_price'] = pd.to_numeric(trades['entry_price'], errors='coerce')
        trades['exit_price'] = pd.to_numeric(trades['exit_price'], errors='coerce')
        trades['profit'] = pd.to_numeric(trades['profit'], errors='coerce')
        mc_results, simulated_equity_curves = monte_carlo_simulation(trades, initial_balance, num_simulations)
        return mc_results, simulated_equity_curves
