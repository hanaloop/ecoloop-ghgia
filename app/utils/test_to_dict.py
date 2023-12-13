import pytest

from app.utils.to_dict import to_dict

def test_dict_conversion():
    # Testing conversion of an object with __dict__ attribute
    obj = {"key1": "value1", "key2": "value2"}
    assert to_dict(obj) == obj

def test_non_dict_conversion():
    # Testing conversion of an object without __dict__ attribute
    obj = "test"
    assert to_dict(obj) == obj

def test_empty_dict_conversion():
    # Testing conversion of an empty dictionary
    obj = {}
    assert to_dict(obj) == obj

def test_none_conversion():
    # Testing conversion of None
    obj = None
    assert to_dict(obj) == obj

def test_empty_string_conversion():
    # Testing conversion of an empty string
    obj = ""
    assert to_dict(obj) == obj

def test_object_with_list_conversion():
    # Testing conversion of an actual object with a list attribute
    class TestObject:
        def __init__(self, x):
            self.x = x
            self.list_attr = [1, 2, 3]

    obj = TestObject(5)
    assert to_dict(obj) == {"x": 5, "list_attr": [1, 2, 3]}
