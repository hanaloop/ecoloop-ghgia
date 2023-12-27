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
    if len(item) == 1:
        return item[0]
    else:
        raise ValueError(f"Value {value} not found in dictionary {d}.")

