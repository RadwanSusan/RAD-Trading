# src\RAD_trading\tests\test_risk_management.py
import unittest
from RAD_trading.risk_management import calculate_position_size, atr_stop_loss
import pandas as pd
class TestRiskManagement(unittest.TestCase):
    def test_calculate_position_size(self):
        position_size = calculate_position_size(10000, 1, 1.2000, 1.1950)
        self.assertGreater(position_size, 0)
    def test_atr_stop_loss(self):
        data = pd.DataFrame({
            'high': [1.2010, 1.2020, 1.2030],
            'low': [1.1990, 1.1980, 1.1970],
            'close': [1.2000, 1.2010, 1.2020]
        })
        atr = 0.002
        buy_stop = atr_stop_loss(data.iloc[-1], atr, 'buy')
        sell_stop = atr_stop_loss(data.iloc[-1], atr, 'sell')
        self.assertLess(buy_stop, data['low'].iloc[-1])
        self.assertGreater(sell_stop, data['high'].iloc[-1])
if __name__ == '__main__':
    unittest.main()
