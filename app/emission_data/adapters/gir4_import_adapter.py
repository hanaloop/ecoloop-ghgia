from typing_extensions import Buffer
import numpy as np
from app.config.column_mapping import emission_data_cols    
import datetime
import pandas as pd
from app.utils.file import FileUtils

SHEETS_TO_READ = ["CO2", "CH4"]

class GirCategoryAdapter:
    def __init__(self):
        self.current_alpha = "1"
        self.previous_values = {'level_1': '', 'level_2': '', 'level_3': '', 'level_4': '', 'level_5':''}

    
    def __reset(self):
        self.current_alpha = "1"
        self.previous_values = {'level_1': '', 'level_2': '', 'level_3': '', 'level_4': '', 'level_5':''}

    def __transform_category_value(self, value, previous_values):
            """_summary_
            It transforms the values in the gir table to match the IPCC codes, by matching the starting
            letters, characters to each level, and keeping track of the levels, i.e. A, B, C, D -> A.1 B.1 etc.
            Args:
                value (_type_): _description_
                previous_values (_type_): _description_

            Returns:
                dataframe: gir table dataframe formatted to IPCC codes
            """
            # Check if the value is not a string
            if not isinstance(value, str):
                return value
            
            if value.isalpha():  # level_1 level category
                previous_values['level_1'] = self.current_alpha
                result = str(self.current_alpha) + '.'
                # Increment the current alphabetical value for the next level_1 level category
                self.current_alpha = str(int(self.current_alpha) + 1)
                return result
            elif value.startswith(tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZ')):  # level_2 level category
                previous_values['level_2'] = value.split('.')[0]
                return previous_values['level_1'] + '.' + previous_values['level_2']
            elif value.replace(" ","")[0].isdigit():  # level_3 level category or level_5 level
                # If the previous value is a lowercase letter, it's level_5 level, else it's level_3 level
                if previous_values['level_4'] and str(previous_values["level_4"]).isupper():
                    previous_values["level_5"] = value.split('.')[0]
                    return (previous_values['level_1'] + '.' + previous_values['level_2'] + '.' + 
                            previous_values['level_3'] + '.' + previous_values['level_4'] + '.' + previous_values['level_5'])
                elif previous_values['level_4'] and str(previous_values["level_4"]).islower()  and value[0] == " ":
                    previous_values['level_5'] = value.split('.')[0].strip()
                    return (previous_values['level_1'] + '.' + previous_values['level_2'] + '.' + 
                            previous_values['level_3'] + '.' + previous_values["level_4"] + "." + previous_values["level_5"])

                else:
                    previous_values['level_3'] = value.split('.')[0]
                    previous_values["level_4"] = ""
                    previous_values["level_5"] = ""
                    return (previous_values['level_1'] + '.' + previous_values['level_2'] + '.' + 
                            previous_values['level_3'])

            elif value[0].islower():  # level_5 level category
                previous_values['level_4'] = value.split('.')[0]
                return (previous_values['level_1'] + '.' + previous_values['level_2'] + 
                        '.' + previous_values['level_3'] + '.' + previous_values['level_4'])

            else:
                return value

    async def __process_data(self, df:pd.DataFrame):
        """_summary_

        Args:
            df (pd.DataFrame): _description_

        Returns:
            dataframe: returns a dataframe by using the transform_category_value function to match
            the entries in the gir table with the categories.
        """
        df.drop(df.index[:2],inplace=True) #skipping rows that do not contain data
        df.drop(df.index[136:],inplace=True) #skipping columns that do not contain data
        # Apply the adjusted transformation
        df["분야·부문/연도"] = df["분야·부문/연도"].apply(lambda x: self.__transform_category_value(x, self.previous_values))
        self.__reset()
        return df

    async def __prepare_for_db(self, df:pd.DataFrame, sheet_name: str):
        """_summary_
        Formats the emission data dataframe
        Args:
            df (pd.DataFrame): _description_
            sheet_name (_type_): _description_

        Returns:
            dataframe: dataframe with formatted columns
        """

        emission_data_df = pd.DataFrame(columns=emission_data_cols)

        # Populate the emission_data_df using the data from sheet1_df
        for col in df.columns[1:]:  # Exclude the first column (categoryName)
            temp_df = pd.DataFrame()
            temp_df["categoryName"] = df["분야·부문/연도"]
            temp_df["emissionTotal"] = df[col]
            temp_df["pollutantId"] = sheet_name  # Name of the first sheet
            temp_df["periodStartDt"] = datetime.datetime(int(col), 1, 1)  # January of the year
            temp_df["periodEndDt"] = datetime.datetime(int(col), 12, 31)  # December of the year
            temp_df["source"] = "gir4"
            temp_df["periodLength"] = "1Y"
            emission_data_df = pd.concat([emission_data_df, temp_df], ignore_index=True)
        non_float_pattern = r'^(?!-?\d*\.\d*$).*$'
        emission_data_df["emissionTotal"] = emission_data_df["emissionTotal"].replace(non_float_pattern, None, regex=True)
        emission_data_df["emissionTotal"] = emission_data_df["emissionTotal"].astype(float)
        emission_data_df = emission_data_df.replace({np.nan: None})
        return emission_data_df
    
    async def prepare(self, data_source: str, buffer: Buffer = None, path: str = None) -> pd.DataFrame:
        files = FileUtils()
        sheets = files.get_excel_sheet_names(buffer or path, data_source)
        emission_data_df = pd.DataFrame()
        for sheet in list(set(sheets) & set(SHEETS_TO_READ)):
            df = await files.read_to_pd("xlsx", buffer or path, sheet= sheet)
            df = await self.__process_data(df)
            df = await self.__prepare_for_db(df, sheet)
            emission_data_df = pd.concat([emission_data_df, df], ignore_index=True)
        return emission_data_df
            
        
