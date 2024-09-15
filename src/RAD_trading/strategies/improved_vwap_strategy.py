# src\RAD_trading\strategies\improved_vwap_strategy.py
from .base_strategy import BaseStrategy
import pandas as pd
import numpy as np


class ImprovedVWAPStrategy(BaseStrategy):
    def __init__(
        self,
        symbol,
        timeframe,
        short_vwap=20,
        long_vwap=50,
        rsi_period=14,
        rsi_overbought=70,
        rsi_oversold=30,
        atr_period=14,
        atr_multiplier=2,
        risk_per_trade=0.01,
    ):
        super().__init__(symbol, timeframe)
        self.short_vwap = short_vwap
        self.long_vwap = long_vwap
        self.rsi_period = rsi_period
        self.rsi_overbought = rsi_overbought
        self.rsi_oversold = rsi_oversold
        self.atr_period = atr_period
        self.atr_multiplier = atr_multiplier
        self.risk_per_trade = risk_per_trade

    def calculate_vwap(self, data, period):
        typical_price = (data["high"] + data["low"] + data["close"]) / 3
        vwap = (typical_price * data["tick_volume"]).rolling(
            window=period
        ).sum() / data["tick_volume"].rolling(window=period).sum()
        return vwap

    def calculate_rsi(self, data, period):
        delta = data["close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def calculate_atr(self, data, period):
        high_low = data["high"] - data["low"]
        high_close = np.abs(data["high"] - data["close"].shift())
        low_close = np.abs(data["low"] - data["close"].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        return true_range.rolling(period).mean()

    def generate_signal(self, data):
        df = data.copy()
        df["short_vwap"] = self.calculate_vwap(df, self.short_vwap)
        df["long_vwap"] = self.calculate_vwap(df, self.long_vwap)
        df["rsi"] = self.calculate_rsi(df, self.rsi_period)
        df["atr"] = self.calculate_atr(df, self.atr_period)

        # Volume analysis
        df["volume_ma"] = df["tick_volume"].rolling(window=20).mean()
        df["volume_ratio"] = df["tick_volume"] / df["volume_ma"]

        # Generate signals
        df["signal"] = "hold"

        # Buy conditions
        buy_condition = (
            (df["close"] > df["short_vwap"])
            & (df["short_vwap"] > df["long_vwap"])
            & (df["rsi"] < self.rsi_overbought)
            & (df["volume_ratio"] > 1.5)  # High volume
        )
        df.loc[buy_condition, "signal"] = "buy"

        # Sell conditions
        sell_condition = (
            (df["close"] < df["short_vwap"])
            & (df["short_vwap"] < df["long_vwap"])
            & (df["rsi"] > self.rsi_oversold)
            & (df["volume_ratio"] > 1.5)  # High volume
        )
        df.loc[sell_condition, "signal"] = "sell"

        # Calculate stop loss and take profit
        df["stop_loss"] = np.where(
            df["signal"] == "buy",
            df["close"] - self.atr_multiplier * df["atr"],
            df["close"] + self.atr_multiplier * df["atr"],
        )

        # Dynamic position sizing
        account_balance = 10000  # This should be dynamically updated in a real scenario
        df["position_size"] = (account_balance * self.risk_per_trade) / (
            self.atr_multiplier * df["atr"]
        )

        return df

    def on_bar(self, data, trades, orders):
        last_row = data.iloc[-1]
        current_price = last_row["close"]

        # Check for open positions
        open_positions = [trade for trade in trades if trade["state"] == "open"]

        # Close positions if stop loss or take profit is hit
        for position in open_positions:
            if position["type"] == "buy":
                if current_price <= position["stop_loss"]:
                    orders.close_trade(position)
            elif position["type"] == "sell":
                if current_price >= position["stop_loss"]:
                    orders.close_trade(position)

            # Update trailing stop loss
            new_stop_loss = (
                (current_price - self.atr_multiplier * last_row["atr"])
                if position["type"] == "buy"
                else (current_price + self.atr_multiplier * last_row["atr"])
            )
            if position["type"] == "buy" and new_stop_loss > position["stop_loss"]:
                orders.modify_sl(position, new_stop_loss)
            elif position["type"] == "sell" and new_stop_loss < position["stop_loss"]:
                orders.modify_sl(position, new_stop_loss)

        # Open new positions
        if not open_positions:
            if last_row["signal"] == "buy":
                orders.open_trade(
                    self.symbol, last_row["position_size"], "buy", last_row["stop_loss"]
                )
            elif last_row["signal"] == "sell":
                orders.open_trade(
                    self.symbol,
                    last_row["position_size"],
                    "sell",
                    last_row["stop_loss"],
                )

    def get_parameters(self):
        return {
            "short_vwap": self.short_vwap,
            "long_vwap": self.long_vwap,
            "rsi_period": self.rsi_period,
            "rsi_overbought": self.rsi_overbought,
            "rsi_oversold": self.rsi_oversold,
            "atr_period": self.atr_period,
            "atr_multiplier": self.atr_multiplier,
            "risk_per_trade": self.risk_per_trade,
        }

    def set_parameters(self, params):
        self.short_vwap = params.get("short_vwap", self.short_vwap)
        self.long_vwap = params.get("long_vwap", self.long_vwap)
        self.rsi_period = params.get("rsi_period", self.rsi_period)
        self.rsi_overbought = params.get("rsi_overbought", self.rsi_overbought)
        self.rsi_oversold = params.get("rsi_oversold", self.rsi_oversold)
        self.atr_period = params.get("atr_period", self.atr_period)
        self.atr_multiplier = params.get("atr_multiplier", self.atr_multiplier)
        self.risk_per_trade = params.get("risk_per_trade", self.risk_per_trade)
