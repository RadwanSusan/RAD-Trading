import unittest
import pandas as pd
from RAD_trading.strategies import SMAStrategy, RSIStrategy
class TestStrategies(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame({
            'time': pd.date_range(start='2023-01-01', periods=100, freq='H'),
            'open': [100] * 100,
            'high': [105] * 100,
            'low': [95] * 100,
            'close': [100] * 100,
            'volume': [1000] * 100
        })
    def test_sma_strategy(self):
        strategy = SMAStrategy('EURUSD', 'H1', short_period=10, long_period=20)
        result = strategy.generate_signal(self.data)
        self.assertIn('signal', result.columns)
        self.assertIn(result['signal'].iloc[-1], ['buy', 'sell', 'hold'])
    def test_rsi_strategy(self):
        strategy = RSIStrategy('EURUSD', 'H1', rsi_period=14, overbought=70, oversold=30)
        result = strategy.generate_signal(self.data)
        self.assertIn('signal', result.columns)
        self.assertIn(result['signal'].iloc[-1], ['buy', 'sell', 'hold'])
if __name__ == '__main__':
    unittest.main()
