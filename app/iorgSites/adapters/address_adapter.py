import re
import numpy as np
import pandas as pd


def format_address_df(df: pd.DataFrame, address_col: str) -> pd.DataFrame:
    """_summary_
    Strips various non-functioning strings from the factory addresses
    """
    
    data_dicts = [obj.__dict__ for obj in df]# Convert objects to dictionaries
    factories = pd.DataFrame(data_dicts)  # Create DataFrame
    factories.replace(np.nan, None, inplace=True)
    factories[address_col] = factories[address_col].astype(str).apply(lambda x: re.sub(r'\(.*$', "", x))
    factories[address_col] = factories[address_col].astype(str).apply(lambda x: re.sub(r'\d+필지', "", x))
    factories[address_col] = factories[address_col].astype(str).apply(lambda x: re.sub(r"외\s*외|외\s*", "", x))
    factories[address_col] = factories[address_col].apply(lambda x: re.split(',', x)[0])
    return factories

def format_address_string(address: str) -> str:
    address = address.strip()
    address = re.sub(r'\(.*$', "", address)
    address = re.sub(r'\d+필지', "", address)
    address = re.sub(r"외\s*외|외\s*", "", address)
    address = re.split(',', address)[0]
    address = address.strip()
    return address
    