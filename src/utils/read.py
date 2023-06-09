import os
from functools import reduce
from typing import Optional, Union

import awswrangler as wr
import pandas as pd
from pyarrow import ArrowInvalid


def read_parquet_or_csv(path: str, **kwargs) -> pd.DataFrame:
    """
    Read data from either a Parquet file or a CSV file.

    Args
    ----
    - `path` (str): The path to the file to be read. If the path starts with "s3://",
                it is assumed to be an S3 object.
    - `kwargs`: Those keyword arguments will be directly passed to `read_csv` or
                `read_parquet` corresponding methods.

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
            df = wr.s3.read_parquet(path, **kwargs)
        except ArrowInvalid:
            df = wr.s3.read_csv(path, **kwargs)
    else:
        try:
            df = pd.read_parquet(path, **kwargs)
        except ArrowInvalid:
            df = pd.read_csv(path, **kwargs)
    return df


def join_path(*paths: str, sep: Optional[str] = None) -> str:
    """
    Join multiple paths together using a specified separator.

    Args
    ----
    - `*paths` (str): One or more path strings to be joined.
    - `sep` (Optional[str]): Separator to be used for joining the paths.
    If not provided, the default system separator will be used.

    Returns
    -------
    - `str`: The joined path.

    Example
    -------
    >>> join_path('path', 'to', 'file.txt', sep='/')
    'path/to/file.txt'

    The `join_path` function takes multiple path strings and concatenates
    them using the specified separator `sep`. If `sep` is not provided,
    the default system separator (os.path.sep) will be used.

    The function utilizes an internal helper `_joint_two_paths` to join
    two paths at a time. It removes any trailing separators from the
    first path and any leading separators from the second path before joining
    them using the specified separator.

    Note
    ----
    The function relies on the `os.path.sep` attribute to determine
    the system separator. It is recommended to import the `os` module
    before using this function.
    """
    if sep is None:
        sep = os.path.sep
    n_sep = len(sep)

    def _joint_two_paths(path_1: Union[str, None], path_2: Union[str, None]) -> str:
        if path_1 is None:
            path_1 = ""
        if path_2 is None:
            path_2 = ""
        if path_1.endswith(sep):  # type: ignore
            path_1 = path_1[:-n_sep]
        if path_2.startswith(sep):  # type: ignore
            path_2 = path_2[n_sep:]
        if not path_1:
            return path_2
        if not path_2:
            return path_1
        return sep.join([path_1, path_2])  # type: ignore

    return reduce(_joint_two_paths, paths)
