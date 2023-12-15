import re
import numpy as np
import pandas as pd


def format_address_df(df: pd.DataFrame, address_col: str) -> pd.DataFrame:
    """_summary_
    Strips various non-functioning strings from the factory addresses
    """
    
    data_dicts = [obj.__dict__ for obj in df]# Convert objects to dictionaries
    factories = pd.DataFrame(data_dicts)  # Create DataFrame
    factories.apply(lambda row: fix_address_string(row[address_col]), axis=1)
    return factories

def fix_address_string(address: str) -> str:
    address = address.strip()
    address = re.sub(r'\(.*$', "", address)
    address = re.sub(r'\d+필지', "", address)
    address = re.sub(r'\d+번지', "", address)  # Remove parts containing 번지
    address = re.sub(r'\d+필', "", address)    # Remove parts containing 필
    address = re.sub(r"외\s*외|외\s*", "", address)
    address = re.sub(r"[!@#$%^&*()_+={}\[\]:;<>,.?~\\-]", "", address)
    address = address.strip(",")
    address = address.strip()
    return address
