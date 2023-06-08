#!/usr/bin/env python3
import argparse
import ast
import os
from typing import List

import mlflow
import mlflow.sklearn
import numpy as np
from scipy.optimize import curve_fit
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.utils.validation import check_array, check_is_fitted, check_X_y

from src.utils.read import read_parquet_or_csv
from src.utils.split import split_X_y_df


class ExponentialModel(BaseEstimator, RegressorMixin):
    def __init__(self, initial_params: List[float]) -> None:
        self.initial_params = initial_params

    @staticmethod
    def _model_func(x, w0, w1, w2, w3):
        distance = x[:, 0]
        # mileage = x[:, 1]
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="Training script",
        description="Fits the model according to the data passed",
        epilog="End of help",
    )

    parser.add_argument(
        "-i",
        "--initial-params",
        type=ast.literal_eval,
        required=True,
        help="Initial parameters",
    )

    parser.add_argument(
        "-d",
        "--data",
        type=str,
        default=os.path.join(os.getcwd(), "data"),
        required=False,
        help="Where to load data from",
    )

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    print(f"Initial params: {args.initial_params}")
    df = read_parquet_or_csv(path=args.data)
    train, test = train_test_split(df, test_size=0.2, random_state=42)
    X_train, y_train, X_test, y_test = split_X_y_df(
        train=train, test=test, target="coste"
    )
    with mlflow.start_run():
        model = ExponentialModel(initial_params=args.initial_params)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        scoring = mean_squared_error(y_true=y_test, y_pred=y_pred)
        mlflow.log_artifact(train)
        mlflow.log_param("MSE", scoring)
        mlflow.sklearn.log_model(sk_model=model)
    print("Training completed!")


if __name__ == "__main__":
    main()
