# src\RAD_trading\portfolio_optimization\efficient_frontier.py
import numpy as np
import pandas as pd
from scipy.optimize import minimize
class EfficientFrontier:
    def __init__(self, returns, cov_matrix, risk_free_rate=0.02):
        self.returns = returns
        self.cov_matrix = cov_matrix
        self.risk_free_rate = risk_free_rate
    def portfolio_return(self, weights):
        return np.sum(self.returns.mean() * weights) * 252
    def portfolio_volatility(self, weights):
        return np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix * 252, weights)))
    def sharpe_ratio(self, weights):
        return (self.portfolio_return(weights) - self.risk_free_rate) / self.portfolio_volatility(weights)
    def minimize_volatility(self, target_return=None):
        num_assets = len(self.returns.columns)
        args = (self.cov_matrix,)
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bound = (0.0, 1.0)
        bounds = tuple(bound for asset in range(num_assets))
        if target_return:
            constraints = ({'type': 'eq', 'fun': lambda x: self.portfolio_return(x) - target_return},
                           {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        result = minimize(self.portfolio_volatility, num_assets*[1./num_assets,], args=args,
                          method='SLSQP', bounds=bounds, constraints=constraints)
        return result.x
    def maximize_sharpe_ratio(self):
        num_assets = len(self.returns.columns)
        args = (self.returns, self.cov_matrix, self.risk_free_rate)
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bound = (0.0, 1.0)
        bounds = tuple(bound for asset in range(num_assets))
        result = minimize(lambda x: -self.sharpe_ratio(x), num_assets*[1./num_assets,], args=args,
                          method='SLSQP', bounds=bounds, constraints=constraints)
        return result.x
    def efficient_frontier(self, points=100):
        target_returns = np.linspace(self.returns.mean().min(), self.returns.mean().max(), points)
        efficient_portfolios = [self.minimize_volatility(target_return) for target_return in target_returns]
        return pd.DataFrame({
            'Return': [self.portfolio_return(w) for w in efficient_portfolios],
            'Volatility': [self.portfolio_volatility(w) for w in efficient_portfolios]
        })
