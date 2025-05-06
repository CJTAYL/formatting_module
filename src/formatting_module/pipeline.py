from pathlib import Path
from typing import (
    Union, Sequence, Optional, List
)
import pandas as pd

from .io import read_data
from .core import (
    assign_dtypes,
    clean_whitespace,
    update_col_names,
    uppercase_strings,
    map_branch,
    format_phone_number,
    format_currency,
)

def run_pipeline(
    source: Union[str, Path, pd.DataFrame],
    *,
    date_columns: Optional[Sequence[str]]   = None,
    int_columns: Optional[Sequence[str]]    = None,
    string_columns: Optional[Sequence[str]] = None,
    float_columns: Optional[Sequence[str]]  = None,
    new_col_names: Optional[Sequence[str]]  = None,
    branch_column: Optional[str]           = None,
    phone_columns: Optional[Sequence[str]]  = None,
    currency_columns: Optional[Sequence[str]] = None,
    uppercase: bool = False,
) -> pd.DataFrame:
    """
    Run the full formatting pipeline on your data.

    param source : filepath (will use read_data) or already-loaded DataFrame.
    param date_columns: list of columns containing data with type date
    param int_columns: list of columns containing data with type integer
    param string_columns: list of columns containing data with type string
    param float_columns: list of columns containing data with type float
    param new_col_names: full list of column names to apply via update_col_names()
    param branch_column: if given, maps that column through map_branch()
    param phone_columns: List of columns to format with format_phone_number()
    param currency_columns: list of columns to format with format_currency()
    param uppercase: if True, uppercases all string cells
    return df: formatted DataFrame
    """
    # 1) load or copy
    if isinstance(source, (str, Path)):
        df = read_data(source)
    else:
        df = source.copy()

    # 2) cast dtypes
    df = assign_dtypes(
        df,
        date_columns=date_columns,
        int_columns=int_columns,
        string_columns=string_columns,
        float_columns=float_columns,
    )

    # 3) strip whitespaces 
    df = df.map(clean_whitespace)
    
    # 4) rename columns if requested
    if new_col_names is not None:
        df = update_col_names(df, new_col_names)

    # 5) uppercase all strings
    if uppercase:
        df = uppercase_strings(df)

    # 6) map branch names
    if branch_column and branch_column in df:
        df[branch_column] = df[branch_column].apply(map_branch)

    # 7) format phone numbers
    if phone_columns:
        for col in phone_columns:
            if col in df:
                df[col] = df[col].apply(format_phone_number)

    # 8) format currencies
    if currency_columns:
        for col in currency_columns:
            if col in df:
                df[col] = df[col].apply(format_currency)

    return df
