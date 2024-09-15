# src\RAD_trading\market_microstructure\order_book.py
import pandas as pd


class OrderBook:
    def __init__(self):
        self.bids = pd.DataFrame(columns=["price", "tick_volume"])
        self.asks = pd.DataFrame(columns=["price", "tick_volume"])

    def update(self, side, price, tick_volume):
        if side == "bid":
            self.bids = self.bids.append(
                {"price": price, "tick_volume": tick_volume}, ignore_index=True
            )
            self.bids = (
                self.bids.groupby("price")
                .sum()
                .reset_index()
                .sort_values("price", ascending=False)
            )
        elif side == "ask":
            self.asks = self.asks.append(
                {"price": price, "tick_volume": tick_volume}, ignore_index=True
            )
            self.asks = (
                self.asks.groupby("price").sum().reset_index().sort_values("price")
            )

    def get_top_of_book(self):
        if not self.bids.empty and not self.asks.empty:
            return {
                "bid_price": self.bids["price"].iloc[0],
                "bid_volume": self.bids["tick_volume"].iloc[0],
                "ask_price": self.asks["price"].iloc[0],
                "ask_volume": self.asks["tick_volume"].iloc[0],
                "spread": self.asks["price"].iloc[0] - self.bids["price"].iloc[0],
            }
        return None

    def get_depth(self, levels=5):
        return {
            "bids": self.bids.head(levels).to_dict("records"),
            "asks": self.asks.head(levels).to_dict("records"),
        }
