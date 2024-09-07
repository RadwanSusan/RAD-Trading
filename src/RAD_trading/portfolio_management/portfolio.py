# src\RAD_trading\portfolio_management\portfolio.py
import pandas as pd
class Portfolio:
    def __init__(self):
        self.positions = {}
        self.cash = 0
    def add_position(self, symbol, quantity, price):
        if symbol in self.positions:
            self.positions[symbol]['quantity'] += quantity
            self.positions[symbol]['average_price'] = (self.positions[symbol]['average_price'] * self.positions[symbol]['quantity'] + price * quantity) / (self.positions[symbol]['quantity'] + quantity)
        else:
            self.positions[symbol] = {'quantity': quantity, 'average_price': price}
    def remove_position(self, symbol, quantity, price):
        if symbol in self.positions:
            if quantity >= self.positions[symbol]['quantity']:
                del self.positions[symbol]
            else:
                self.positions[symbol]['quantity'] -= quantity
    def update_cash(self, amount):
        self.cash += amount
    def get_portfolio_value(self, current_prices):
        total_value = self.cash
        for symbol, position in self.positions.items():
            if symbol in current_prices:
                total_value += position['quantity'] * current_prices[symbol]
        return total_value
    def get_portfolio_summary(self, current_prices):
        summary = []
        for symbol, position in self.positions.items():
            if symbol in current_prices:
                market_value = position['quantity'] * current_prices[symbol]
                unrealized_pnl = market_value - position['quantity'] * position['average_price']
                summary.append({
                    'symbol': symbol,
                    'quantity': position['quantity'],
                    'average_price': position['average_price'],
                    'current_price': current_prices[symbol],
                    'market_value': market_value,
                    'unrealized_pnl': unrealized_pnl
                })
        return pd.DataFrame(summary)
