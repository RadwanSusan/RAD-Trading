# src/RAD_trading/backtesting/backtesting_interface.py
from .backtesting import BacktestingEngine
from ..strategies.strategy_loader import load_strategies
from ..strategies.sma_strategy import SMAStrategy
from ..strategies.vwap_strategy import VWAPStrategy
from ..strategies.rsi_strategy import RSIStrategy
from ..strategies.base_strategy import BaseStrategy
from ..backtesting.optimization import optimize_strategy
from ..backtesting.monte_carlo import monte_carlo_simulation
from ..strategies.improved_vwap_strategy import ImprovedVWAPStrategy
from ..strategies.advanced_vwap_strategy2 import AdvancedVWAPStrategy
import pandas as pd
import concurrent.futures


class BacktestingInterface:
    def __init__(self):
        self.engine = BacktestingEngine()
        self.strategies = self.load_strategies()

    def list_strategies(self):
        return list(self.strategies.keys())

    def load_strategies(self):
        return {
            "SMAStrategy": SMAStrategy,
            "RSIStrategy": RSIStrategy,
            "VWAPStrategy": VWAPStrategy,
            "BaseStrategy": BaseStrategy,
            "ImprovedVWAPStrategy": ImprovedVWAPStrategy,
            "AdvancedVWAPStrategy": AdvancedVWAPStrategy,
        }

    def get_strategy_parameters(self, strategy_name):
        if strategy_name not in self.strategies:
            raise ValueError(f"Strategy '{strategy_name}' not found")
        strategy = self.strategies[strategy_name]("DUMMY", "DUMMY")
        return strategy.get_parameters()

    def run_backtest(
        self,
        strategy_name,
        symbol,
        timeframe,
        start_date,
        end_date,
        initial_balance,
        strategy_params,
    ):
        if strategy_name not in self.strategies:
            raise ValueError(f"Strategy '{strategy_name}' not found")

        strategy_class = self.strategies[strategy_name]

        results = self.engine.run_backtest(
            strategy_class,
            symbol,
            timeframe,
            start_date,
            end_date,
            initial_balance,
            strategy_params,
        )

        return results

    def compare_strategies(self, backtest_params, strategies_to_compare):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for strategy_name, strategy_params in strategies_to_compare.items():
                base_strategy_name = strategy_name.split("_")[
                    0
                ]  # Handle cases like 'SMAStrategy_2'
                if base_strategy_name not in self.strategies:
                    raise ValueError(f"Strategy '{base_strategy_name}' not found")
                future = executor.submit(
                    self.run_backtest,
                    base_strategy_name,
                    backtest_params["symbol"],
                    backtest_params["timeframe"],
                    backtest_params["start_date"],
                    backtest_params["end_date"],
                    backtest_params["initial_balance"],
                    strategy_params,
                )
                futures.append((strategy_name, future))
            results = {}
            for strategy_name, future in futures:
                results[strategy_name] = future.result()
        comparison = pd.DataFrame(
            {
                strategy: results[strategy]["metrics"]
                for strategy in strategies_to_compare
            }
        )
        return comparison, results

    def optimize_strategy(
        self,
        strategy_name,
        symbol,
        timeframe,
        start_date,
        end_date,
        initial_balance,
        param_ranges,
        optimization_metric="sharpe_ratio",
    ):
        if strategy_name not in self.strategies:
            raise ValueError(f"Strategy '{strategy_name}' not found")
        strategy_class = self.strategies[strategy_name]
        best_params, best_metric = optimize_strategy(
            self.engine,
            strategy_class,
            symbol,
            timeframe,
            start_date,
            end_date,
            initial_balance,
            param_ranges,
            optimization_metric,
        )
        return best_params, best_metric

    def run_monte_carlo(self, backtest_results, num_simulations=1000):
        trades = backtest_results["trades"]
        initial_balance = float(backtest_results["equity_curve"].iloc[0])
        mc_results, simulated_equity_curves = monte_carlo_simulation(
            trades, initial_balance, num_simulations
        )
        return mc_results, simulated_equity_curves
