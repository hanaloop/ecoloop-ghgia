import pytest
from app.utils.data_types import to_dict

def test_to_dict():
    # Testing conversion of an object with attributes to a dictionary
    obj1 = SomeClass()
    obj1.attr1 = "value1"
    obj1.attr2 = "value2"
    obj1.attr3 = None

    expected1 = {"attr1": "value1", "attr2": "value2"}
    assert to_dict(obj1) == expected1

    # Testing conversion of an object without attributes to a dictionary
    obj2 = SomeClass()
    expected2 = {}
    assert to_dict(obj2) == expected2

    # Testing conversion of a dictionary object to a dictionary
    obj3 = {"attr1": "value1", "attr2": "value2"}
    expected3 = {"attr1": "value1", "attr2": "value2"}
    assert to_dict(obj3) == expected3

    # Testing conversion of an object with attributes and empty values to a dictionary
    obj4 = SomeClass()
    obj4.attr1 = ""
    obj4.attr2 = "value2"
    obj4.attr3 = None

    expected4 = {"attr2": "value2"}
    assert to_dict(obj4) == expected4

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

