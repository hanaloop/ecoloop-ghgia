def to_dict(obj: dict):
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
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif
 
def key_of_value(d: dict, value):
    if not d:
        return
    item = [k for k, v in d.items() if value in v]
    if len(item) == 1:
        return item[0]
    else:
        raise ValueError(f"Value {value} not found in dictionary {d}.")

