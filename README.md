# RAD Trading

RAD Trading is a comprehensive trading and backtesting framework developed to facilitate algorithmic trading strategies and analysis.

## Features

-  Backtesting engine
-  Multiple trading strategies
-  Integration with MetaTrader5
-  Data visualization tools
-  Performance analytics
-  Utility functions for financial calculations

## Installation

1. Clone the repository:
   git clone https://github.com/RadwanSusan/RAD-Trading.git
   cd RAD-Trading
2. Create a virtual environment:
   python -m venv venv
   source venv/bin/activate # On Windows use venv\Scripts\activate
3. Install the required packages:
   pip install -r requirements.txt
4. Set up your MetaTrader5 credentials in `config.py`

## Usage

Here's a basic example of how to use the backtester:

```python
from RAD_trading import Backtester, get_ohlc_history
from RAD_trading.utils import calculate_sharpe_ratio
# Get historical data
ohlc_data = get_ohlc_history('EURUSD', mt5.TIMEFRAME_H1, start_date, end_date)
# Define your strategy
def my_strategy(data, trades, orders):
 # Your strategy logic here
 pass
# Set up and run the backtest
bt = Backtester()
bt.set_historical_data(ohlc_data)
bt.set_on_bar(my_strategy)
results = bt.run_backtest()
# Analyze results
sharpe_ratio = calculate_sharpe_ratio(results['profit_net'])
print(f"Sharpe Ratio: {sharpe_ratio}")
# Visualize results
bt.visualize_backtest().show()
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### License

This project is licensed under the MIT License.
These updates ensure that all new functionalities are properly documented and accessible, and that the project structure is consistent and well-organized.
