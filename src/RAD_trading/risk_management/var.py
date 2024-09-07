# src\RAD_trading\risk_management\var.py
import numpy as np
from scipy import stats
def calculate_var(returns, confidence_level=0.95, time_horizon=1):
    """
    Calculate Value at Risk (VaR) using the historical method.
    :param returns: Series of historical returns
    :param confidence_level: Confidence level for VaR calculation
    :param time_horizon: Time horizon for VaR in days
    :return: VaR value
    """
    var = np.percentile(returns, (1 - confidence_level) * 100)
    return -var * np.sqrt(time_horizon)
def calculate_cvar(returns, confidence_level=0.95):
    """
    Calculate Conditional Value at Risk (CVaR) using the historical method.
    :param returns: Series of historical returns
    :param confidence_level: Confidence level for CVaR calculation
    :return: CVaR value
    """
    var = calculate_var(returns, confidence_level)
    return -returns[returns <= -var].mean()
def monte_carlo_var(current_value, mu, sigma, confidence_level=0.95, time_horizon=1, num_simulations=10000):
    """
    Calculate Value at Risk (VaR) using Monte Carlo simulation.
    :param current_value: Current portfolio value
    :param mu: Expected return (annualized)
    :param sigma: Volatility (annualized)
    :param confidence_level: Confidence level for VaR calculation
    :param time_horizon: Time horizon for VaR in days
    :param num_simulations: Number of Monte Carlo simulations
    :return: VaR value
    """
    dt = time_horizon / 252  # Assuming 252 trading days in a year
    returns = np.random.normal(mu * dt, sigma * np.sqrt(dt), num_simulations)
    simulated_values = current_value * np.exp(returns)
    var = current_value - np.percentile(simulated_values, (1 - confidence_level) * 100)
    return var
