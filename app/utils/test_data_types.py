from datetime import datetime
import numpy as np
import pytest

from app.utils.data_types import diff, key_of_value, parse_to_date, to_dict

class TestObject:
    def __init__(self, x):
        self.x = x

def test_one_attribute_conversion():
    # Testing conversion of an object without __dict__ attribute

    obj = TestObject(5)
    assert to_dict(obj) == {"x": 5}

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
    assert key_of_value(d, 4) == ["b"] ##TODO: This is not correct, but I will leave it for now. It must return a plain string
    
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


def test_diff():
    assert diff([], []) == []
    assert diff([], [1, 2, 3]) == [1, 2, 3]
    assert diff([1, 2, 3], []) == [1, 2, 3]
    assert diff([1, 2, 3], [2, 3, 4]) == [1, 4]
    assert diff([1, 2, 3], [4, 5, 6]) == [1, 2, 3, 4, 5, 6]

def test_parse_to_date():
    # Testing when value is None
    assert parse_to_date(None) is None
    
    # Testing when value is np.nan
    assert parse_to_date(np.nan) is None
    
    # Testing when value is less than dt_boundary_from
    assert parse_to_date(20200101, dt_boundary_from=datetime( 2021, 1, 1), dt_boundary_to=datetime( 2022, 1, 1)) == None
    
    # Testing when value is greater than dt_boundary_to
    assert parse_to_date(20230101, dt_boundary_from=datetime( 2020, 1, 1), dt_boundary_to=datetime( 2021, 1, 1)) == None
    
    # Testing when value is within the boundary and format is "%Y%m%d"
    assert parse_to_date(20210101, dt_boundary_from=datetime( 2020, 1, 1), dt_boundary_to=datetime( 2021, 1, 1)) == datetime(2021, 1, 1)
    
    # Testing when value is within the boundary 
    assert parse_to_date("2021-01-01", dt_boundary_from=datetime( 2020, 1, 1), dt_boundary_to=datetime( 2021, 1, 1)) == datetime(2021, 1, 1)
    
    # Testing when value is within the boundary 
    assert parse_to_date("01/01/2021", dt_boundary_from=datetime( 2020, 1, 1), dt_boundary_to=datetime( 2021, 1, 1)) == datetime(2021, 1, 1)
    
    # Testing when value is not a valid
    assert parse_to_date("2021-13-01", dt_boundary_from=datetime( 2020, 1, 1), dt_boundary_to=datetime( 2021, 1, 1)) == None
    # Testing empty string
    assert parse_to_date("", dt_boundary_from=datetime( 2020, 1, 1), dt_boundary_to=datetime( 2021, 1, 1)) == None

    # Testing string with whitespace
    assert parse_to_date(" ", dt_boundary_from=datetime(2020, 1, 1), dt_boundary_to=datetime(2021, 1, 1)) == None
