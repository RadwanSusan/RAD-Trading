# src/RAD_trading/strategies/vwap_strategy.py
from .base_strategy import BaseStrategy
import pandas as pd
import numpy as np


class VWAPStrategy(BaseStrategy):
    def __init__(self, symbol, timeframe, vwap_period=20, position_size=0.01):
        super().__init__(symbol, timeframe)
        self.vwap_period = vwap_period
        self.position_size = position_size

    def calculate_vwap(self, data):
        print(data)
        typical_price = (data["high"] + data["low"] + data["close"]) / 3
        vwap = (typical_price * data["tick_volume"]).rolling(
            window=self.vwap_period
        ).sum() / data["tick_volume"].rolling(window=self.vwap_period).sum()
        return vwap

    def generate_signal(self, data):
        df = data.copy()
        df["vwap"] = self.calculate_vwap(df)
        df["signal"] = np.where(df["close"] > df["vwap"], "buy", "sell")
        return df

    def get_parameters(self):
        return {"vwap_period": self.vwap_period, "position_size": self.position_size}

    def set_parameters(self, params):
        self.vwap_period = params.get("vwap_period", self.vwap_period)
        self.position_size = params.get("position_size", self.position_size)
