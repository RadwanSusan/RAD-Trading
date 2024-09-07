# src\RAD_trading\options\black_scholes.py
import numpy as np
from scipy.stats import norm
class BlackScholes:
    @staticmethod
    def d1(S, K, T, r, sigma):
        return (np.log(S/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
    @staticmethod
    def d2(S, K, T, r, sigma):
        return BlackScholes.d1(S, K, T, r, sigma) - sigma*np.sqrt(T)
    @staticmethod
    def call_price(S, K, T, r, sigma):
        d1 = BlackScholes.d1(S, K, T, r, sigma)
        d2 = BlackScholes.d2(S, K, T, r, sigma)
        return S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
    @staticmethod
    def put_price(S, K, T, r, sigma):
        d1 = BlackScholes.d1(S, K, T, r, sigma)
        d2 = BlackScholes.d2(S, K, T, r, sigma)
        return K*np.exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)
