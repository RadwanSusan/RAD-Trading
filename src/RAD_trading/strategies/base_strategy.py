# src\RAD_trading\strategies\base_strategy.py
from abc import ABC, abstractmethod
class BaseStrategy(ABC):
    def __init__(self, symbol, timeframe):
        self.symbol = symbol
        self.timeframe = timeframe
    @abstractmethod
    def generate_signal(self, data):
        pass
    @abstractmethod
    def on_bar(self, data, trades, orders):
        pass
