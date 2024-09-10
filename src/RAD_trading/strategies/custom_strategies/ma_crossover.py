# src/RAD_trading/strategies/custom_strategies/ma_crossover.py
from ..base_strategy import BaseStrategy
import pandas as pd
class MACrossoverStrategy(BaseStrategy):
    def __init__(self, symbol, timeframe, short_window=10, long_window=50):
        super().__init__(symbol, timeframe)
        self.short_window = short_window
        self.long_window = long_window

    def generate_signal(self, data):
        df = data.copy()

        df['short_ma'] = df['close'].rolling(window=self.short_window).mean()
        df['long_ma'] = df['close'].rolling(window=self.long_window).mean()
        df['signal'] = 'hold'
        df.loc[df['short_ma'] > df['long_ma'], 'signal'] = 'buy'
        df.loc[df['short_ma'] < df['long_ma'], 'signal'] = 'sell'

        # Ensure all signals are strings
        df['signal'] = df['signal'].astype(str)

        return df
    def get_parameters(self):
        return {
            'short_window': self.short_window,
            'long_window': self.long_window
        }
    def set_parameters(self, params):
        self.short_window = params.get('short_window', self.short_window)
        self.long_window = params.get('long_window', self.long_window)
