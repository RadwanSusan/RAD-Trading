# src\RAD_trading\execution\base_executor.py
from abc import ABC, abstractmethod
class BaseExecutor(ABC):
    def __init__(self, symbol, total_quantity, start_time, end_time):
        self.symbol = symbol
        self.total_quantity = total_quantity
        self.start_time = start_time
        self.end_time = end_time
        self.executed_quantity = 0
    @abstractmethod
    def get_next_order(self, current_time, market_data):
        pass
    def update_executed_quantity(self, quantity):
        self.executed_quantity += quantity
    @property
    def is_complete(self):
        return self.executed_quantity >= self.total_quantity
