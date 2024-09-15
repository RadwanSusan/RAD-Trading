import numpy as np
import pandas as pd
from concurrent.futures import ProcessPoolExecutor
def run_simulation(seed, trade_returns, initial_balance):
	np.random.seed(seed)
	simulated_returns = np.random.choice(trade_returns, size=len(trade_returns), replace=True)
	cumulative_returns = (1 + simulated_returns).cumprod()
	equity_curve = initial_balance * cumulative_returns
	return equity_curve
def monte_carlo_simulation(trades, initial_balance, num_simulations=1000):
	trade_returns = trades['profit'] / trades['entry_price']
	with ProcessPoolExecutor() as executor:
		simulated_equity_curves = list(executor.map(run_simulation,
													range(num_simulations),
													[trade_returns] * num_simulations,
													[initial_balance] * num_simulations))
	simulated_equity_curves = np.array(simulated_equity_curves)
	final_balances = simulated_equity_curves[:, -1]
	results = {
		'mean_final_balance': np.mean(final_balances),
		'median_final_balance': np.median(final_balances),
		'5th_percentile': np.percentile(final_balances, 5),
		'95th_percentile': np.percentile(final_balances, 95),
		'probability_of_profit': np.mean(final_balances > initial_balance),
		'max_drawdown': calculate_max_drawdown(pd.DataFrame(simulated_equity_curves.T)).mean()
	}
	return results, simulated_equity_curves
def calculate_max_drawdown(equity_curve):
	rolling_max = np.maximum.accumulate(equity_curve)
	drawdown = (equity_curve - rolling_max) / rolling_max
	return drawdown.min()
