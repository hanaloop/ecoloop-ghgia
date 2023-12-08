import datetime
from typing import Union
import pandas as pd
import numpy as np
from app.foundation.field_type_lister import match_to_types, sort_fields_by_inner_annotation
from pydantic.fields import FieldInfo

def test_match_to_types():
    # Test converting columns to datetime
    data = pd.DataFrame({'col1': ['2021-01-01', '2022-01-01'], 'col2': ['2021-01-01', '2022-01-01']})
    sorted_annotations = {'datetime': ['col1', 'col2']}
    expected_result = pd.DataFrame({'col1': [pd.Timestamp('2021-01-01'), pd.Timestamp('2022-01-01')], 'col2': [pd.Timestamp('2021-01-01'), pd.Timestamp('2022-01-01')]})
    assert match_to_types(data, sorted_annotations).equals(expected_result)

    # Test converting columns to int
    data = pd.DataFrame({'col1': ['1', '2'], 'col2': ['3', '4']})
    sorted_annotations = {'int': ['col1', 'col2']}
    expected_result = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    assert match_to_types(data, sorted_annotations).equals(expected_result)

    # Test converting columns to float
    data = pd.DataFrame({'col1': ['1.1', '2.2'], 'col2': ['3.3', '4.4']})
    sorted_annotations = {'float': ['col1', 'col2']}
    expected_result = pd.DataFrame({'col1': [1.1, 2.2], 'col2': [3.3, 4.4]})
    assert match_to_types(data, sorted_annotations).equals(expected_result)

    # Test converting int to float
    data = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    sorted_annotations = {'float': ['col1', 'col2']}
    expected_result = pd.DataFrame({'col1': [1.0, 2.0], 'col2': [3.0, 4.0]})
    assert match_to_types(data, sorted_annotations).equals(expected_result)

    # Test converting columns to bool
    data = pd.DataFrame({'col1': ['True', 'False'], 'col2': ['True', 'False']})
    sorted_annotations = {'bool': ['col1', 'col2']}
    expected_result = pd.DataFrame({'col1': [True, False], 'col2': [True, False]})
    assert match_to_types(data, sorted_annotations).equals(expected_result)

    # Test converting columns to str
    data = pd.DataFrame({'col1': ['abc', 'def'], 'col2': ['ghi', 'jkl']})
    sorted_annotations = {'str': ['col1', 'col2']}
    expected_result = pd.DataFrame({'col1': ['abc', 'def'], 'col2': ['ghi', 'jkl']})
    assert match_to_types(data, sorted_annotations).equals(expected_result)

    # Test converting columns to Json
    data = pd.DataFrame({'col1': [np.nan, 'value'], 'col2': [np.nan, 'value']})
    sorted_annotations = {'Json': ['col1', 'col2']}
    expected_result = pd.DataFrame({'col1': ['{}', 'value'], 'col2': ['{}', 'value']})
    assert match_to_types(data, sorted_annotations).equals(expected_result)

    # Test converting columns to List
    data = pd.DataFrame({'col1': ['[1, 2, 3]', '[]'], 'col2': ['[4, 5, 6]', '[]']})
    sorted_annotations = {'List': ['col1', 'col2']}
    expected_result = pd.DataFrame({'col1': [[1, 2, 3], []], 'col2': [[4, 5, 6], []]})
    assert match_to_types(data, sorted_annotations).equals(expected_result)

    # Test converting columns to Dict
    data = pd.DataFrame({'col1': ['{"key1": "value1"}', '{}'], 'col2': ['{"key2": "value2"}', '{}']})
    sorted_annotations = {'Dict': ['col1', 'col2']}
    expected_result = pd.DataFrame({'col1': [{'key1': 'value1'}, {}], 'col2': [{'key2': 'value2'}, {}]})
    assert match_to_types(data, sorted_annotations).equals(expected_result)

    # Test converting Non nullable columns to string
    data = pd.DataFrame({'col1': [None, 'value'], 'col2': [None, 'value']})
    sorted_annotations = {'str': ['col1', 'col2']}
    expected_result = pd.DataFrame({'col1': ['', 'value'], 'col2': ['', 'value']})
    assert match_to_types(data, sorted_annotations).equals(expected_result)

    # Test np.Nan to string when not nullable
    data = pd.DataFrame({'col1': [np.NaN, 'value'], 'col2': [np.NaN, 'value']})
    sorted_annotations = {'str': ['col1', 'col2']}
    expected_result = pd.DataFrame({'col1': ['', 'value'], 'col2': ['', 'value']})
    assert match_to_types(data, sorted_annotations).equals(expected_result)


def test_sort_fields_by_inner_annotation():
    # Test case 1: Empty data
    data = {}
    assert sort_fields_by_inner_annotation(data) == {}

    # Test case 2: Single field with non-Union annotation
    data = {'field1': FieldInfo(annotation=str)}
    assert sort_fields_by_inner_annotation(data) == {'str': ['field1']}

    # Test case 3: Single field with Union annotation
    data = {'field1': FieldInfo(annotation=Union[str, int])}
    assert sort_fields_by_inner_annotation(data) == {'str': ['field1'], 'int': ['field1']}

    # Test case 4: Multiple fields with different annotations
    data = {
        'field1': FieldInfo(annotation=str),
        'field2': FieldInfo(annotation=int),
        'field3': FieldInfo(annotation=datetime.datetime)
    }
    assert sort_fields_by_inner_annotation(data) == {'str': ['field1'], 'int': ['field2'], 'datetime': ['field3']}