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
        self.previous_values = {'first': '', 'second': '', 'third': '', 'fourth': '', 'fifth':''}

    def __transform_category_value(self, value, previous_values): #TODO: Need to fix to remove spaces, and . at the end of values
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
            
            if value.isalpha():  # First level category
                previous_values['first'] = self.current_alpha
                result = str(self.current_alpha) + '.'
                # Increment the current alphabetical value for the next first level category
                self.current_alpha = str(int(self.current_alpha) + 1)
                return result
            elif value.startswith(tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZ')):  # Second level category
                previous_values['second'] = value.split('.')[0]
                return previous_values['first'] + '.' + previous_values['second']
            elif value.replace(" ","")[0].isdigit():  # Third level category or Fifth level
                # If the previous value is a lowercase letter, it's fifth level, else it's third level
                if previous_values['fourth'] and str(previous_values["fourth"]).isupper():
                    previous_values["fifth"] = value.split('.')[0]
                    return (previous_values['first'] + '.' + previous_values['second'] + '.' + 
                            previous_values['third'] + '.' + previous_values['fourth'] + '.' + previous_values['fifth'])
                elif previous_values['fourth'] and str(previous_values["fourth"]).islower()  and value[0] == " ":
                    previous_values['fifth'] = value.split('.')[0].strip()
                    return (previous_values['first'] + '.' + previous_values['second'] + '.' + 
                            previous_values['third'] + '.' + previous_values["fourth"] + "." + previous_values["fifth"])

                else:
                    previous_values['third'] = value.split('.')[0]
                    previous_values["fourth"] = ""
                    previous_values["fifth"] = ""
                    return (previous_values['first'] + '.' + previous_values['second'] + '.' + 
                            previous_values['third'])

            elif value[0].islower():  # Fourth level category
                previous_values['fourth'] = value.split('.')[0]
                return (previous_values['first'] + '.' + previous_values['second'] + 
                        '.' + previous_values['third'] + '.' + previous_values['fourth'])

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
        emission_data_df = emission_data_df.replace({np.nan: None})
        return emission_data_df
    
    async def prepare(self, data_source: str, buffer: Buffer = None, path: str = None) -> pd.DataFrame:
        files = FileUtils()
        sheets = files.get_excel_sheet_names(buffer, data_source)
        emission_data_df = pd.DataFrame()
        for sheet in list(set(sheets) & set(SHEETS_TO_READ)):
            df = await files.read_to_pd("xlsx", buffer)
            df = await self.__process_data(df)
            df = await self.__prepare_for_db(df, sheet)
            emission_data_df = pd.concat([emission_data_df, df], ignore_index=True)
        return emission_data_df
            
        