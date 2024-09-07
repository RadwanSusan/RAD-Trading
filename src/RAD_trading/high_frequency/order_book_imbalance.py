# src\RAD_trading\high_frequency\order_book_imbalance.py
def calculate_order_book_imbalance(order_book, levels=5):
    """
    Calculate order book imbalance.
    :param order_book: OrderBook object
    :param levels: Number of price levels to consider
    :return: Order book imbalance metric
    """
    bid_volume = sum(order_book.bids['volume'].head(levels))
    ask_volume = sum(order_book.asks['volume'].head(levels))
    total_volume = bid_volume + ask_volume
    if total_volume == 0:
        return 0
    return (bid_volume - ask_volume) / total_volume
