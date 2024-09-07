# src\RAD_trading\execution\twap.py
from .base_executor import BaseExecutor
import numpy as np
class TWAPExecutor(BaseExecutor):
    def __init__(self, symbol, total_quantity, start_time, end_time, num_intervals):
        super().__init__(symbol, total_quantity, start_time, end_time)
        self.num_intervals = num_intervals
        self.interval_duration = (end_time - start_time) / num_intervals
        self.quantity_per_interval = total_quantity / num_intervals
    def get_next_order(self, current_time, market_data):
        if current_time < self.start_time or current_time >= self.end_time:
            return None
        interval_index = int((current_time - self.start_time) / self.interval_duration)
        quantity_to_execute = self.quantity_per_interval * (interval_index + 1) - self.executed_quantity
        return {
            'symbol': self.symbol,
            'quantity': min(quantity_to_execute, self.total_quantity - self.executed_quantity),
            'order_type': 'market'
        }
