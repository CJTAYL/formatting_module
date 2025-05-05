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
    "CHARLOTTE ": "CHARLOTTE - MERIDIAN",
    "SUCURSAL MERIDIAN": "CHARLOTTE - MERIDIAN",
    "MERIDIAN": "CHARLOTTE - MERIDIAN",
    "MERIDIAN ": "CHARLOTTE - MERIDIAN",
    "BRANCH MERIDIAN": "CHARLOTTE - MERIDIAN",
    "CHARLOTTE MERIDIAN": "CHARLOTTE - MERIDIAN",
    "VISTA DRIVE": "CHARLOTTE - MERIDIAN",
    "VISTA DRIVE 180": "CHARLOTTE - MERIDIAN",
    "2510 VISTA DR ": "CHARLOTTE - MERIDIAN",
    "2510 VISTA DR": "CHARLOTTE - MERIDIAN",
    "MARIDIAN": "CHARLOTTE - MERIDIAN",
    "VISTA DR": "CHARLOTTE - MERIDIAN",
    
    "702": "CHARLOTTE - UNIVERSITY CITY",
    "UNIVERSITY CITY": "CHARLOTTE - UNIVERSITY CITY",
    "UNIVERSITY CITY ": "CHARLOTTE - UNIVERSITY CITY",
    "UNIVERSITY": "CHARLOTTE - UNIVERSITY CITY",
    "UNIVERSITY ": "CHARLOTTE - UNIVERSITY CITY",
    "UNIVESITY CITY": "CHARLOTTE - UNIVERSITY CITY",
    "8601 UNIVERSITY CITY BLVD, CHARLOTTE, NC 28213": "CHARLOTTE - UNIVERSITY CITY", 
    "UNIVERSTY CITY": "CHARLOTTE - UNIVERSITY CITY",
    
    "SOUTH BOULEVARD": "CHARLOTTE - S. BLVD",
    "SOUTH BLV": "CHARLOTTE - S. BLVD",
    "SOUTH BLVD": "CHARLOTTE - S. BLVD",
    "SOUTH BOULEVARD ": "CHARLOTTE - S. BLVD",
    "5910 SOUTH BVLD": "CHARLOTTE - S. BLVD",
    "5910 SOUTH BLVD": "CHARLOTTE - S. BLVD",
    "SOUTH BULVD": "CHARLOTTE - S. BLVD",
    "SOUTH BLV ": "CHARLOTTE - S. BLVD",
    
    "703": "GREENSBORO - W. MARKET",
    "WEST GATE GREENSBORO": "GREENSBORO - WEST MARKET",
    "WEST MARKET GREENSBORO": "GREENSBORO - WEST MARKET",
    "W MARKET GREENSBORO": "GREENSBORO - WEST MARKET",
    "GREENSBORO - W. MARKET": "GREENSBORO - WEST MARKET",
    "106 MUIRS CHAPEL RD, GREENSBORO, NC 27410": "GREENSBORO - WEST MARKET",
    
    "704": "FAYETTEVILLE",
    "FAYETTEVILLE ": "FAYETTEVILLE",
    "FALLETEVIYE ": "FAYETTEVILLE",
    
    "705": "GREENSBORO - W. GATE",
    "GREENSBORO W GATE": "GREENSBORO - W. GATE",
    
    "708": "CHARLOTTE - MILTON",
    "MILTON": "CHARLOTTE - MILTON",
    "MILTON ": "CHARLOTTE - MILTON",
    "MILTO": "CHARLOTTE - MILTON",
    "CHARLOTTE MILTON": "CHARLOTTE - MILTON",
    "MILTON ROAD": "CHARLOTTE - MILTON",
    "MILTONT": "CHARLOTTE - MILTON",
    "MILTON RD ": "CHARLOTTE - MILTON",
    
    "714": "WINSTON-SALEM",
    "WINSTON SALEM": "WINSTON-SALEM",
    "1608 S STRATFORD RD, WINSTON SALEM": "WINSTON-SALEM",
    
    "717": "DURHAM",
    "BRANCH 717": "DURHAM",
    "DURHAM ": "DURHAM",
    "DURHAM NC": "DURHAM",
    "DOWNTOWN DURHAM": "DURHAM",
    "DOWNTOWN": "DURHAM",
    "DURHAN": "DURHAM",
    "DURHAM DOWNTOWN": "DURHAM",
    "DURHAM DOWNTOWN ": "DURHAM",
    "MORGAN STREET ": "DURHAM",
    
    "720": "OPERATIONS",
    
    "721": "VIRTUAL CENTER (Raleigh)",
    
    "737": "RALEIGH",
    "RALEIGH, NC": "RALEIGH",
    "RALEIGH , NC": "RALEIGH",
    "RALEIGH / MSC": "RALEIGH",
    "CAPITAL VOULEVAR": "RALEIGH",
    "CAPITAL BOULEVAR": "RALEIGH",
    "RALEIGH ": "RALEIGH",
    "CAPITAL BOULEVAR ": "RALEIGH",
    
    "747": "GARNER",
    "GARNER ": "GARNER",
    
    "751": "CHARLOTTE - MONROE",
    "MONROE ": "CHARLOTTE - MONROE",
    "6317 MONROE RD CHARLOTTE NC 28212": "CHARLOTTE - MONROE",
    "6317 MONROE RD CHARLOTTE, NC 28212": "CHARLOTTE - MONROE",
    
    "777": "NORTH DURHAM",
    "NORTH ROXBORO": "NORTH DURHAM",
    "ROXBORO ST": "NORTH DURHAM",
    "ROXBORO ST DURHAM NC": "NORTH DURHAM",
    "ROXBORO ": "NORTH DURHAM",
    "NORTH DURHAM ": "NORTH DURHAM",
    "N ROXBRO": "NORTH DURHAM",
    
    "790": "CARRBORO",
    "CARBORO": "CARRBORO",
    "CARRBORO 790": "CARRBORO",
    
    "MSC": "MEMBER SERVICE CENTER",
    
    "HIGH POINT ": "HIGH POINT",
    
    "R43": "NA",
    "BURLINGTON": "NA",
    "MALL": "NA"
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

def update_col_names(df, col_names):
    """
    Standardize column names

    :param df: DataFrame to be edited
    :param col_names: list of column names
    :return: df with updated column names
    """
    df.columns = col_names
    return df


def uppercase_strings(df):
    """
    Convert all strings in DataFrame to uppercase
    """
    df = df.map(lambda x: x.upper() if isinstance(x, str) else x)
    return df


