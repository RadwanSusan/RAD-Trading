# src\RAD_trading\risk_management\stop_loss.py
import pandas as pd
def atr_stop_loss(data, atr_period=14, multiplier=2):
    high_low = data['high'] - data['low']
    high_close = abs(data['high'] - data['close'].shift())
    low_close = abs(data['low'] - data['close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = ranges.max(axis=1)
    atr = true_range.rolling(window=atr_period).mean()
    buy_stop = data['low'] - (multiplier * atr)
    sell_stop = data['high'] + (multiplier * atr)
    return pd.DataFrame({'buy_stop': buy_stop, 'sell_stop': sell_stop})
def fixed_stop_loss(entry_price, stop_loss_pips, direction, pip_value):
    if direction.lower() == 'buy':
        return entry_price - (stop_loss_pips * pip_value)
    elif direction.lower() == 'sell':
        return entry_price + (stop_loss_pips * pip_value)
    else:
        raise ValueError("Direction must be 'buy' or 'sell'")
