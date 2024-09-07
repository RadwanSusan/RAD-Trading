# src\RAD_trading\strategies\sma_strategy.py
from .base_strategy import BaseStrategy
class SMAStrategy(BaseStrategy):
    def __init__(self, symbol, timeframe, short_period=20, long_period=50):
        super().__init__(symbol, timeframe)
        self.short_period = short_period
        self.long_period = long_period
    def generate_signal(self, data):
        data['sma_short'] = data['close'].rolling(self.short_period).mean()
        data['sma_long'] = data['close'].rolling(self.long_period).mean()
        data['signal'] = 'hold'
        data.loc[data['sma_short'] > data['sma_long'], 'signal'] = 'buy'
        data.loc[data['sma_short'] < data['sma_long'], 'signal'] = 'sell'
        return data
    def on_bar(self, data, trades, orders):
        volume = 100000  # 1 lot
        open_trades = trades[trades['state'] == 'open']
        num_open_trades = open_trades.shape[0]
        if data['signal'] == 'buy' and not num_open_trades:
            orders.open_trade(self.symbol, volume, 'buy')
        elif data['signal'] == 'sell' and not num_open_trades:
            orders.open_trade(self.symbol, volume, 'sell')
        if num_open_trades:
            trade = open_trades.iloc[0]
            if (trade['order_type'] == 'buy' and data['signal'] == 'sell') or \
               (trade['order_type'] == 'sell' and data['signal'] == 'buy'):
                orders.close_trade(trade)
