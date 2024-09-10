# config\mt5_config.py
mt5_credentials = {
    'login': 110413,
    'password': 'Blackbird@007',
    'server': 'FusionMarkets-Demo',
    'exe_path': "C:\\Program Files\\Fusion Markets MetaTrader 5\\terminal64.exe"
}
def initialize_mt5():
    from RAD_trading.mt5_trade_utils import initialize_mt5, shutdown_mt5
    import atexit
    success = initialize_mt5(
        mt5_credentials['login'],
        mt5_credentials['password'],
        mt5_credentials['server'],
        mt5_credentials['exe_path']
    )
    if success:
        atexit.register(shutdown_mt5)
        print('MT5 initialized')
    else:
        print('Failed to initialize MT5')
    return success
