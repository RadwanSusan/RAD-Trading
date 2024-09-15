# # src\RAD_trading\data_providers\mt5_provider.py
# import MetaTrader5 as mt5
# import pandas as pd
# class MT5DataProvider:
#     def __init__(self):
#         if not mt5.initialize():
#             print("initialize() failed")
#             mt5.shutdown()
#     def get_historical_data(self, symbol, timeframe, start_date, end_date):
#         print(f"Fetching historical data for {symbol} from {start_date} to {end_date} and {timeframe}")
#         timeframe_map = {
#             'M1': mt5.TIMEFRAME_M1,
#             'M5': mt5.TIMEFRAME_M5,
#             'M15': mt5.TIMEFRAME_M15,
#             'M30': mt5.TIMEFRAME_M30,
#             'H1': mt5.TIMEFRAME_H1,
#             'H4': mt5.TIMEFRAME_H4,
#             'D1': mt5.TIMEFRAME_D1,
#             'W1': mt5.TIMEFRAME_W1,
#             'MN1': mt5.TIMEFRAME_MN1
#         }
#         mt5_timeframe = timeframe_map.get(timeframe)
#         if mt5_timeframe is None:
#             raise ValueError(f"Invalid timeframe: {timeframe}")
#         start_date = pd.to_datetime(start_date).to_pydatetime()
#         end_date = pd.to_datetime(end_date).to_pydatetime()
#         if start_date >= end_date:
#             raise ValueError("start_date must be earlier than end_date")
#         rates = mt5.copy_rates_range(symbol, mt5_timeframe, start_date, end_date)
#         if rates is None or len(rates) == 0:
#             print("Failed to retrieve rates or no data available")
#             return pd.DataFrame()
#         df = pd.DataFrame(rates)
#         df['time'] = pd.to_datetime(df['time'], unit='s')
#         return df
#     def __del__(self):
#         mt5.shutdown()
# src\RAD_trading\data_providers\mt5_provider.py
import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import concurrent.futures
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MT5DataProvider:
    def __init__(self, max_workers=4):
        if not mt5.initialize():
            logger.error("MetaTrader5 initialization failed")
            mt5.shutdown()
        self.max_workers = max_workers
        self.timeframe_map = {
            "M1": mt5.TIMEFRAME_M1,
            "M5": mt5.TIMEFRAME_M5,
            "M15": mt5.TIMEFRAME_M15,
            "M30": mt5.TIMEFRAME_M30,
            "H1": mt5.TIMEFRAME_H1,
            "H4": mt5.TIMEFRAME_H4,
            "D1": mt5.TIMEFRAME_D1,
            "W1": mt5.TIMEFRAME_W1,
            "MN1": mt5.TIMEFRAME_MN1,
        }

    def get_historical_data(self, symbol, timeframe, start_date, end_date):
        logger.info(
            f"Fetching historical data for {symbol} from {start_date} to {end_date} and {timeframe}"
        )

        mt5_timeframe = self.timeframe_map.get(timeframe)
        if mt5_timeframe is None:
            raise ValueError(f"Invalid timeframe: {timeframe}")

        start_date = pd.to_datetime(start_date).to_pydatetime()
        end_date = pd.to_datetime(end_date).to_pydatetime()
        if start_date >= end_date:
            raise ValueError("start_date must be earlier than end_date")

        # Fetch data in parallel
        chunk_size = timedelta(days=7)
        date_ranges = self._get_date_ranges(start_date, end_date, chunk_size)

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers
        ) as executor:
            future_to_chunk = {
                executor.submit(
                    self._fetch_data_chunk, symbol, mt5_timeframe, start, end
                ): (start, end)
                for start, end in date_ranges
            }
            data_chunks = []
            for future in concurrent.futures.as_completed(future_to_chunk):
                chunk = future.result()
                if chunk is not None:
                    data_chunks.append(chunk)

        if not data_chunks:
            logger.warning("Failed to retrieve rates or no data available")
            return pd.DataFrame()

        df = pd.concat(data_chunks, ignore_index=True)
        df["time"] = pd.to_datetime(df["time"], unit="s")
        df = df.sort_values("time").drop_duplicates()

        return df

    def _fetch_data_chunk(self, symbol, mt5_timeframe, start_date, end_date):
        try:
            rates = mt5.copy_rates_range(symbol, mt5_timeframe, start_date, end_date)
            if rates is not None and len(rates) > 0:
                return pd.DataFrame(rates)
        except Exception as e:
            logger.error(
                f"Error fetching data for {symbol} from {start_date} to {end_date}: {e}"
            )
        return None

    def _get_date_ranges(self, start_date, end_date, chunk_size):
        date_ranges = []
        current_start = start_date
        while current_start < end_date:
            current_end = min(current_start + chunk_size, end_date)
            date_ranges.append((current_start, current_end))
            current_start = current_end
        return date_ranges

    def __del__(self):
        mt5.shutdown()
