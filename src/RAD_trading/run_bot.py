# src\RAD_trading\run_bot.py
import MetaTrader5 as mt5
from RAD_trading.config import mt5_credentials
from RAD_trading import (
    initialize_mt5, shutdown_mt5, send_market_order,
    close_all_positions, get_positions
)
import time
import pandas as pd
def strategy(symbol, timeframe):
    # Fetch the latest data
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, 100)
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    # Calculate indicators
    df['sma_fast'] = df['close'].rolling(window=10).mean()
    df['sma_slow'] = df['close'].rolling(window=20).mean()
    # Generate signals
    last_row = df.iloc[-1]
    if last_row['sma_fast'] > last_row['sma_slow']:
        return 'buy'
    elif last_row['sma_fast'] < last_row['sma_slow']:
        return 'sell'
    else:
        return None
def run_bot():
    symbol = "ETHUSD"
    timeframe = mt5.TIMEFRAME_M5
    volume = 0.01
    while True:
        try:
            # Get the current signal
            signal = strategy(symbol, timeframe)
            # Get current positions
            positions = get_positions()
            if signal == 'buy' and len(positions) == 0:
                print("Opening Buy position")
                send_market_order(symbol, volume, 'buy')
            elif signal == 'sell' and len(positions) == 0:
                print("Opening Sell position")
                send_market_order(symbol, volume, 'sell')
            elif signal is None and len(positions) > 0:
                print("Closing all positions")
                close_all_positions()
            # Wait for next candle
            time.sleep(60)  # Sleep for 1 minute (adjust based on your timeframe)
        except Exception as e:
            print(f"An error occurred: {e}")
            break
if __name__ == "__main__":
    if initialize_mt5(mt5_credentials['login'], mt5_credentials['password'], mt5_credentials['server'], mt5_credentials['exe_path']):
        try:
            run_bot()
        finally:
            shutdown_mt5()
    else:
        print("Failed to initialize MT5. Bot not started.")
