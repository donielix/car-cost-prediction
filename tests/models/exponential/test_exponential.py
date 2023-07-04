import numpy as np
import pytest
from sklearn.metrics import mean_squared_error, r2_score

from src.models.exponential.train import ExponentialModel, hyperparameter_optimization
from src.utils.read import join_path, read_parquet_or_csv
from src.utils.split import split_X_y_df


@pytest.fixture
def train_test():
    train = read_parquet_or_csv(path=join_path("data", "train.parquet", sep="/"))
    test = read_parquet_or_csv(path=join_path("data", "test.parquet", sep="/"))
    X_train, y_train, X_test, y_test = split_X_y_df(
        train=train, test=test, target="coste"
    )
    return X_train, y_train, X_test, y_test


def test_exponential(train_test):
    X_train, y_train, X_test, y_test = train_test
    best, trials = hyperparameter_optimization(
        X_train=X_train, y_train=y_train, max_evals=100
    )
    model = ExponentialModel(**best)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    scoring = mean_squared_error(y_true=y_test, y_pred=y_pred)
    r2 = r2_score(y_true=y_test, y_pred=y_pred)
    maximum_error = np.max(np.abs(y_pred - y_test))
    assert r2 > 0.9
    assert scoring < 0.4
    assert maximum_error < 5
