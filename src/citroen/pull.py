#!/usr/bin/env python3

from pathlib import Path
import awswrangler as wr
import pandas as pd
from sklearn.model_selection import train_test_split
import os

_HERE = Path(__file__).resolve().parent

def pull_data(query: str, database: str) -> pd.DataFrame:
    """
    Pull data from AWS Athena
    """
    return wr.athena.read_sql_query(sql=query, database=database)


def save_data(df: pd.DataFrame, path: str, test_size: float, random_state: int = 42) -> None:
    """
    Save DataFrame into a train and tests files
    """
    train , test = train_test_split(
        df, test_size=test_size, random_state=random_state
    )

    train.to_parquet(os.path.join(path, "train.parquet"), index=False)
    test.to_parquet(os.path.join(path, "test.parquet"), index=False)


if __name__ == "__main__":
    with open(_HERE / "data.sql") as sql_file:
        SQL = sql_file.read()
    df = pull_data(query=SQL, database="citroen-database")
    save_data(df=df, path="data", test_size=0.2)
