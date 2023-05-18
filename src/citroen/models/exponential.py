from typing import List
from scipy.optimize import curve_fit
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
import numpy as np


class ExponentialModel(BaseEstimator, RegressorMixin):
    def __init__(self, initial_params: List[float]) -> None:
        self.initial_params = initial_params

    @staticmethod
    def _model_func(x, w0, w1, w2, w3):
        distance = x[:, 0]
        mileage = x[:, 1]
        fuel_price = x[:, 2]

        consumption = w0 + w1 * np.exp(-w2 * distance + w3)
        price = consumption * distance * fuel_price
        return price

    def fit(self, X, y):
        # Check that X and y have correct shape
        X, y = check_X_y(X, y)
        # Store the classes seen during fit
        self.X_ = X
        self.y_ = y
        self.best_params_, pcov = curve_fit(
            self._model_func, xdata=X, ydata=y, p0=self.initial_params
        )
        self.estimation_err_ = np.sqrt(np.diag(pcov))
        # Return the classifier
        return self

    def predict(self, X):
        # Check if fit has been called
        check_is_fitted(self)
        # Input validation
        X = check_array(X)
        return self._model_func(X, *self.best_params_)
