def to_dict(obj: dict):
    if hasattr(obj, "__dict__"):
        return {k: v for k, v in obj.items() if v is not None and v != ""}

    else:
        return obj