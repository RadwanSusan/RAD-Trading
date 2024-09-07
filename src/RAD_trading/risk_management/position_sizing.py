# src\RAD_trading\risk_management\position_sizing.py
def calculate_position_size(account_balance, risk_percentage, entry_price, stop_loss_price):
    risk_amount = account_balance * (risk_percentage / 100)
    price_difference = abs(entry_price - stop_loss_price)
    if price_difference == 0:
        return 0
    position_size = risk_amount / price_difference
    return position_size
