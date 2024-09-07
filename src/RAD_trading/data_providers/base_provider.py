# src\RAD_trading\data_providers\base_provider.py
from abc import ABC, abstractmethod
class BaseDataProvider(ABC):
    @abstractmethod
    def get_historical_data(self, symbol, timeframe, start_date, end_date):
        pass
