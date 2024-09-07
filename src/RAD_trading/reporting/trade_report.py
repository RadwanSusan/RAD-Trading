# src\RAD_trading\reporting\trade_report.py
import pandas as pd
def generate_trade_report(trades):
    report = trades[['symbol', 'order_type', 'volume', 'open_time', 'open_price',
                     'close_time', 'close_price', 'profit', 'sl', 'tp']]
    report['duration'] = report['close_time'] - report['open_time']
    report['pips'] = (report['close_price'] - report['open_price']) * (1 if report['order_type'] == 'buy' else -1) * 10000
    return report.sort_values('open_time', ascending=False)
