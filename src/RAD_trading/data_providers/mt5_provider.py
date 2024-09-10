# src\RAD_trading\data_providers\mt5_provider.py
import MetaTrader5 as mt5
import pandas as pd
class MT5DataProvider:
    def __init__(self):
        if not mt5.initialize():
            print("initialize() failed")
            mt5.shutdown()
    def get_historical_data(self, symbol, timeframe, start_date, end_date):
        print(f"Fetching historical data for {symbol} from {start_date} to {end_date} and {timeframe}")
        timeframe_map = {
            'M1': mt5.TIMEFRAME_M1,
            'M5': mt5.TIMEFRAME_M5,
            'M15': mt5.TIMEFRAME_M15,
            'M30': mt5.TIMEFRAME_M30,
            'H1': mt5.TIMEFRAME_H1,
            'H4': mt5.TIMEFRAME_H4,
            'D1': mt5.TIMEFRAME_D1,
            'W1': mt5.TIMEFRAME_W1,
            'MN1': mt5.TIMEFRAME_MN1
        }
        mt5_timeframe = timeframe_map.get(timeframe)
        if mt5_timeframe is None:
            raise ValueError(f"Invalid timeframe: {timeframe}")
        start_date = pd.to_datetime(start_date).to_pydatetime()
        end_date = pd.to_datetime(end_date).to_pydatetime()
        if start_date >= end_date:
            raise ValueError("start_date must be earlier than end_date")
        rates = mt5.copy_rates_range(symbol, mt5_timeframe, start_date, end_date)
        if rates is None or len(rates) == 0:
            print("Failed to retrieve rates or no data available")
            return pd.DataFrame()
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        return df
    def __del__(self):
        mt5.shutdown()
