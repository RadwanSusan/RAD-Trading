# src/RAD_trading/strategies/custom_strategies/rsi_strategy.py
from ..base_strategy import BaseStrategy
import pandas as pd
class RSIStrategy(BaseStrategy):
    def __init__(self, symbol, timeframe, rsi_period=14, overbought=70, oversold=30):
        super().__init__(symbol, timeframe)
        self.rsi_period = rsi_period
        self.overbought = overbought
        self.oversold = oversold
    def generate_signal(self, data):
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.rsi_period).mean()
        rs = gain / loss
        data['rsi'] = 100 - (100 / (1 + rs))
        data['signal'] = 'hold'
        data.loc[data['rsi'] > self.overbought, 'signal'] = 'sell'
        data.loc[data['rsi'] < self.oversold, 'signal'] = 'buy'
        return data
    def get_parameters(self):
        return {
            'rsi_period': self.rsi_period,
            'overbought': self.overbought,
            'oversold': self.oversold
        }
    def set_parameters(self, params):
        self.rsi_period = params.get('rsi_period', self.rsi_period)
        self.overbought = params.get('overbought', self.overbought)
        self.oversold = params.get('oversold', self.oversold)
