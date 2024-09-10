# src\RAD_trading\backtesting\backtesting.py
from ..data_providers import MT5DataProvider
from ..performance_analytics import calculate_sharpe_ratio, calculate_max_drawdown
from ..visualization import plot_equity_curve, plot_drawdown
from RAD_trading.logging_config import backtesting_logger
from ..performance_analytics.performance_metrics import calculate_metrics
import pandas as pd
import plotly.io as pio
class BacktestingEngine:
    def __init__(self):
        self.data_provider = MT5DataProvider()
        self.logger = backtesting_logger
    def run_backtest(self, strategy_class, symbol, timeframe, start_date, end_date, initial_balance, strategy_params):
        backtesting_logger.info(f"Running backtest for {symbol} from {start_date} to {end_date}")
        # Fetch historical data
        data = self.data_provider.get_historical_data(symbol, timeframe, start_date, end_date)
        backtesting_logger.info(f"Fetched {len(data)} data points")
        # Create strategy instance
        strategy = strategy_class(symbol, timeframe)
        strategy.set_parameters(strategy_params)
        # Run backtest
        results = self._run_backtest_logic(strategy, data, initial_balance)
        # Calculate performance metrics
        equity_curve = results['equity_curve']
        returns = equity_curve.pct_change().dropna()
        sharpe_ratio = calculate_sharpe_ratio(returns)
        max_drawdown = calculate_max_drawdown(equity_curve)
        # Generate plots
        equity_plot = plot_equity_curve(equity_curve)
        drawdown_plot = plot_drawdown(equity_curve)
        # Calculate performance metrics
        metrics = calculate_metrics(equity_curve, results['trades'])
        # Prepare results
        results = {
            'trades': results['trades'],
            'equity_curve': equity_curve,
            'metrics': metrics,
            'equity_plot': pio.to_json(equity_plot),
            'drawdown_plot': pio.to_json(drawdown_plot)
        }
        return results
    def _run_backtest_logic(self, strategy, data, initial_balance):
        balance = initial_balance
        position = None
        trades = []
        equity_curve = [initial_balance]

        for i in range(1, len(data)):
            try:
                signals = strategy.generate_signal(data.iloc[:i+1])
                current_signal = signals.iloc[-1]['signal']
                current_price = data.iloc[i]['close']

                self.logger.debug(f"Processing data point {i}: Signal={current_signal}, Price={current_price}")

                if position is None and current_signal in ['buy', 'sell']:
                    position = {
                        'type': current_signal,
                        'entry_price': float(current_price),
                        'entry_time': str(data.index[i])
                    }
                    self.logger.debug(f"Opening position: {position}")
                elif position is not None:
                    if (position['type'] == 'buy' and current_signal == 'sell') or \
                    (position['type'] == 'sell' and current_signal == 'buy'):
                        exit_price = float(current_price)
                        profit = (exit_price - position['entry_price']) if position['type'] == 'buy' else (position['entry_price'] - exit_price)
                        balance += profit
                        trade = {
                            'entry_time': position['entry_time'],
                            'exit_time': str(data.index[i]),
                            'type': position['type'],
                            'entry_price': position['entry_price'],
                            'exit_price': exit_price,
                            'profit': profit
                        }
                        trades.append(trade)
                        self.logger.debug(f"Closing position: {trade}")
                        position = None

                equity_curve.append(float(balance))
            except Exception as e:
                self.logger.error(f"Error at data point {i}: {str(e)}", exc_info=True)
                raise

        return {
            'trades': pd.DataFrame(trades),
            'equity_curve': pd.Series(equity_curve, index=data.index)
        }
