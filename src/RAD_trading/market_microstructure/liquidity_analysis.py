# src\RAD_trading\market_microstructure\liquidity_analysis.py
import numpy as np


def analyze_liquidity(order_book, price_levels=5):
    """
    Analyze market liquidity based on the order book.
    :param order_book: OrderBook object
    :param price_levels: Number of price levels to consider
    :return: Dictionary of liquidity metrics
    """
    bids = order_book.bids.head(price_levels)
    asks = order_book.asks.head(price_levels)
    bid_ask_spread = asks["price"].iloc[0] - bids["price"].iloc[0]
    depth = bids["tick_volume"].sum() + asks["tick_volume"].sum()
    bid_slope = np.polyfit(bids["price"], bids["tick_volume"], 1)[0]
    ask_slope = np.polyfit(asks["price"], asks["tick_volume"], 1)[0]
    return {
        "bid_ask_spread": bid_ask_spread,
        "depth": depth,
        "bid_slope": bid_slope,
        "ask_slope": ask_slope,
    }
