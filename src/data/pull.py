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
    Execute an SQL query on an AWS Athena database and return the result
    as a pandas DataFrame.

    Parameters
    ----------
    `query` : str
        The SQL query to execute on the Athena database.
    `database` : str
        The name of the Athena database to execute the query on.

    Returns
    -------
    `pd.DataFrame`
        A pandas DataFrame containing the result of the query.

    Examples
    --------
    >>> import pandas as pd
    >>> query = "SELECT * FROM mytable WHERE category='books' AND price > 10"
    >>> database = "my_athena_database"
    >>> df = pull_data(query, database)

    This will execute the `query` on the `database` using AWS Athena,
    and return the result as a pandas DataFrame.
    The DataFrame will contain all rows from the `mytable` table where
    the `category` column is 'books' and the `price` column is greater than 10.
    """

    return wr.athena.read_sql_query(sql=query, database=database)


def save_data(
    df: pd.DataFrame, path: str, test_size: float, random_state: int = 42
) -> None:
    """
    Split a pandas DataFrame into training and testing sets, and save them
    to disk as parquet files.

    Parameters
    ----------
    `df` : pd.DataFrame
        The input DataFrame to split into training and testing sets.
    `path` : str
        The path to save the parquet files to.
    `test_size` : float
        The proportion of the input DataFrame to use for testing.
        Must be between 0 and 1.
    `random_state` : int, optional (default=42)
        The random seed to use for splitting the data into training and testing sets.

    Returns
    -------
    None

    Raises
    ------
    `ValueError`
        If the `test_size` parameter is not between 0 and 1.

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.read_csv('data.csv')
    >>> save_data(df, 'data', test_size=0.2, random_state=123)

    This will split the `df` DataFrame into training and testing sets,
    with 20% of the data used for testing.
    The resulting parquet files will be saved in a directory called 'data'
    at the current working directory.
    """

    train, test = train_test_split(df, test_size=test_size, random_state=random_state)
    path_ = Path(path)
    if not path_.exists():
        path_.mkdir(parents=True, exist_ok=True)

    train.to_parquet(os.path.join(path, "train.parquet"), index=False)
    test.to_parquet(os.path.join(path, "test.parquet"), index=False)


def main(args: argparse.Namespace):
    """
    Execute the main functionality of this script.

    This function reads an SQL query from a file called 'data.sql',
    executes the query on an AWS Athena database,splits the resulting DataFrame
    into training and testing sets, and saves the sets as parquet files.

    Parameters
    ----------
    `args` : argparse.Namespace
        An `argparse.Namespace` object containing the command-line arguments
        passed to this script.

    Returns
    -------
    None

    Examples
    --------
    >>> import argparse
    >>> parser = argparse.ArgumentParser(description='My script')
    >>> parser.add_argument(
        '--database', type=str, help='The name of the Athena database to query'
        )
    >>> parser.add_argument(
        '--data', type=str, help='The path to save the parquet files to'
        )
    >>> args = parser.parse_args()
    >>> main(args)

    This will execute the main functionality of the script using the command-line
    arguments passed to it.
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
