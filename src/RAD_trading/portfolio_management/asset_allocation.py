# src\RAD_trading\portfolio_management\asset_allocation.py
import numpy as np
from scipy.optimize import minimize
def optimize_portfolio(returns, risk_free_rate=0.02):
    """
    Optimize portfolio weights using Mean-Variance Optimization.
    :param returns: DataFrame of asset returns
    :param risk_free_rate: Risk-free rate
    :return: Optimal weights for each asset
    """
    def portfolio_volatility(weights, returns):
        return np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))
    def portfolio_return(weights, returns):
        return np.sum(returns.mean() * weights) * 252
    def neg_sharpe_ratio(weights, returns, risk_free_rate):
        p_ret = portfolio_return(weights, returns)
        p_vol = portfolio_volatility(weights, returns)
        return -(p_ret - risk_free_rate) / p_vol
    num_assets = returns.shape[1]
    args = (returns, risk_free_rate)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for asset in range(num_assets))
    result = minimize(neg_sharpe_ratio, num_assets*[1./num_assets], args=args,
                      method='SLSQP', bounds=bounds, constraints=constraints)
    return pd.Series(result.x, index=returns.columns)
