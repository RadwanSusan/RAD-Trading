# src/RAD_trading/strategies/sma_strategy.py

from .base_strategy import BaseStrategy
import pandas as pd


class SMAStrategy(BaseStrategy):
    def __init__(self, symbol, timeframe, short_period=20, long_period=50):
        super().__init__(symbol, timeframe)
        self.short_period = None
        self.long_period = None
        self.set_parameters({"short_period": short_period, "long_period": long_period})

    def generate_signal(self, data):
        df = data.copy()
        df["sma_short"] = df["close"].rolling(window=int(self.short_period)).mean()
        df["sma_long"] = df["close"].rolling(window=int(self.long_period)).mean()

        df["signal"] = "hold"
        df.loc[df["sma_short"] > df["sma_long"], "signal"] = "buy"
        df.loc[df["sma_short"] < df["sma_long"], "signal"] = "sell"

        return df

    def get_parameters(self):
        return {"short_period": self.short_period, "long_period": self.long_period}

    def set_parameters(self, params):
        self.short_period = max(1, int(params.get("short_period", 20)))
        self.long_period = max(1, int(params.get("long_period", 50)))
