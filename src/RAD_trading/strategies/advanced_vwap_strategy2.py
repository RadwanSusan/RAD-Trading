import pandas as pd
import numpy as np
from ta.trend import EMAIndicator
from ta.volatility import BollingerBands
from .base_strategy import BaseStrategy


class AdvancedVWAPStrategy(BaseStrategy):
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
        ema_period=200,
        volatility_threshold=1.5,
        risk_reward_ratio=2,
        bollinger_period=20,
        bollinger_std=2,
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
        self.ema_period = ema_period
        self.volatility_threshold = volatility_threshold
        self.risk_reward_ratio = risk_reward_ratio
        self.bollinger_period = bollinger_period
        self.bollinger_std = bollinger_std

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

    def calculate_fibonacci_levels(self, high, low):
        diff = high - low
        level_1 = high - 0.236 * diff
        level_2 = high - 0.382 * diff
        level_3 = high - 0.618 * diff
        return level_1, level_2, level_3

    def get_market_regime(self, data):
        bb = BollingerBands(
            data["close"], window=self.bollinger_period, window_dev=self.bollinger_std
        )
        data["bb_high"] = bb.bollinger_hband()
        data["bb_low"] = bb.bollinger_lband()
        data["bb_width"] = (data["bb_high"] - data["bb_low"]) / data["close"]
        return np.where(
            data["bb_width"] > data["bb_width"].rolling(window=100).mean(),
            "volatile",
            "range",
        )

    def generate_signal(self, data):
        df = data.copy()
        df["short_vwap"] = self.calculate_vwap(df, self.short_vwap)
        df["long_vwap"] = self.calculate_vwap(df, self.long_vwap)
        df["rsi"] = self.calculate_rsi(df, self.rsi_period)
        df["atr"] = self.calculate_atr(df, self.atr_period)
        df["ema"] = EMAIndicator(df["close"], window=self.ema_period).ema_indicator()

        # Volume analysis
        df["volume_ma"] = df["tick_volume"].rolling(window=20).mean()
        df["volume_ratio"] = df["tick_volume"] / df["volume_ma"]

        # Volatility filter
        df["volatility"] = df["close"].pct_change().rolling(window=20).std() * np.sqrt(
            252
        )

        # Market regime
        df["market_regime"] = self.get_market_regime(df)

        # Fibonacci levels
        df["fib_level_1"], df["fib_level_2"], df["fib_level_3"] = (
            self.calculate_fibonacci_levels(
                df["high"].rolling(window=20).max(), df["low"].rolling(window=20).min()
            )
        )

        # Generate signals
        df["signal"] = "hold"

        # Buy conditions
        buy_condition = (
            (df["close"] > df["short_vwap"])
            & (df["short_vwap"] > df["long_vwap"])
            & (df["rsi"] < self.rsi_overbought)
            & (df["volume_ratio"] > 1.5)  # High volume
            & (df["close"] > df["ema"])  # Trend filter
            & (df["volatility"] > self.volatility_threshold)  # Volatility filter
            & (df["close"] < df["fib_level_1"])  # Fibonacci entry
            & (df["market_regime"] == "volatile")  # Market regime filter
        )
        df.loc[buy_condition, "signal"] = "buy"

        # Sell conditions
        sell_condition = (
            (df["close"] < df["short_vwap"])
            & (df["short_vwap"] < df["long_vwap"])
            & (df["rsi"] > self.rsi_oversold)
            & (df["volume_ratio"] > 1.5)  # High volume
            & (df["close"] < df["ema"])  # Trend filter
            & (df["volatility"] > self.volatility_threshold)  # Volatility filter
            & (df["close"] > df["fib_level_3"])  # Fibonacci entry
            & (df["market_regime"] == "volatile")  # Market regime filter
        )
        df.loc[sell_condition, "signal"] = "sell"

        # Calculate stop loss and take profit
        df["stop_loss"] = np.where(
            df["signal"] == "buy",
            df["close"] - self.atr_multiplier * df["atr"],
            df["close"] + self.atr_multiplier * df["atr"],
        )
        df["take_profit"] = np.where(
            df["signal"] == "buy",
            df["close"] + self.risk_reward_ratio * (df["close"] - df["stop_loss"]),
            df["close"] - self.risk_reward_ratio * (df["stop_loss"] - df["close"]),
        )

        # Dynamic position sizing
        account_balance = 10000  # This should be dynamically updated in a real scenario
        df["position_size"] = (account_balance * self.risk_per_trade) / (
            df["close"] - df["stop_loss"]
        ).abs()

        return df

    def on_bar(self, data, trades, orders):
        last_row = data.iloc[-1]
        current_price = last_row["close"]

        # Check for open positions
        open_positions = [trade for trade in trades if trade["state"] == "open"]

        # Close positions if stop loss or take profit is hit
        for position in open_positions:
            if position["type"] == "buy":
                if (
                    current_price <= position["stop_loss"]
                    or current_price >= position["take_profit"]
                ):
                    orders.close_trade(position)
            elif position["type"] == "sell":
                if (
                    current_price >= position["stop_loss"]
                    or current_price <= position["take_profit"]
                ):
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
                    self.symbol,
                    last_row["position_size"],
                    "buy",
                    last_row["stop_loss"],
                    last_row["take_profit"],
                )
            elif last_row["signal"] == "sell":
                orders.open_trade(
                    self.symbol,
                    last_row["position_size"],
                    "sell",
                    last_row["stop_loss"],
                    last_row["take_profit"],
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
            "ema_period": self.ema_period,
            "volatility_threshold": self.volatility_threshold,
            "risk_reward_ratio": self.risk_reward_ratio,
            "bollinger_period": self.bollinger_period,
            "bollinger_std": self.bollinger_std,
        }

    def set_parameters(self, params):
        for key, value in params.items():
            setattr(self, key, value)
