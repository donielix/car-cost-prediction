#!/usr/bin/env python3
import argparse
import getpass
import logging
import os
import platform
from typing import Dict

import mlflow.sklearn
import numpy as np
from hyperopt import STATUS_OK, Trials, fmin, hp, tpe
from sklearn.metrics import make_scorer, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score

import mlflow
from src.models.exponential.base import ExponentialModel
from src.models.exponential.preprocessing import ColumnDropperTransformer
from src.utils.read import (
    get_folder_permissions,
    get_owner_and_group_ids,
    join_path,
    read_parquet_or_csv,
)
from src.utils.split import split_X_y_df


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


def parse_args() -> argparse.Namespace:
    default_data_path = os.path.join(os.getcwd(), "data")
    parser = argparse.ArgumentParser(
        prog="Training script",
        description="Fits the model according to the data passed",
        epilog="End of help",
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


def hyperparameter_optimization(model, X_train, y_train, max_evals=1000):
    scorer = make_scorer(score_func=mean_squared_error, greater_is_better=False)

    def objective(params: Dict) -> Dict:
        estimator = model(**params)
        score = cross_val_score(
            estimator=estimator,
            X=X_train,
            y=y_train,
            scoring=scorer,
            n_jobs=-1,
        ).mean()
        return {"loss": -score, "status": STATUS_OK}

    space = {
        "w0": hp.uniform("w0", 0, 10),
        "w1": hp.uniform("w1", 0, 15),
        "w2": hp.uniform("w2", 0, 15),
        "w3": hp.normal("w3", 0, 15),
    }
    trials = Trials()
    best = fmin(
        objective,
        space,
        algo=tpe.suggest,
        max_evals=max_evals,
        verbose=False,
        show_progressbar=True,
        trials=trials,
    )
    return best, trials


def main():
    TARGET_FIELD = "coste"
    logger = setup_logger()
    logger.debug(f"Current user: {getpass.getuser()}")
    logger.debug(f"Current host: {platform.node()}")
    args = parse_args()
    logger.debug(f"Input arguments: {args}")
    train = read_parquet_or_csv(path=join_path(args.data, args.train_name, sep="/"))
    test = read_parquet_or_csv(path=join_path(args.data, args.validation_name, sep="/"))
    logger.debug(f"Train dataset size: {len(train)}\nTest dataset size: {len(test)}")
    logger.debug("Preprocessing data...")
    dropper = ColumnDropperTransformer(columns=["consumo_medio"])
    train = dropper.transform(train)
    test = dropper.transform(test)

    X_train, y_train, X_test, y_test = split_X_y_df(
        train=train, test=test, target=TARGET_FIELD
    )
    if args.mlflow_tracking:
        mlflow.set_tracking_uri(args.mlflow_tracking)
    with mlflow.start_run() as run:  # noqa: F841
        best, trials = hyperparameter_optimization(
            model=ExponentialModel, X_train=X_train, y_train=y_train
        )
        model = ExponentialModel(**best)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        scoring = mean_squared_error(y_true=y_test, y_pred=y_pred)
        r2 = r2_score(y_true=y_test, y_pred=y_pred)
        maximum_error = np.max(np.abs(y_pred - y_test))
        logger.debug(f"Data folder permissions: {get_folder_permissions('data')}")
        logger.debug(f"Data folder owner: {get_owner_and_group_ids('data')}")
        mlflow.log_artifact("data")
        mlflow.log_param("best_params", model.best_params_)
        mlflow.log_param("estimation_err", model.estimation_err_)
        mlflow.log_param("condition_number", model.cond_)
        mlflow.log_metric("MSE", scoring)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("maximum_error", maximum_error)
        mlflow.sklearn.log_model(sk_model=model, artifact_path="model")
        mlflow.artifacts.download_artifacts(
            artifact_uri=run.info.artifact_uri + "/model/", dst_path="model/"
        )
    logger.info("Training completed!")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
