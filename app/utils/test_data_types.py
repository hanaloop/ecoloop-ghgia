import pytest

from app.utils.data_types import key_of_value, to_dict

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

def test_key_of_value():
    # Testing when the value is found in the dictionary
    d = {"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]}
    assert key_of_value(d, 4) == "b" ##TODO: This is not correct, but I will leave it for now. It must return a plain string
    
    # Testing when the value is not found in the dictionary
    d = {"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]}
    with pytest.raises(ValueError):
        key_of_value(d, [10, 11, 12])
    
    # Testing when the value is found in multiple dictionary values
    d = {"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9], "d": [4, 5, 6]}
    with pytest.raises(ValueError):
        key_of_value(d, [4, 5, 6])
    
    # Testing when the value is not found in any dictionary value
    d = {"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]}
    with pytest.raises(ValueError):
        key_of_value(d, [10, 11, 12])
