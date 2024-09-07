# src\RAD_trading\events\event_types.py
from dataclasses import dataclass
@dataclass
class TradeEvent:
    type: str
    symbol: str
    order_type: str
    volume: float
    price: float
@dataclass
class SignalEvent:
    type: str
    symbol: str
    signal: str
    strength: float
