# src\RAD_trading\options\implied_volatility.py
import numpy as np
from scipy.optimize import brentq
from .black_scholes import BlackScholes
class ImpliedVolatility:
    @staticmethod
    def calculate_call_iv(S, K, T, r, market_price):
        def objective(sigma):
            return BlackScholes.call_price(S, K, T, r, sigma) - market_price
        return brentq(objective, 1e-6, 10)
    @staticmethod
    def calculate_put_iv(S, K, T, r, market_price):
        def objective(sigma):
            return BlackScholes.put_price(S, K, T, r, sigma) - market_price
        return brentq(objective, 1e-6, 10)
