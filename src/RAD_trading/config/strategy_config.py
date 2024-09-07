# config\strategy_config.py
SMA_STRATEGY_CONFIG = {
    'symbol': 'EURUSD',
    'timeframe': '1h',
    'short_period': 20,
    'long_period': 50,
    'risk_percentage': 1,
    'stop_loss_pips': 50
}
BOLLINGER_STRATEGY_CONFIG = {
    'symbol': 'GBPUSD',
    'timeframe': '4h',
    'period': 20,
    'num_std': 2,
    'risk_percentage': 1,
    'stop_loss_atr_multiplier': 2
}
