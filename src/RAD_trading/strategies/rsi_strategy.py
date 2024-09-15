# src\RAD_trading\strategies\rsi_strategy.py
from .base_strategy import BaseStrategy
import pandas as pd
import numpy as np


class RSIStrategy(BaseStrategy):
    def __init__(self, symbol, timeframe, rsi_period=14, overbought=70, oversold=30):
        super().__init__(symbol, timeframe)
        self.rsi_period = rsi_period
        self.overbought = overbought
        self.oversold = oversold

    def calculate_rsi(self, data, period):
        delta = data["close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def generate_signal(self, data):
        data["rsi"] = self.calculate_rsi(data, self.rsi_period)
        data["signal"] = np.where(
            data["rsi"] > self.overbought,
            "sell",
            np.where(data["rsi"] < self.oversold, "buy", "hold"),
        )
        return data

    def on_bar(self, data, trades, orders):
        last_row = data.iloc[-1]
        if last_row["signal"] == "buy":
            orders.open_trade(self.symbol, 0.01, "buy")
        elif last_row["signal"] == "sell":
            orders.open_trade(self.symbol, 0.01, "sell")
