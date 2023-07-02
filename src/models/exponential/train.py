#!/usr/bin/env python3
import argparse
import ast
import getpass
import logging
import os
import platform
from typing import List

import mlflow.sklearn
import numpy as np
from scipy.optimize import curve_fit
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.utils.validation import check_array, check_is_fitted, check_X_y

import mlflow
from src.utils.read import (
    get_folder_permissions,
    get_owner_and_group_ids,
    join_path,
    read_parquet_or_csv,
)
from src.utils.split import split_X_y_df

logging.basicConfig(level=logging.DEBUG)


def setup_logger() -> logging.Logger:
    # Set up logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create console handler and set level to debug
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Add formatter to console handler
    console_handler.setFormatter(formatter)

    # Add console handler to logger
    logger.addHandler(console_handler)

    return logger


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
            self._model_func,
            xdata=X,
            ydata=y,
            p0=self.initial_params,
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


def parse_args() -> argparse.Namespace:
    default_data_path = os.path.join(os.getcwd(), "data")
    default_init_params = np.random.uniform(-5, 5, size=4)
    parser = argparse.ArgumentParser(
        prog="Training script",
        description="Fits the model according to the data passed",
        epilog="End of help",
    )

    parser.add_argument(
        "-i",
        "--initial-params",
        type=ast.literal_eval,
        required=False,
        default=default_init_params,
        help=f"Initial parameters. Default: {default_init_params}",
    )

    parser.add_argument(
        "-d",
        "--data",
        type=str,
        default=default_data_path,
        required=False,
        help=f"Where to load data from. Default: {default_data_path}",
    )

    parser.add_argument(
        "-t",
        "--train-name",
        type=str,
        default="train.parquet",
        required=False,
        help="The name of the training dataset. Default: train.parquet",
    )

    parser.add_argument(
        "-v",
        "--validation-name",
        type=str,
        default="test.parquet",
        required=False,
        help="The name of the validation dataset. Default: test.parquet",
    )

    parser.add_argument(
        "-m",
        "--mlflow-tracking",
        required=False,
        help="The MLFlow tracking uri",
    )

    args = parser.parse_args()
    return args


def main():
    TARGET_FIELD = "coste"
    logger = setup_logger()
    logger.debug(f"Current user: {getpass.getuser()}")
    logger.debug(f"Current host: {platform.node()}")
    args = parse_args()
    logger.debug(f"Input arguments: {args}")
    logger.info(f"Initial params: {args.initial_params}")
    train = read_parquet_or_csv(path=join_path(args.data, args.train_name, sep="/"))
    test = read_parquet_or_csv(path=join_path(args.data, args.validation_name, sep="/"))
    logger.debug(f"Train dataset size: {len(train)}\nTest dataset size: {len(test)}")

    X_train, y_train, X_test, y_test = split_X_y_df(
        train=train, test=test, target=TARGET_FIELD
    )
    if args.mlflow_tracking:
        mlflow.set_tracking_uri(args.mlflow_tracking)
    with mlflow.start_run() as run:  # noqa: F841
        model = ExponentialModel(initial_params=args.initial_params)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        scoring = mean_squared_error(y_true=y_test, y_pred=y_pred)
        r2 = r2_score(y_true=y_test, y_pred=y_pred)
        maximum_error = np.max(np.abs(y_pred - y_test))
        logger.debug(f"Data folder permissions: {get_folder_permissions('data')}")
        logger.debug(f"Data folder owner: {get_owner_and_group_ids('data')}")
        mlflow.log_artifact("data")
        mlflow.log_param("initial_points", args.initial_params)
        mlflow.log_param("best_params", model.best_params_)
        mlflow.log_param("estimation_err", model.estimation_err_)
        mlflow.log_param("condition_number", model.cond_)
        mlflow.log_metric("MSE", scoring)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("maximum_error", maximum_error)
        mlflow.sklearn.log_model(sk_model=model, artifact_path="model")
    logger.info("Training completed!")


if __name__ == "__main__":
    main()
