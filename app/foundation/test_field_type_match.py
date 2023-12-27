import datetime
from typing import Union
import pandas as pd
import numpy as np
from app.foundation.field_type_match import match_df_to_types, match_dict_to_types, sort_fields_by_inner_annotation
from pydantic.fields import FieldInfo

def test_match_to_types():
    # Test converting columns to datetime
    data = pd.DataFrame({'col1': ['2021-01-01', '2022-01-01'], 'col2': ['2021-01-01', '2022-01-01']})
    sorted_annotations = {'datetime': ['col1', 'col2']}
    expected_result = pd.DataFrame({'col1': [pd.Timestamp('2021-01-01'), pd.Timestamp('2022-01-01')], 'col2': [pd.Timestamp('2021-01-01'), pd.Timestamp('2022-01-01')]})
    assert match_df_to_types(data, sorted_annotations).equals(expected_result)

    # Test converting columns to int
    data = pd.DataFrame({'col1': ['1', '2'], 'col2': ['3', '4']})
    sorted_annotations = {'int': ['col1', 'col2']}
    expected_result = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    assert match_df_to_types(data, sorted_annotations).equals(expected_result)

    # Test converting columns to float
    data = pd.DataFrame({'col1': ['1.1', '2.2'], 'col2': ['3.3', '4.4']})
    sorted_annotations = {'float': ['col1', 'col2']}
    expected_result = pd.DataFrame({'col1': [1.1, 2.2], 'col2': [3.3, 4.4]})
    assert match_df_to_types(data, sorted_annotations).equals(expected_result)

    # Test converting int to float
    data = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    sorted_annotations = {'float': ['col1', 'col2']}
    expected_result = pd.DataFrame({'col1': [1.0, 2.0], 'col2': [3.0, 4.0]})
    assert match_df_to_types(data, sorted_annotations).equals(expected_result)

    # Test converting columns to bool
    data = pd.DataFrame({'col1': ['True', 'False'], 'col2': ['True', 'False']})
    sorted_annotations = {'bool': ['col1', 'col2']}
    expected_result = pd.DataFrame({'col1': [True, False], 'col2': [True, False]})
    assert match_df_to_types(data, sorted_annotations).equals(expected_result)

    # Test converting columns to str
    data = pd.DataFrame({'col1': ['abc', 'def'], 'col2': ['ghi', 'jkl']})
    sorted_annotations = {'str': ['col1', 'col2']}
    expected_result = pd.DataFrame({'col1': ['abc', 'def'], 'col2': ['ghi', 'jkl']})
    assert match_df_to_types(data, sorted_annotations).equals(expected_result)

    # Test converting columns to Json
    data = pd.DataFrame({'col1': [np.nan, 'value'], 'col2': [np.nan, 'value']})
    sorted_annotations = {'Json': ['col1', 'col2']}
    expected_result = pd.DataFrame({'col1': ['{}', 'value'], 'col2': ['{}', 'value']})
    assert match_df_to_types(data, sorted_annotations).equals(expected_result)

    # Test converting columns to List
    data = pd.DataFrame({'col1': ['[1, 2, 3]', '[]'], 'col2': ['[4, 5, 6]', '[]']})
    sorted_annotations = {'List': ['col1', 'col2']}
    expected_result = pd.DataFrame({'col1': [[1, 2, 3], []], 'col2': [[4, 5, 6], []]})
    assert match_df_to_types(data, sorted_annotations).equals(expected_result)

    # Test converting columns to Dict
    data = pd.DataFrame({'col1': ['{"key1": "value1"}', '{}'], 'col2': ['{"key2": "value2"}', '{}']})
    sorted_annotations = {'Dict': ['col1', 'col2']}
    expected_result = pd.DataFrame({'col1': [{'key1': 'value1'}, {}], 'col2': [{'key2': 'value2'}, {}]})
    assert match_df_to_types(data, sorted_annotations).equals(expected_result)

    # Test converting Non nullable columns to string
    data = pd.DataFrame({'col1': [None, 'value'], 'col2': [None, 'value']})
    sorted_annotations = {'str': ['col1', 'col2']}
    expected_result = pd.DataFrame({'col1': ['', 'value'], 'col2': ['', 'value']})
    assert match_df_to_types(data, sorted_annotations).equals(expected_result)

    # Test np.Nan to string when not nullable
    data = pd.DataFrame({'col1': [np.NaN, 'value'], 'col2': [np.NaN, 'value']})
    sorted_annotations = {'str': ['col1', 'col2']}
    expected_result = pd.DataFrame({'col1': ['', 'value'], 'col2': ['', 'value']})
    assert match_df_to_types(data, sorted_annotations).equals(expected_result)

    #TODO: Test empty relationship list to None (whose names start with a capital letter)
    

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



def test_match_dict_to_types():
   # Test case 1: Testing conversion to int
   data = {'num': '10'}
   sorted_annotations = {'int': ['num']}
   expected_output = {'num': 10}
   assert match_dict_to_types(data, sorted_annotations) == expected_output

   # Test case 2: Testing conversion to float
   data = {'pi': '3.14'}
   sorted_annotations = {'float': ['pi']}
   expected_output = {'pi': 3.14}
   assert match_dict_to_types(data, sorted_annotations) == expected_output

   # Test case 3: Testing conversion to bool
   data = {'is_true': 'True'}
   sorted_annotations = {'bool': ['is_true']}
   expected_output = {'is_true': True}
   assert match_dict_to_types(data, sorted_annotations) == expected_output

   # Test case 4: Testing conversion to str
   data = {'name': 10}
   sorted_annotations = {'str': ['name']}
   expected_output = {'name': '10'}
   assert match_dict_to_types(data, sorted_annotations) == expected_output

   # Test case 5: Testing conversion to Json
   data = {'data': {'key': 'value'}}
   sorted_annotations = {'Json': ['data']}
   expected_output = {'data': '{"key": "value"}'}
   assert match_dict_to_types(data, sorted_annotations) == expected_output

   # Test case 6: Testing conversion to List
   data = {'list': '[1, 2, 3]'}
   sorted_annotations = {'List': ['list']}
   expected_output = {'list': [1, 2, 3]}
   assert match_dict_to_types(data, sorted_annotations) == expected_output

   # Test case 7: Testing conversion to Dict
   data = {'dict': "{'key': 'value'}"}
   sorted_annotations = {'Dict': ['dict']}
   expected_output = {'dict': {'key': 'value'}}
   assert match_dict_to_types(data, sorted_annotations) == expected_output
