"""
Core module for formatting_module

Contains a series of functions for cleaning data
"""
import re
import pandas as pd

from typing import Sequence, Optional

def assign_dtypes(
    df: pd.DataFrame,
    *,
    date_columns: Optional[Sequence[str]]  = None,
    int_columns:  Optional[Sequence[str]]  = None,
    string_columns: Optional[Sequence[str]] = None,
    float_columns: Optional[Sequence[str]] = None
) -> pd.DataFrame:
    """
    Cast specified DataFrame columns to the given pandas dtypes.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame to modify.
    date_columns
        Columns to parse with pd.to_datetime.
    int_columns
        Columns to cast to pandas nullable Int64.
    string_columns
        Columns to cast to pandas StringDtype.
    float_columns
        Columns to cast to float.

    Returns
    -------
    pd.DataFrame
        The DataFrame (modified in-place) with new dtypes.
    """
    # Work on a copy if you don’t want to mutate the original:
    # df = df.copy()

    # 1) datetime columns
    if date_columns:
        for col in date_columns:
            if col in df:
                df[col] = pd.to_datetime(df[col], errors="coerce")

    # 2) integer columns
    if int_columns:
        for col in int_columns:
            if col in df:
                df[col] = df[col].astype("Int64")

    # 3) string columns
    if string_columns:
        for col in string_columns:
            if col in df:
                df[col] = df[col].astype("string")

    # 4) float columns
    if float_columns:
        for col in float_columns:
            if col in df:
                df[col] = df[col].astype(float)

    return df


def format_phone_number(phone):
    """
    Format phone number into standard format

    Parameters
    ----------
    phone : string
        Phone number to format

    Returns
    -------
    phone: string
        Phone number with the format (XXX) XXX-XXXX or +1 (XXX) XXX-XXXX
    """
    if pd.isna(phone):
        return phone
    if not isinstance(phone, str):
        raise TypeError(f'Expected a string, got {type(phone).__name__!r}')
    else:
        digits = re.sub(r'\D', '', phone)
        if len(digits) == 10:
            area, mid, last = digits[:3], digits[3:6], digits[6:]
            return f'({area}) {mid}-{last}'
        elif len(digits) == 11 and digits.startswith('1'):
            area, mid, last = digits[1:4], digits[4:7], digits[7:]
            return f'+1 ({area}) {mid}-{last}'
        else:
            raise ValueError(
                f'Cannot format phone number: expected 10 or 11 digits starting with 1 and got {len(digits)} digits'
            )
