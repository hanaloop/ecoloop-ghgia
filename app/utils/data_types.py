from datetime import datetime
import dateutil.parser
import numpy as np


def to_dict(obj: object):
    """
    Converts an objects attributes to a dictionary.
    
    Parameters:
        obj (dict): The object to be converted to a dictionary.
        
    Returns:
        dict: The converted dictionary.
    """
    obj = obj.__dict__
    if hasattr(obj, "__dict__"):
        return {k: v for k, v in obj.items() if v is not None and v != ""}

    else:
        return obj

def diff(li1, li2):
    """
    Calculates the difference (intersection) of two lists.

    Args:
        li1 (list): The first list.
        li2 (list): The second list.

    Returns:
        list: A list containing the elements that are present in either li1 or li2, but not in both.
    """
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif
 
def key_of_value(d: dict, value):
    """
    Returns the key associated with the given value in a dictionary.

    Parameters:
        d (dict): The dictionary to search.
        value: The value to find the key for.

    Returns:
        The key associated with the given value.

    Raises:
        ValueError: If the value is not found in the dictionary, or if multiple keys are associated with the value.
    """
    if not d:
        return
    item = [k for k, v in d.items() if value in v]
    if len(item):
        return item
    else:
        raise ValueError(f"Value {value} not found in dictionary {d}.")


from typing import Optional, Union
import numpy as np
import dateutil.parser
from datetime import datetime

def parse_to_date(
    value: Union[str, datetime, None],
    intended_format: str = "%Y%m%d",
    dt_boundary_from: Optional[datetime] = None,
    dt_boundary_to: Optional[datetime] = None
) -> Optional[datetime]:
    try:
        if isinstance(value, datetime):
            if dt_boundary_from is not None and dt_boundary_to is not None:
                if dt_boundary_from > dt_boundary_to:
                    raise ValueError("dt_boundary_from must be less than or equal to dt_boundary_to.")
                if dt_boundary_from <= value <= dt_boundary_to:
                    return value
                return None
            return value
        
        if not isinstance(value, str) and (value is None or np.isnan(value)):
            return None
        
        if isinstance(value, str) and value.strip() == "":
            return None

        if dt_boundary_from is not None and dt_boundary_to is not None:
            if dt_boundary_from > dt_boundary_to:
                raise ValueError("dt_boundary_from must be less than or equal to dt_boundary_to.")
            _date = dateutil.parser.parse(str(value))
            if dt_boundary_from <= _date <= dt_boundary_to:
                return _date
            return None
        
        _date = dateutil.parser.parse(str(value))
        return _date
    except ValueError:
        return None


def try_cast(value, type: type)-> bool:
    """
    A function that tries to cast a given value to a specified type.

    Parameters:
        value (Any): The value to be casted.
        type (type): The type to cast the value to.

    Returns:
        bool: True if the value can be casted to the specified type, False otherwise.
    """
    try:
        type(value)
        return True
    except:
        return False
