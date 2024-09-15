# src\RAD_trading\market_impact\permanent_impact.py
import numpy as np


def calculate_permanent_impact(order_size, average_daily_volume, volatility):
    """
    Calculate permanent market impact.
    :param order_size: Size of the order in shares
    :param average_daily_volume: Average daily trading tick_volume of the stock
    :param volatility: Daily volatility of the stock
    :return: Estimated permanent price impact as a percentage
    """
    # Parameters (these can be calibrated based on historical data)
    lambda_param = 1.0  # Price impact coefficient
    # Calculate relative order size
    relative_order_size = order_size / average_daily_volume
    # Calculate impact
    impact = (
        lambda_param
        * volatility
        * np.sign(order_size)
        * np.log(1 + relative_order_size)
    )
    return impact
