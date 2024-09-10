# src/RAD_trading/strategies/strategy_loader.py
import importlib
import os
def load_strategies():
    strategy_dir = os.path.join(os.path.dirname(__file__), 'custom_strategies')
    strategies = {}
    for filename in os.listdir(strategy_dir):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = filename[:-3]
            module = importlib.import_module(f'.custom_strategies.{module_name}', package='RAD_trading.strategies')
            for item_name in dir(module):
                item = getattr(module, item_name)
                if isinstance(item, type) and item.__name__.endswith('Strategy'):
                    strategies[item.__name__] = item
    return strategies
