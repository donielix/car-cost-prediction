import grp
import os
import pwd
from functools import reduce
from pathlib import Path
from typing import Dict, Optional, Union

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


def get_folder_permissions(folder_path) -> str:
    """
    Retrieve the permissions of a specified folder.

    Args
    ----
    - `folder_path` (str): The path to the folder.

    Returns
    -------
    - `str`: The permissions of the folder in octal representation.

    Raises
    ------
    - `FileNotFoundError`: If the specified folder is not found.
    """
    return oct(os.stat(folder_path).st_mode)[-3:]


def get_owner_and_group_ids(directory_path: Union[str, Path]) -> Dict[str, str]:
    """
    Get the owner and group IDs of a directory.

    Args
    ----
    - `directory_path` (str or pathlib.Path): The path to the directory.

    Returns
    -------
    - `dict`: A dictionary containing the owner ID (str) and group ID (str)
    of the directory. If the directory does not exist, the values will be None.

    Raises:
        ValueError: If the directory does not exist.
    """
    # Convert the directory path to a Path object
    directory = Path(directory_path)

    # Check if the directory exists
    if directory.exists():
        # Retrieve the owner ID and group ID
        owner_uid = os.stat(directory).st_uid
        group_gid = os.stat(directory).st_gid
        try:
            owner_id = pwd.getpwuid(owner_uid).pw_name
        except KeyError:
            owner_id = str(owner_uid)
        try:
            group_id = grp.getgrgid(group_gid).gr_name
        except KeyError:
            group_id = str(group_gid)

        # Return a dictionary containing the owner ID and group ID
        return {"owner_id": owner_id, "group_id": group_id}

    else:
        # Handle the case when the directory does not exist
        raise ValueError("Directory does not exist.")
