from typing import Tuple

import pandas as pd


def split_X_y_df(
    train: pd.DataFrame, test: pd.DataFrame, target: str
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Split the given train and test DataFrames into features (X) and
    target variables (y).

    Args
    ----
    - `train` (pd.DataFrame): The training DataFrame containing both
    features and target variable.
    - `test` (pd.DataFrame): The test DataFrame containing both
    features and target variable.
    - `target` (str): The column name of the target variable.

    Returns
    -------
    `Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]`:
    A tuple containing four DataFrames:
    - `X_train`: The training features DataFrame, which excludes the target variable.
    - `y_train`: The training target variable DataFrame.
    - `X_test`: The test features DataFrame, which excludes the target variable.
    - `y_test`: The test target variable DataFrame.
    """
    X_train = train.drop(columns=target)
    y_train = train[target]
    X_test = test.drop(columns=target)
    y_test = test[target]

    return X_train, y_train, X_test, y_test
