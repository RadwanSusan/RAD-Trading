# tests/test_backtesting.py
import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from RAD_trading.backtesting.backtesting import BacktestingEngine
from RAD_trading.backtesting.backtesting_interface import BacktestingInterface
from RAD_trading.strategies.sma_strategy import SMAStrategy


class MockDataProvider:
    def get_historical_data(self, symbol, timeframe, start_date, end_date):
        dates = pd.date_range(start=start_date, end=end_date, freq="D")
        data = pd.DataFrame(
            {
                "open": np.random.randn(len(dates)) + 100,
                "high": np.random.randn(len(dates)) + 101,
                "low": np.random.randn(len(dates)) + 99,
                "close": np.random.randn(len(dates)) + 100,
                "tick_volume": np.random.randint(1000, 10000, len(dates)),
            },
            index=dates,
        )
        return data


class TestBacktesting(unittest.TestCase):
    def setUp(self):
        self.engine = BacktestingEngine()
        self.engine.data_provider = MockDataProvider()
        self.interface = BacktestingInterface()
        self.interface.engine = self.engine

    def test_run_backtest(self):
        results = self.engine.run_backtest(
            SMAStrategy,
            "EURUSD",
            "D1",
            datetime(2020, 1, 1),
            datetime(2021, 1, 1),
            10000,
            {"short_period": 10, "long_period": 20},
        )
        self.assertIn("trades", results)
        self.assertIn("equity_curve", results)
        self.assertIn("metrics", results)
        self.assertIn("equity_plot", results)
        self.assertIn("drawdown_plot", results)

    def test_compare_strategies(self):
        comparison, results = self.interface.compare_strategies(
            {
                "symbol": "EURUSD",
                "timeframe": "D1",
                "start_date": datetime(2020, 1, 1),
                "end_date": datetime(2021, 1, 1),
                "initial_balance": 10000,
            },
            {
                "SMAStrategy_1": {"short_period": 10, "long_period": 20},
                "SMAStrategy_2": {"short_period": 20, "long_period": 50},
            },
        )
        self.assertEqual(len(comparison.columns), 2)
        self.assertEqual(len(results), 2)

    def test_optimize_strategy(self):
        best_params, best_metric = self.interface.optimize_strategy(
            "SMAStrategy",
            "EURUSD",
            "D1",
            datetime(2020, 1, 1),
            datetime(2021, 1, 1),
            10000,
            {"short_period": (5, 50), "long_period": (10, 100)},
            "sharpe_ratio",
        )
        self.assertIn("short_period", best_params)
        self.assertIn("long_period", best_params)
        self.assertIsInstance(best_metric, float)

    def test_monte_carlo(self):
        backtest_results = self.engine.run_backtest(
            SMAStrategy,
            "EURUSD",
            "D1",
            datetime(2020, 1, 1),
            datetime(2021, 1, 1),
            10000,
            {"short_period": 10, "long_period": 20},
        )
        mc_results, simulated_equity_curves = self.interface.run_monte_carlo(
            backtest_results, num_simulations=100
        )
        self.assertIn("mean_final_balance", mc_results)
        self.assertIn("median_final_balance", mc_results)
        self.assertIn("5th_percentile", mc_results)
        self.assertIn("95th_percentile", mc_results)
        self.assertIn("probability_of_profit", mc_results)
        self.assertIn("max_drawdown", mc_results)
        self.assertEqual(simulated_equity_curves.shape[0], 100)

    def test_performance(self):
        import time

        start_time = time.time()
        self.test_run_backtest()
        backtest_time = time.time() - start_time
        start_time = time.time()
        self.test_compare_strategies()
        compare_time = time.time() - start_time
        start_time = time.time()
        self.test_optimize_strategy()
        optimize_time = time.time() - start_time
        start_time = time.time()
        self.test_monte_carlo()
        monte_carlo_time = time.time() - start_time
        print(f"Backtest time: {backtest_time:.2f}s")
        print(f"Compare strategies time: {compare_time:.2f}s")
        print(f"Optimize strategy time: {optimize_time:.2f}s")
        print(f"Monte Carlo simulation time: {monte_carlo_time:.2f}s")


if __name__ == "__main__":
    unittest.main()
