# src/RAD_trading/__init__.py
from .backtesting import BacktestingEngine, BacktestingInterface
from .mt5_trade_utils import (
    send_market_order, close_position, close_all_positions,
    modify_sl_tp, get_positions, place_pending_order,
    modify_position, get_account_info, get_symbol_info,
    calculate_margin_required, wait_for_market_open,
    get_exposure, initialize_mt5, shutdown_mt5
)
from .notifications import email_notifier
from .logging_config import trading_logger, backtesting_logger, performance_logger
from .web_interface import app
__all__ = [
    'BacktestingEngine',
    'BacktestingInterface',
    'send_market_order',
    'close_position',
    'close_all_positions',
    'modify_sl_tp',
    'get_positions',
    'place_pending_order',
    'modify_position',
    'get_account_info',
    'get_symbol_info',
    'calculate_margin_required',
    'wait_for_market_open',
    'get_exposure',
    'initialize_mt5',
    'shutdown_mt5',
    'email_notifier',
    'trading_logger',
    'backtesting_logger',
    'performance_logger',
    'app',
]
