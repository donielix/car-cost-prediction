from typing import Optional

import awswrangler as wr
import pandas as pd
from pyarrow import ArrowInvalid


def read_parquet_or_csv(path: str, sep: Optional[str] = None) -> pd.DataFrame:
    """
    Read data from either a Parquet file or a CSV file.

    Args
    ----
    - `path` (str): The path to the file to be read. If the path starts with "s3://",
                it is assumed to be an S3 object.
    - `sep` (str, optional): The delimiter used in the CSV file. Only applicable if
                            the file is in CSV format. Defaults to None.

    Returns
    -------
    - `pd.DataFrame`: A DataFrame containing the data from the file.

    Notes
    -----
    - If the file is located in an S3 bucket, the function attempts to read it as a
        Parquet file using the `wr.s3.read_parquet` function from the awswrangler
        library.
        If an ArrowInvalid exception occurs, it tries to read it as a CSV file using
        `wr.s3.read_csv` function.
    - If the file is a local file, it tries to read it as a Parquet file using the
        `pd.read_parquet` function. If an ArrowInvalid exception occurs, it tries to
        read it as a CSV file using `pd.read_csv` function.

    Examples
    --------
    >>> df = read_parquet_or_csv("data/file.parquet")
    >>> df = read_parquet_or_csv("data/file.csv", sep=",")
    >>> df = read_parquet_or_csv("s3://bucket/file.parquet")
    >>> df = read_parquet_or_csv("s3://bucket/file.csv", sep=",")

    """
    if path.startswith("s3://"):
        try:
            df = wr.s3.read_parquet(path)
        except ArrowInvalid:
            df = wr.s3.read_csv(path, sep=sep)
    else:
        try:
            df = pd.read_parquet(path)
        except ArrowInvalid:
            df = pd.read_csv(path, sep=sep)
    return df
