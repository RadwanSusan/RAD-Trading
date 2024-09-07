# src\RAD_trading\utils\date_utils.py
import MetaTrader5 as mt5
from datetime import timedelta
def convert_to_mt5_timeframe(timeframe):
    timeframe_map = {
        '1m': mt5.TIMEFRAME_M1,
        '5m': mt5.TIMEFRAME_M5,
        '15m': mt5.TIMEFRAME_M15,
        '30m': mt5.TIMEFRAME_M30,
        '1h': mt5.TIMEFRAME_H1,
        '4h': mt5.TIMEFRAME_H4,
        '1d': mt5.TIMEFRAME_D1,
        '1w': mt5.TIMEFRAME_W1,
        '1mn': mt5.TIMEFRAME_MN1
    }
    return timeframe_map.get(timeframe, mt5.TIMEFRAME_D1)
def get_next_bar_time(current_time, timeframe):
    if timeframe == mt5.TIMEFRAME_M1:
        return current_time + timedelta(minutes=1)
    elif timeframe == mt5.TIMEFRAME_M5:
        return current_time + timedelta(minutes=5)
    # Add more cases for other timeframes
    else:
        raise ValueError("Unsupported timeframe")
