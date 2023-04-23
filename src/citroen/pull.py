#!/usr/bin/env python3

import argparse
import os
from pathlib import Path

import awswrangler as wr
import pandas as pd
from sklearn.model_selection import train_test_split

_HERE = Path(__file__).resolve().parent


def pull_data(query: str, database: str) -> pd.DataFrame:
    """
    Pull data from AWS Athena
    """
    return wr.athena.read_sql_query(sql=query, database=database)


def save_data(
    df: pd.DataFrame, path: str, test_size: float, random_state: int = 42
) -> None:
    """
    Save DataFrame into a train and tests files
    """
    train, test = train_test_split(df, test_size=test_size, random_state=random_state)
    path_ = Path(path)
    if not path_.exists():
        path_.mkdir(parents=True, exist_ok=True)

    train.to_parquet(os.path.join(path, "train.parquet"), index=False)
    test.to_parquet(os.path.join(path, "test.parquet"), index=False)


def main(args: argparse.Namespace):
    """
    Main function.
    """
    with open(_HERE / "data.sql") as sql_file:
        SQL = sql_file.read()
    df = pull_data(query=SQL, database=args.database)
    save_data(df=df, path=args.data, test_size=0.2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Pulling script",
        description="Pulls the data from AWS S3 into the data folder",
        epilog="End of help",
    )
    parser.add_argument(
        "-d",
        "--data",
        type=str,
        required=False,
        default=os.path.join(os.getcwd(), "data"),
        help="Path where to store the pulled data",
    )
    parser.add_argument(
        "--database",
        type=str,
        required=False,
        default="citroen-database",
        help="AWS Glue database",
    )
    args = parser.parse_args()
    main(args)
