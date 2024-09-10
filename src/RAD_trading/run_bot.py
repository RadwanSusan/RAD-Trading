# src\RAD_trading\run_bot.py
import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import time
from RAD_trading import (
    send_market_order, close_all_positions, get_positions
)
from RAD_trading.logging_config import trading_logger
from RAD_trading.risk_management import calculate_position_size, atr_stop_loss
from RAD_trading.notifications import email_notifier

class TradingBot:
    def __init__(self, symbols, timeframe, strategy_class, risk_percentage=1, max_open_trades=3):
        self.symbols = symbols
        self.timeframe = timeframe
        self.strategies = {symbol: strategy_class(symbol, timeframe) for symbol in symbols}
        self.risk_percentage = risk_percentage
        self.max_open_trades = max_open_trades
        self.is_running = False
        self.logger = trading_logger
    def fetch_data(self):
        data = {}
        for symbol in self.symbols:
            rates = mt5.copy_rates_from_pos(symbol, self.timeframe, 0, 1000)
            df = pd.DataFrame(rates)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            data[symbol] = df
        return data
    def calculate_position_size(self, entry_price, stop_loss):
        account_info = mt5.account_info()
        if account_info is None:
            raise ValueError("Failed to get account info")
        balance = account_info.balance
        position_size = calculate_position_size(balance, self.risk_percentage, entry_price, stop_loss)
        return position_size

    def calculate_atr(self, data, period=14):
        high_low = data['high'] - data['low']
        high_close = np.abs(data['high'] - data['close'].shift())
        low_close = np.abs(data['low'] - data['close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        return true_range.rolling(period).mean().iloc[-1]

    def execute_trades(self, signals):
        positions = get_positions()
        for symbol, signal in signals.items():
            if len(positions) >= self.max_open_trades:
                self.logger.info(f"Maximum number of open trades ({self.max_open_trades}) reached. Skipping trade execution for {symbol}.")
                continue

            if signal in ['buy', 'sell']:
                data = self.fetch_data()[symbol]
                atr = self.calculate_atr(data)
                entry_price = mt5.symbol_info_tick(symbol).ask if signal == 'buy' else mt5.symbol_info_tick(symbol).bid
                stop_loss = atr_stop_loss(data.iloc[-1], atr, signal)
                volume = self.calculate_position_size(symbol, entry_price, stop_loss)

                self.logger.info(f"Opening {signal} position for {symbol} with volume {volume}")
                send_market_order(symbol, volume, signal, sl=stop_loss)

            elif signal == 'close':
                self.logger.info(f"Closing all positions for {symbol}")
                close_all_positions(symbol=symbol)

    def update_trades(self):
        positions = get_positions()
        for trade in self.trades:
            if trade['exit_price'] is None:
                matching_position = next((p for p in positions if p.symbol == self.symbol), None)
                if matching_position is None:
                    # Trade has been closed
                    trade['exit_price'] = mt5.symbol_info_tick(self.symbol).bid
                    trade['profit'] = matching_position.profit

    def get_performance(self):
        if self.initial_balance is None:
            account_info = mt5.account_info()
            self.initial_balance = account_info.balance

        account_info = mt5.account_info()
        self.current_balance = account_info.balance

        return {
            "initial_balance": self.initial_balance,
            "current_balance": self.current_balance,
            "profit_loss": self.current_balance - self.initial_balance,
            "trade_count": len(self.trades),
            "win_rate": self.calculate_win_rate(),
        }

    def calculate_win_rate(self):
        if not self.trades:
            return 0
        winning_trades = sum(1 for trade in self.trades if trade['profit'] is not None and trade['profit'] > 0)
        return winning_trades / len(self.trades)

    def run(self):
        self.is_running = True
        self.logger.info(f"Starting trading bot for symbols: {', '.join(self.symbols)}")
        while self.is_running:
            try:
                data = self.fetch_data()
                signals = {symbol: self.strategies[symbol].generate_signal(data[symbol]).iloc[-1]['signal'] for symbol in self.symbols}
                self.execute_trades(signals)
                self.update_trades()
                time.sleep(60)  # Sleep for 1 minute
            except Exception as e:
                self.logger.error(f"An error occurred: {e}", exc_info=True)
                self.is_running = False
        self.logger.info("Trading bot stopped")


    def stop(self):
        self.is_running = False
