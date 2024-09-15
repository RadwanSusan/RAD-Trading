# src\RAD_trading\market_impact\temporary_impact.py
import numpy as np


def calculate_temporary_impact(
    order_size, average_daily_volume, volatility, market_cap
):
    """
    Calculate temporary market impact using the Square Root Law.
    :param order_size: Size of the order in shares
    :param average_daily_volume: Average daily trading tick_volume of the stock
    :param volatility: Daily volatility of the stock
    :param market_cap: Market capitalization of the stock
    :return: Estimated temporary price impact as a percentage
    """
    # Parameters (these can be calibrated based on historical data)
    gamma = 0.5  # Square root law parameter
    beta = 0.1  # Scaling factor
    # Calculate relative order size
    relative_order_size = order_size / average_daily_volume
    # Calculate impact
    impact = (
        beta
        * volatility
        * np.power(relative_order_size, gamma)
        * np.power(market_cap / 1e9, -0.25)
    )
    return impact
