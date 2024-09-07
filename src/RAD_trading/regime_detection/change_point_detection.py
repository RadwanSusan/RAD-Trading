# src\RAD_trading\regime_detection\change_point_detection.py
import numpy as np
from ruptures import Pelt
def detect_change_points(data, model="l2", min_size=5):
    """
    Detect change points in time series data.
    :param data: 1D numpy array of time series data
    :param model: Cost model for change point detection ("l1", "l2", "rbf", etc.)
    :param min_size: Minimum segment length
    :return: List of detected change points
    """
    algo = Pelt(model=model, min_size=min_size).fit(data)
    change_points = algo.predict(pen=np.log(len(data)) * 0.5)
    return change_points[:-1]  # Exclude the last change point (end of series)
