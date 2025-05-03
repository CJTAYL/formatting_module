import pandas as pd
from typing import Union
from pathlib import Path

def read_data(path: Union[str, Path], **kwargs):
    """
    Read data of different file types into a pandas DataFrame

    :param path: Path to file
    :param kwargs: Keyword arguments
    :return: pandas DataFrame
    """
    p = Path(path)
    ext = p.suffix.lower()

    if ext == ".csv":
        return pd.read_csv(path, **kwargs)
    elif ext == ".txt":
        return pd.read_csv(path, sep="\t", **kwargs)
    elif ext == {".xls", ".xlsx"}:
        return pd.read_excel(path, **kwargs)
    elif ext == ".json":
        return pd.read_json(path, **kwargs)
    elif ext in {".parquet", ".pq"}:
        return pd.read_parquet(path, **kwargs)
    elif ext in {".pickle", ".pkl"}:
        return pd.read_pickle(path, **kwargs)
    elif ext == ".feather":
        return pd.read_feather(path, **kwargs)
    elif ext in {".h5", ".hdf5"}:
        return pd.read_hdf(path, **kwargs)
    else:
        raise ValueError(f"Unrecognized file extension: {ext!r}")
