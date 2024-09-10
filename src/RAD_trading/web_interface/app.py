# src\RAD_trading\web_interface\web_interface.py
from flask import Flask, render_template, request, jsonify
from RAD_trading.run_bot import TradingBot
from RAD_trading.strategies import SMAStrategy, RSIStrategy
from RAD_trading.config import mt5_credentials
from RAD_trading import initialize_mt5, shutdown_mt5
from RAD_trading.backtesting import BacktestingEngine
import MetaTrader5 as mt5
import threading
import pandas as pd
app = Flask(__name__)
bot = None
bot_thread = None
backtesting_engine = BacktestingEngine()
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/start_bot', methods=['POST'])
def start_bot():
    global bot, bot_thread
    if bot is None or not bot.is_running:
        symbols = request.form.getlist('symbols')
        timeframe = getattr(mt5, request.form['timeframe'])
        strategy_type = request.form['strategy_type']
        risk_percentage = float(request.form['risk_percentage'])
        if strategy_type == 'SMA':
            strategy_class = lambda symbol, tf: SMAStrategy(symbol, tf, int(request.form['short_period']), int(request.form['long_period']))
        elif strategy_type == 'RSI':
            strategy_class = lambda symbol, tf: RSIStrategy(symbol, tf, int(request.form['rsi_period']), int(request.form['overbought']), int(request.form['oversold']))
        else:
            return jsonify({"status": "error", "message": "Invalid strategy type"})
        bot = TradingBot(symbols, timeframe, strategy_class, risk_percentage)
        if initialize_mt5(mt5_credentials['login'], mt5_credentials['password'], mt5_credentials['server'], mt5_credentials['exe_path']):
            bot_thread = threading.Thread(target=bot.run)
            bot_thread.start()
            return jsonify({"status": "success", "message": "Bot started successfully"})
        else:
            return jsonify({"status": "error", "message": "Failed to initialize MT5"})
    else:
        return jsonify({"status": "error", "message": "Bot is already running"})
@app.route('/stop_bot', methods=['POST'])
def stop_bot():
    global bot
    if bot and bot.is_running:
        bot.stop()
        shutdown_mt5()
        return jsonify({"status": "success", "message": "Bot stopped successfully"})
    else:
        return jsonify({"status": "error", "message": "Bot is not running"})
@app.route('/bot_status')
def bot_status():
    global bot
    if bot and bot.is_running:
        return jsonify({"status": "running"})
    else:
        return jsonify({"status": "stopped"})
@app.route('/performance')
def get_performance():
    if bot and bot.is_running:
        performance = bot.get_performance()
        return jsonify({
            "status": "success",
            "current_balance": performance["current_balance"],
            "profit_loss": performance["profit_loss"],
            "trade_count": performance["trade_count"],
            "win_rate": performance["win_rate"],
            "timestamps": performance["timestamps"],
            "equity_curve": performance["equity_curve"],
            "drawdown": performance["drawdown"]
        })
    else:
        return jsonify({"status": "error", "message": "Bot is not running"})
@app.route('/backtest', methods=['POST'])
def run_backtest():
    symbol = request.form['symbol']
    timeframe = getattr(mt5, request.form['timeframe'])
    start_date = pd.to_datetime(request.form['start_date'])
    end_date = pd.to_datetime(request.form['end_date'])
    initial_balance = float(request.form['initial_balance'])
    strategy_params = {
        'short_period': int(request.form['short_period']),
        'long_period': int(request.form['long_period'])
    }
    results = backtesting_engine.run_backtest(symbol, timeframe, start_date, end_date, initial_balance, strategy_params)
    return jsonify({
        'sharpe_ratio': results['sharpe_ratio'],
        'max_drawdown': results['max_drawdown'],
        'equity_plot': results['equity_plot'],
        'drawdown_plot': results['drawdown_plot'],
        'final_balance': results['equity_curve'].iloc[-1]
    })
if __name__ == '__main__':
    app.run(debug=True)
