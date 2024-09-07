# src\RAD_trading\__init__.py
from .backtester import Backtester
from .mt5_trade_utils import (
    send_market_order, close_position, close_all_positions,
    modify_sl_tp, get_positions, place_pending_order,
    modify_position, get_account_info, get_symbol_info,
    calculate_margin_required, wait_for_market_open,
    get_exposure, initialize_mt5, shutdown_mt5
)
__all__ = [
    'Backtester',
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
]
