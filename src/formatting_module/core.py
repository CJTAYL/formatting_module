"""
Core module for formatting_module

Contains a series of functions for cleaning data
"""
import re
import pandas as pd

from typing import Sequence, Optional, Union
from pathlib import Path

branch_dict = {
    "0": "LATINO COMMUNITY CREDIT UNION",
    "701": "CHARLOTTE - MERIDIAN",
    "SUCURSAL MERIDIAN": "CHARLOTTE - MERIDIAN",
    "MERIDIAN": "CHARLOTTE - MERIDIAN",
    "BRANCH MERIDIAN": "CHARLOTTE - MERIDIAN",
    "VISTA DRIVE": "CHARLOTTE - MERIDIAN",
    "UNIVERSITY CITY": "CHARLOTTE - UNIVERSITY CITY",
    "SOUTH BOULEVARD": "CHARLOTTE - S. BLVD",
    "SOUTH BLVD": "CHARLOTTE - S. BLVD",
    "703": "GREENSBORO - W. MARKET",
    "WEST MARKET GREENSBORO": "GREENSBORO - WEST MARKET",
    "W MARKET GREENSBORO": "GREENSBORO - WEST MARKET",
    "704": "FAYETTEVILLE",
    "705": "GREENSBORO - W. GATE",
    "708": "CHARLOTTE - MILTON",
    "MILTON": "CHARLOTTE - MILTON",
    "MILTON ROAD": "CHARLOTTE - MILTON",
    "714": "WINSTON-SALEM",
    "717": "DURHAM",
    "DOWNTOWN DURHAM": "DURHAM",
    "DOWNTOWN": "DURHAM",
    "DURHAN": "DURHAM",
    "DURHAM DOWNTOWN": "DURHAM",
    "721": "VIRTUAL CENTER",
    "737": "RALEIGH",
    "RALEIGH, NC": "RALEIGH",
    "RALEIGH / MSC": "RALEIGH",
    "CAPITAL VOULEVAR": "RALEIGH",
    "747": "GARNER",
    "751": "CHARLOTTE - MONROE",
    "777": "NORTH DURHAM",
    "NORTH ROXBORO": "NORTH DURHAM",
    "ROXBORO ST": "NORTH DURHAM",
    "790": "CARRBORO",
    "CARBORO": "CARRBORO",
    "MSC": "MEMBER SERVICE CENTER"
}

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

    param df pd.DataFrame: input DataFrame to modify.
    param date_columns: columns to parse with pd.to_datetime.
    param int_columns :Columns to cast to pandas nullable Int64.
    param string_columns: columns to cast to pandas StringDtype.
    param float_columns: Columns to cast to float.
    returns pd.DataFrame: DataFrame (modified in-place) with new dtypes.
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


def format_currency(amount, symbol = "$", decimals = 2, thousands_sep = ","):
    """
    Format number as USD

    :param amount:
    :param symbol:
    :param decimals:
    :param thousands_sep:
    :return str: formatted number as string
    """
    sign = "-" if amount < 0 else ""
    # This does both the thousands‐sep and fixed‐width decimals for you:
    formatted = f"{abs(amount):,.{decimals}f}"
    return f"{sign}{symbol}{formatted}"


def format_phone_number(phone):
    """
    Format phone number into standard format

    param phone : string phone number to format
    returns phone: phone number with the format (XXX) XXX-XXXX or +1 (XXX) XXX-XXXX
    """
    if pd.isna(phone):
        return phone 
    digits = re.sub(r'\D', '', str(phone))
    if len(digits) == 10:
        return f'({digits[:3]}) {digits[3:6]}-{digits[6:]}'
    elif len(digits) == 11 and digits.startswith('1'):
        return f'({digits[1:4]}) {digits[4:7]}-{digits[7:]}'
    else:
        return phone


def map_branch(branch_name):
    """
    Update branch name based on incorrect inputs provided by members

    param branch_name: string input from member
    returns branch_name: string with corrected branch name where appropriate
    """
    if pd.notnull(branch_name) and branch_name in branch_dict:
        return branch_dict[branch_name]
    return branch_name

    
def uppercase_strings(df):
    """
    Convert all strings in DataFrame to uppercase
    """
    df = df.map(lambda x: x.upper() if isinstance(x, str) else x)
    return df


