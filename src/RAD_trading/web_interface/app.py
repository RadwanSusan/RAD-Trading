# src\RAD_trading\web_interface\app.py
from flask import Flask, render_template, request, jsonify
from RAD_trading.backtesting.backtesting_interface import BacktestingInterface
import pandas as pd
from RAD_trading.logging_config import backtesting_logger
app = Flask(__name__)
backtesting_interface = BacktestingInterface()
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/strategies')
def get_strategies():
    return jsonify(backtesting_interface.list_strategies())
@app.route('/strategy_parameters')
def get_strategy_parameters():
    strategy_name = request.args.get('strategy')
    try:
        params = backtesting_interface.get_strategy_parameters(strategy_name)
        return jsonify(params)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
@app.route('/compare_strategies', methods=['POST'])
def compare_strategies():
    data = request.json
    try:
        comparison, results = backtesting_interface.compare_strategies(
            data['backtest_params'],
            data['strategies_to_compare']
        )
        return jsonify({
            'comparison': comparison.to_dict(),
            'results': results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400
@app.route('/run_backtest', methods=['POST'])
def run_backtest():
    data = request.json
    try:
        results = backtesting_interface.run_backtest(
            data['strategy'],
            data['symbol'],
            data['timeframe'],
            pd.to_datetime(data['start_date']),
            pd.to_datetime(data['end_date']),
            float(data['initial_balance']),
            data['strategy_params']
        )
        return jsonify({
            'metrics': results['metrics'].to_dict(),
            'equity_plot': results['equity_plot'],
            'drawdown_plot': results['drawdown_plot'],
            'trades': results['trades'].to_dict(orient='records')
        })
    except Exception as e:
        backtesting_logger.error(f"Error during backtest: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 400
@app.route('/optimize_strategy', methods=['POST'])
def optimize_strategy():
    data = request.json
    try:
        best_params, best_metric = backtesting_interface.optimize_strategy(
            data['strategy'],
            data['symbol'],
            data['timeframe'],
            pd.to_datetime(data['start_date']),
            pd.to_datetime(data['end_date']),
            data['initial_balance'],
            data['param_ranges'],
            data.get('optimization_metric', 'sharpe_ratio')
        )
        return jsonify({
            'best_params': best_params,
            'best_metric': best_metric
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400
@app.route('/run_monte_carlo', methods=['POST'])
def run_monte_carlo():
    data = request.json
    try:
        backtest_results = backtesting_interface.run_backtest(
            data['strategy'],
            data['symbol'],
            data['timeframe'],
            pd.to_datetime(data['start_date']),
            pd.to_datetime(data['end_date']),
            data['initial_balance'],
            data['strategy_params']
        )
        mc_results, simulated_equity_curves = backtesting_interface.run_monte_carlo(backtest_results, data.get('num_simulations', 1000))
        return jsonify({
            'mc_results': mc_results,
            'simulated_equity_curves': simulated_equity_curves.tolist()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400
if __name__ == '__main__':
    app.run(debug=True)
