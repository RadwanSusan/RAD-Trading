# src\RAD_trading\factor_modeling\factor_model.py
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
class FactorModel:
    def __init__(self, factors):
        self.factors = factors
        self.model = LinearRegression()
    def fit(self, returns, factor_data):
        X = factor_data[self.factors]
        y = returns
        self.model.fit(X, y)
    def get_factor_loadings(self):
        return pd.Series(self.model.coef_, index=self.factors)
    def get_alpha(self):
        return self.model.intercept_
    def predict(self, factor_data):
        X = factor_data[self.factors]
        return self.model.predict(X)
    def calculate_r_squared(self, returns, factor_data):
        X = factor_data[self.factors]
        return self.model.score(X, returns)
    def decompose_returns(self, returns, factor_data):
        factor_returns = self.predict(factor_data)
        alpha = returns - factor_returns
        return pd.DataFrame({
            'total_return': returns,
            'factor_return': factor_returns,
            'alpha': alpha
        })
