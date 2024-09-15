# src\RAD_trading\mt5_trade_utils\trade_utils.py
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import time


def send_market_order(
    symbol,
    tick_volume,
    order_type,
    sl=0.0,
    tp=0.0,
    deviation=20,
    comment="",
    magic=0,
    type_filling=mt5.ORDER_FILLING_IOC,
):
    tick = mt5.symbol_info_tick(symbol)
    order_dict = {"buy": mt5.ORDER_TYPE_BUY, "sell": mt5.ORDER_TYPE_SELL}
    price_dict = {"buy": tick.ask, "sell": tick.bid}
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "tick_volume": float(tick_volume),
        "type": order_dict[order_type],
        "price": price_dict[order_type],
        "sl": sl,
        "tp": tp,
        "deviation": deviation,
        "magic": magic,
        "comment": comment,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": type_filling,
    }
    order_result = mt5.order_send(request)
    if order_result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Order send failed: {order_result.comment}")
        return None
    return order_result


def close_position(
    position, deviation=20, magic=0, comment="", type_filling=mt5.ORDER_FILLING_IOC
):
    order_type_dict = {
        mt5.ORDER_TYPE_BUY: mt5.ORDER_TYPE_SELL,
        mt5.ORDER_TYPE_SELL: mt5.ORDER_TYPE_BUY,
    }
    price_dict = {
        mt5.ORDER_TYPE_BUY: mt5.symbol_info_tick(position.symbol).bid,
        mt5.ORDER_TYPE_SELL: mt5.symbol_info_tick(position.symbol).ask,
    }
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "position": position.ticket,
        "symbol": position.symbol,
        "tick_volume": position.tick_volume,
        "type": order_type_dict[position.type],
        "price": price_dict[position.type],
        "deviation": deviation,
        "magic": magic,
        "comment": comment,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": type_filling,
    }
    order_result = mt5.order_send(request)
    if order_result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Order close failed: {order_result.comment}")
        return None
    return order_result


def close_all_positions(
    order_type="all", magic=None, type_filling=mt5.ORDER_FILLING_IOC
):
    order_type_dict = {"buy": mt5.ORDER_TYPE_BUY, "sell": mt5.ORDER_TYPE_SELL}
    if mt5.positions_total() > 0:
        positions = mt5.positions_get()
        if positions is None:
            print("No positions to close")
            return []
        positions_df = pd.DataFrame(
            list(positions), columns=positions[0]._asdict().keys()
        )
        if magic is not None:
            positions_df = positions_df[positions_df["magic"] == magic]
        if order_type != "all":
            positions_df = positions_df[
                (positions_df["type"] == order_type_dict[order_type])
            ]
        if positions_df.empty:
            print("No open positions matching the criteria")
            return []
        results = []
        for _, position in positions_df.iterrows():
            order_result = close_position(position, type_filling=type_filling)
            results.append(order_result)
        return results
    else:
        print("No positions to close")
        return []


def modify_sl_tp(ticket, stop_loss, take_profit):
    position = mt5.positions_get(ticket=ticket)
    if not position:
        print(f"Position with ticket {ticket} not found")
        return None
    position = position[0]
    request = {
        "action": mt5.TRADE_ACTION_SLTP,
        "position": ticket,
        "symbol": position.symbol,
        "sl": stop_loss,
        "tp": take_profit,
    }
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Modify SL/TP failed: {result.comment}")
        return None
    return result


def get_positions(magic=None):
    if mt5.positions_total() > 0:
        positions = mt5.positions_get()
        if positions is None:
            print("Failed to get open positions")
            return pd.DataFrame()
        positions_df = pd.DataFrame(
            list(positions), columns=positions[0]._asdict().keys()
        )
        if magic is not None:
            positions_df = positions_df[positions_df["magic"] == magic]
        return positions_df
    else:
        return pd.DataFrame()


def place_pending_order(
    symbol,
    tick_volume,
    order_type,
    price,
    sl=0.0,
    tp=0.0,
    deviation=20,
    comment="",
    magic=0,
    type_filling=mt5.ORDER_FILLING_IOC,
):
    order_type_dict = {
        "buy_limit": mt5.ORDER_TYPE_BUY_LIMIT,
        "sell_limit": mt5.ORDER_TYPE_SELL_LIMIT,
        "buy_stop": mt5.ORDER_TYPE_BUY_STOP,
        "sell_stop": mt5.ORDER_TYPE_SELL_STOP,
    }
    request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": symbol,
        "tick_volume": float(tick_volume),
        "type": order_type_dict[order_type],
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": deviation,
        "magic": magic,
        "comment": comment,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": type_filling,
    }
    order_result = mt5.order_send(request)
    if order_result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Pending order placement failed: {order_result.comment}")
        return None
    return order_result


def modify_position(ticket, sl=None, tp=None):
    position = mt5.positions_get(ticket=ticket)
    if not position:
        print(f"Position with ticket {ticket} not found")
        return None
    position = position[0]
    request = {
        "action": mt5.TRADE_ACTION_SLTP,
        "position": ticket,
        "symbol": position.symbol,
        "sl": sl if sl is not None else position.sl,
        "tp": tp if tp is not None else position.tp,
    }
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Position modification failed: {result.comment}")
        return None
    return result


def get_account_info():
    account_info = mt5.account_info()
    if account_info is None:
        print("Failed to get account info")
        return None
    return {
        "balance": account_info.balance,
        "equity": account_info.equity,
        "profit": account_info.profit,
        "margin": account_info.margin,
        "margin_free": account_info.margin_free,
        "margin_level": account_info.margin_level,
        "currency": account_info.currency,
    }


def get_symbol_info(symbol):
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(f"Failed to get symbol info for {symbol}")
        return None
    return {
        "spread": symbol_info.spread,
        "digits": symbol_info.digits,
        "trade_contract_size": symbol_info.trade_contract_size,
        "trade_tick_value": symbol_info.trade_tick_value,
        "trade_tick_size": symbol_info.trade_tick_size,
        "volume_min": symbol_info.volume_min,
        "volume_max": symbol_info.volume_max,
        "volume_step": symbol_info.volume_step,
    }


def calculate_margin_required(symbol, tick_volume, order_type):
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(f"Failed to get symbol info for {symbol}")
        return None
    order_type_dict = {"buy": mt5.ORDER_TYPE_BUY, "sell": mt5.ORDER_TYPE_SELL}
    margin = mt5.order_calc_margin(
        order_type_dict[order_type], symbol, tick_volume, symbol_info.ask
    )
    if margin is None:
        print(f"Failed to calculate margin for {symbol}")
        return None
    return margin


def wait_for_market_open(symbol, timeout=3600):
    start_time = time.time()
    while time.time() - start_time < timeout:
        symbol_info = mt5.symbol_info(symbol)
        if (
            symbol_info is not None
            and symbol_info.trade_mode != mt5.SYMBOL_TRADE_MODE_DISABLED
        ):
            return True
        time.sleep(1)
    print(f"Timeout waiting for market to open for {symbol}")
    return False


def get_exposure(symbol):
    positions = mt5.positions_get(symbol=symbol)
    if positions is None:
        return 0
    exposure = sum(
        pos.tick_volume if pos.type == mt5.ORDER_TYPE_BUY else -pos.tick_volume
        for pos in positions
    )
    return exposure


def initialize_mt5(login, password, server, path=None):
    if not mt5.initialize(path=path):
        print("MetaTrader5 package initialization failed")
        return False
    if not mt5.login(login, password, server):
        print("MetaTrader5 login failed")
        mt5.shutdown()
        return False
    print("MetaTrader5 connection established")
    return True


def shutdown_mt5():
    mt5.shutdown()
    print("MetaTrader5 connection closed")
