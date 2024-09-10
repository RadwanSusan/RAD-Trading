# src\RAD_trading\logging_config.py
import logging
from logging.handlers import RotatingFileHandler
import os
def setup_logger(name, log_file, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
# Setup loggers
trading_logger = setup_logger('trading', 'logs/trading.log')
backtesting_logger = setup_logger('backtesting', 'logs/backtesting.log')
performance_logger = setup_logger('performance', 'logs/performance.log')
