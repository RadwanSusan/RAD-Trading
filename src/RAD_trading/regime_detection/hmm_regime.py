# src\RAD_trading\regime_detection\hmm_regime.py
from hmmlearn import hmm
import numpy as np
class HMMRegimeDetector:
    def __init__(self, n_regimes=2):
        self.n_regimes = n_regimes
        self.model = hmm.GaussianHMM(n_components=n_regimes, covariance_type="full")
    def fit(self, returns):
        self.model.fit(returns.reshape(-1, 1))
    def predict_regime(self, returns):
        return self.model.predict(returns.reshape(-1, 1))
    def get_regime_parameters(self):
        means = self.model.means_.flatten()
        variances = np.array([np.diag(cv) for cv in self.model.covars_]).flatten()
        return [{'mean': mean, 'variance': var} for mean, var in zip(means, variances)]
    def get_transition_matrix(self):
        return self.model.transmat_
