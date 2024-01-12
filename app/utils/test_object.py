import pytest

from app.utils.data_types import to_dict

def test_object_with_attributes():
    # Test converting an object with attributes to a dictionary
    class MyClass:
        def __init__(self):
            self.attr1 = 10
            self.attr2 = "Hello"
    
    obj = MyClass()
    expected_dict = {"attr1": 10, "attr2": "Hello"}
    assert to_dict(obj) == expected_dict

def test_object_with_none_attributes():
    # Test converting an object with None attributes to a dictionary
    class MyClass:
        def __init__(self):
            self.attr1 = None
            self.attr2 = None
    
    obj = MyClass()
    expected_dict = { "attr1": None, "attr2": None }
    assert to_dict(obj) == expected_dict

def test_object_with_empty_string_attributes():
    # Test converting an object with empty string attributes to a dictionary
    class MyClass:
        def __init__(self):
            self.attr1 = ""
            self.attr2 = ""
    
    obj = MyClass()
    expected_dict = { "attr1": "", "attr2": "" }
    assert to_dict(obj) == expected_dict
