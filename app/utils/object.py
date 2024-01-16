def list_of_objects_to_dict(objects):
    """
    Converts a list of objects to a list of dictionaries.

    Args:
        objects (list): A list of objects to be converted.

    Returns:
        list: A list of dictionaries representing the objects.
    """
    return [to_dict(d) for d in objects]

def to_dict(obj):
    """
    Convert an object to a dictionary.

    Args:
        obj: The object to convert.

    Returns:
        dict: The dictionary representation of the object.
    """
    d = obj.__dict__
    return {k: v for k, v in d.items() if v is not None and v != ""}
