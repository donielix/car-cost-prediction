import numpy as np
from scipy.optimize import curve_fit
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.utils.validation import check_array, check_is_fitted, check_X_y

from src.utils.decorators import delete_fitted_attributes_if_error


class ExponentialModel(BaseEstimator, RegressorMixin):
    def __init__(
        self,
        w0: float = 0.0,
        w1: float = 0.0,
        w2: float = 0.0,
        w3: float = 0.0,
    ) -> None:
        self.w0 = w0
        self.w1 = w1
        self.w2 = w2
        self.w3 = w3

    @staticmethod
    def _model_func(x, w0, w1, w2, w3):
        distance = x[:, 0]
        # mileage = x[:, 1]
        fuel_price = x[:, 2]

        consumption = w0 + w1 * np.exp(-w2 * distance + w3)
        price = consumption * distance * fuel_price
        return price

    @delete_fitted_attributes_if_error
    def fit(self, X, y):
        # Store the data seen during fit
        self.X_ = X
        self.y_ = y
        # Check that X and y have correct shape
        X, y = check_X_y(X, y)
        self.best_params_, pcov = curve_fit(
            self._model_func,
            xdata=X,
            ydata=y,
            p0=[getattr(self, f"w{i}") for i in range(4)],
            maxfev=10000,
        )
        self.estimation_err_ = np.sqrt(np.diag(pcov))
        self.cond_ = np.linalg.cond(pcov)
        # Return the classifier
        return self

    def predict(self, X):
        # Check if fit has been called
        check_is_fitted(self)
        # Input validation
        X = check_array(X)
        return self._model_func(X, *self.best_params_)

    def predict_endpoint(
        self, distance: float, mileage: float, fuel_price: float, precision: int = 3
    ) -> float:
        # Check if fit has been called
        check_is_fitted(self)
        X = np.array([[distance, mileage, fuel_price]], dtype=np.float64)
        # Input validation
        X = check_array(X)
        return round(
            number=float(self._model_func(X, *self.best_params_)), ndigits=precision
        )
