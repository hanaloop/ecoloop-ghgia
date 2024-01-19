import datetime
import json
from typing import Union, Dict, List, get_args
from collections import defaultdict
import logging
import numpy as np
import pandas as pd
from pydantic.fields import FieldInfo
import ast
from app.utils.data_types import key_of_value, parse_to_date
from app.utils.data_types import diff 

DEFAULT_ANNOTATIONS = {
    "str": '',
    "int": 0,
    "float": 0.0,
    "bool": False,
    "List": None,
    "Dict": None,
    "datetime": datetime.datetime(1,1,1,1,1,1),
    
}

def model_fields_into_type_map(data: Dict[str, FieldInfo]) -> Dict[str, List[str]]: ##TODO: Use hashmap to modify fields instead
    """
    Returns a sorted list of fields by their inner annotation type. Used to get fields that are datetime objects, json etc. 
    in a prisma model.

    Args:
        data (Dict[str, FieldInfo]): A dictionary of field names and FieldInfo objects. Example: prisma.Region.model.fields

    Returns:
        Dict[str, List[str]]: A dictionary of annotation types and lists of field names.
    """
    sorted_fields = defaultdict(list)

    for field_name, field_info in data.items():
        annotation = field_info.annotation
        if annotation == 'children':
            continue
        # Check if the annotation is a Union
        if getattr(annotation, '__origin__', None) is Union:
            # Iterate over each type in the Union
            for inner_type in get_args(annotation):
                sorted_fields[inner_type.__name__].append(field_name)
        else:
            # Handle non-Union types
            sorted_fields[annotation.__name__].append(field_name)
    if "NoneType" in sorted_fields:
        sorted_fields["NoneType"] = diff(sorted_fields["NoneType"], list(data.keys()))

    # Sort fields within each annotation type
    for annotation_type in sorted_fields:
        sorted_fields[annotation_type].sort()

    return dict(sorted_fields)


def match_df_to_types(data: pd.DataFrame, sorted_annotations: Dict[str, List[str]]) -> pd.DataFrame: ##TODO: Update like below
    data = data.replace({np.nan: None})
    for annotation, columns in sorted_annotations.items():
        for column in columns:
            if column not in data.columns:
                continue

            try:
                if annotation == 'datetime':
                    data[column] = pd.to_datetime(data[column], format="ISO8601").replace({np.nan: None})
                elif annotation == 'int':
                    data[column] = data[column].apply(lambda x: int(x) if x is not None else 0)
                elif annotation == 'float':
                    data[column] = data[column].apply(lambda x: float(x) if x is not None else 0.0)
                elif annotation == 'bool':
                    data[column] = data[column].apply(lambda x: True if x == "True" else False if x == "False" else x if x is not None else None)
                elif annotation == 'str':
                    data[column] = data[column].apply(lambda x: str(x) if x is not None else '')
                elif annotation == 'Json':
                    data[column] = data[column].fillna('{}')
                elif annotation == 'List':
                    data[column] = data[column].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
                elif annotation == 'Dict':
                    data[column] = data[column].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else {})

                elif annotation == 'NoneType':
                    default_types = key_of_value(sorted_annotations, column)
                    index_of_none_type = default_types.index("NoneType")
                    default_type = default_types[1-index_of_none_type]
                    data[column] = data[column].fillna(np.nan).replace([np.nan], DEFAULT_ANNOTATIONS[default_type])

            except Exception as e:
                print(f"Error converting column {column} to {annotation}: {e}")

    return data

def cast_dict_to_types(data: dict, sorted_annotations: dict) -> dict:
    """
    Updates the values in the `data` dictionary according to the types specified in the `sorted_annotations` dictionary.

    Args:
        data (dict): The dictionary containing the data to be updated.
        sorted_annotations (dict): The dictionary specifying the types of the values in `data`.

    Returns:
        dict: The updated `data` dictionary. NOTE:This one works much better than the above, use this one if possible.
    """
    ##TODO: Move intersection and annotations to here
    for annotation in sorted_annotations.keys():
        for key, value in list(data.items()):
            if key not in sorted_annotations[annotation]:
                continue
            try:
                if annotation == 'NoneType':
                    default_types = key_of_value(sorted_annotations, key)
                    if default_types[0] == 'NoneType':
                        default_type = default_types[1]
                    else:
                        default_type = default_types[0]
                    if value is None or pd.isna(value):
                        data[key] = DEFAULT_ANNOTATIONS[default_type]
                        continue
                if annotation == 'datetime':
                    if value is not None:
                        data[key] = parse_to_date(value)
                elif annotation == 'int':
                    if value is not None:
                        data[key] = int(value)
                elif annotation == 'float':
                    if value is not None:
                        data[key] = float(value)
                elif annotation == 'bool':
                    if value is not None:
                        data[key] = True if value == "True" else False if value == "False" else value
                elif annotation == 'str':
                    if value is not None:
                        data[key] = str(value)
                elif annotation == 'Json':
                    if value is None:
                        data[key] = '{}'
                    else:
                        data[key] = json.dumps(value)
                elif annotation == 'List':
                    if isinstance(value, str):
                        data[key] = ast.literal_eval(value)
                    else:
                        del data[key]
                elif annotation == 'Dict':
                    if isinstance(value, str):
                        data[key] = ast.literal_eval(value)
                    else:
                        data[key] = {}
                elif annotation[0].isupper():
                    if value is None:
                        del data[key]

            except Exception as e:
                logging.debug(f"Could not cast value {value} to {annotation}: {e}")

    return data
