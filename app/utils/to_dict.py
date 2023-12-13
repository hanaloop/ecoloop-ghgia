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
