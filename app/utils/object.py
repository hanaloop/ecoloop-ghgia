def list_of_objects_to_dict(objects):
    return [to_dict(d) for d in objects]

def to_dict(obj):
    d = obj.__dict__
    return {k: v for k, v in d.items() if v is not None and v != ""}
