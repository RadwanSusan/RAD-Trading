# src\RAD_trading\live_trading\live_trader.py
import time
from ..data_providers import MT5DataProvider
from ..mt5_trade_utils import send_market_order, close_all_positions, get_positions
class LiveTrader:
    def __init__(self, strategy, symbol, timeframe, update_interval=1):
        self.strategy = strategy
        self.symbol = symbol
        self.timeframe = timeframe
        self.update_interval = update_interval
        self.data_provider = MT5DataProvider()
        self.is_running = False
    def start(self):
        self.is_running = True
        while self.is_running:
            current_time = time.time()
            # Fetch latest data
            data = self.data_provider.get_historical_data(self.symbol, self.timeframe,
                                                          current_time - 1000 * self.timeframe, current_time)
            # Get current positions
            positions = get_positions()
            # Generate trading signals
            signals = self.strategy.generate_signal(data)
            # Execute trades based on signals
            self.execute_trades(signals, positions)
            time.sleep(self.update_interval)
    def stop(self):
        self.is_running = False
    def execute_trades(self, signals, positions):
        latest_signal = signals.iloc[-1]
        if latest_signal['signal'] == 'buy' and not any(p['type'] == 0 for p in positions):
            send_market_order(self.symbol, 0.01, 'buy')
        elif latest_signal['signal'] == 'sell' and not any(p['type'] == 1 for p in positions):
            send_market_order(self.symbol, 0.01, 'sell')
        elif latest_signal['signal'] == 'close':
            close_all_positions('all')
