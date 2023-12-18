from typing import Any, Dict, List, Optional, TypedDict
from ipywidgets import HTML
from ipyleaflet import Rectangle
import numpy as np
import pandas as pd
import prisma
from sklearn.preprocessing import MinMaxScaler


class GroupData(TypedDict):
    name: str
    data: pd.DataFrame
    colour: str


class MapChartGroup:


    def __init__(self):
        self.data: Dict[str, Any] = {}
        self.group1: Dict[str, Any] = {"data": [],"name": ""}
        self.group2: Dict[str, Any] = {"data": [], "name": ""}
        self.group3: Dict[str, Any] = {"data": [], "name": ""}

    def add_to_group(self, data: pd.DataFrame, group_name: Optional[str] = None, bubble_message: str = "", colour: str = "#007BB8") -> None:
        """
        Adds data to a map chart group.

        Args:
            data: The data to be added.
            group_name: The name of the group. Defaults to None.

        Returns:
            None
        """
        class_variables = vars(self)

        for index, (var_name, var_value) in enumerate(class_variables.items()):
            if var_name == "data":
                continue
            if not len(var_value["data"]):
                group: List[Any] = []
                for relation in data.itertuples():
                    if relation.longitude is None or relation.latitude is None:
                        continue
                    
                    layer = MapChart(
                        y=float(relation.latitude),
                        x=float(relation.longitude),
                        first_bar=float(relation.norm),
                        colour= colour,
                    ).create_rect(x_offset=index * 0.01)
                    message = HTML()
                    message.value = bubble_message.format(**relation._asdict())
                    layer.popup = message
                    group.append(layer)
                var_value["data"] = group
                var_value["name"] = group_name
                break  # Break here to stop after filling the first None data

        # Update the self.data attribute with the filled data
        self.data = [
            self.group1.get("data"),
            self.group2.get("data"),
            self.group3.get("data"),
        ]

class MapChart:
    def __init__(self, x: float, y: float, first_bar: float = 0, colour: str = "blue") -> None:
        """
        Initialize the mapchart with the given coordinates and optional parameters.
        
        Parameters:
            x (float): The x-coordinate.
            y (float): The y-coordinate.
            first_bar (float, optional): The first bar value. Defaults to 0.
            colour (str, optional): The colour of the object. Defaults to "blue".
        """
        self.x = x
        self.y = y
        self.first_bar = first_bar
        self.colour = colour

    def create_rect(self, width: float=0.01, x_offset: float=0, y_offset: float=0) -> Rectangle:
        """
        Create a rectangle object.

        Args:
            width: The width of the rectangle (default: 0.01).
            x_offset: The x offset of the rectangle (default: 0).
            y_offset: The y offset of the rectangle (default: 0).

        Returns:
            A Rectangle object.

        """
        return Rectangle(
            bounds=(
                (self.y + y_offset, self.x + x_offset),
                (self.y + (self.first_bar), self.x + width + x_offset),
            ),
            weight=1,
            fill=True,
            fill_color=self.colour,
            fill_opacity=1,
        )

class MapDefs:
    def __init__(self, scaler: MinMaxScaler = None) -> None:
        self.scaler = scaler

    def single(self, data: pd.DataFrame | List, scale: bool = True, bubble_message: str = "", colour: str = "#007BB8") -> List[MapChart]:
        """
        create an layer of objects on a map. This will contain only one set of data

        Args:
            data (pd.DataFrame | List): The data to be used for generating the MapChart objects. It can be either a pandas DataFrame or a list.
            scale (bool, optional): Whether to scale the data. Defaults to True.
            bubble_message (str, optional): The message to be displayed in the bubble popup. Defaults to "".
            colour (str, optional): The color of the MapChart objects. Defaults to "#007BB8".

        Returns:
            List[MapChart]: A list of MapChart objects representing the generated MapCharts.
        """
        layers = []
        df = pd.DataFrame.from_records(data) if type(data) != pd.DataFrame else data
        if scale:
            df["norm"] = self.scaler.fit_transform(df[["emissionTotal"]])
        # try:
        #     relations_df["addressDetail"] = relations_df["addressDetail"].apply(json.loads)
        # except:
        #     pass
        for idx, item in df.iterrows():
            if (
                item.longitude is None
                or item.latitude is None
            ):
                continue
            layer = MapChart(
                y= float(item.latitude),
                x= float(item.longitude),
                first_bar= float(item.norm),
                colour= colour,
            ).create_rect()
            message = HTML()
            item_text = pd.Series.to_dict(item)
            message.value = bubble_message.format(**item_text)
            layer.popup = message
            layers.append(layer)

        return layers
    
    def group(self, data: list[GroupData],  chart_group: MapChartGroup,  reference_data_name: str, reference_value_name : str,  bubble_message: str = "") -> List[MapChart]:
        """
        create an layer of objects on a map. This will contain multiple sets of data

        Args:
            data (list[GroupData]): The data to be used for generating the MapChart objects.
            chart_group (MapChartGroup): The MapChartGroup object to add the MapChart objects to.
            reference_data_name (str): The name of the data that the rest of the data will be fitted on.
            reference_value_name (str): The name of the value that will be used for fitting.
            bubble_message (str, optional): The message to be displayed in the bubble popup. Defaults to "".

        Returns:
            List[MapChart]: A list of MapChart objects representing the generated MapCharts.
        NOTE: Currently, the reference_data_name (the data that the rest will be fitted on) must be first in the passed dict
        """
        for group_data in data:
            if group_data["name"] == reference_data_name:
                chart_group.add_to_group(self.__prepare_data__(group_data["data"], fit=True, reference_value_name=reference_value_name), group_data["name"], colour=group_data["colour"], bubble_message=bubble_message)
            else:
                chart_group.add_to_group(self.__prepare_data__(group_data["data"], fit=False, reference_value_name=reference_value_name), group_data["data"], colour=group_data["colour"], bubble_message=bubble_message)
            

    def __prepare_data__(self, data: List, fit=True, reference_value_name: str = None):
        """
        Prepare the data for modeling.

        Args:
            data (List): The input data.
            fit (bool, optional): Whether to fit the scaler. Defaults to True.
            reference_value_name (str, optional): The name of the reference value. Defaults to None.

        Returns:
            pd.DataFrame: The prepared data.
        """
        df = pd.DataFrame.from_records(data=data)
        if fit:
            df["norm"] = self.scaler.fit_transform(df[reference_value_name].values[:, None])
        else:
            df["norm"] = self.scaler.transform(df[reference_value_name].values[:, None])
        return df
