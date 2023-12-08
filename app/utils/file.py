import os
from typing_extensions import Buffer
import openpyxl
import pandas as pd

class FileUtils:
    async def read_to_pd(self, file_type: str, file: Buffer = None, path: str = None) -> pd.DataFrame:
        """
        Reads a file into a pandas dataframe. Generic implementation, finds file type automatically.
        """
        print(file_type)
        if (not file and not path) or (file and path):
            raise Exception("Either file or path must be provided")
        file = file or path
        extension = file_type.split(".")[-1]
        match extension:
            case "csv":
                return await self.read_csv_to_pd(file)
            case "xlsx":
                return await self.read_excel_to_pd(file)
            case "xls":
                return await self.read_excel_to_pd(file)
            case "xml":
                return await self.read_xml_to_pd(file)
            case _:
                raise Exception(f"Unsupported file type: {extension}")


    async def read_excel_to_pd(self, file: Buffer | str) -> pd.DataFrame: ##TODO: Surely this can be simplified
        df = pd.read_excel(file).fillna("")
        df.replace("",None,inplace=True)
        return df


    async def read_xml_to_pd(self, file: Buffer | str) -> pd.DataFrame:
        ##does it read csv? TODO:
        df = pd.read_xml(file).fillna("")
        df.replace("",None,inplace=True)
        return df

    async def read_csv_to_pd(self, file: Buffer | str) -> pd.DataFrame:
        df = pd.read_csv(file).fillna("")
        df.replace("",None,inplace=True)
        return df
    
    def get_excel_sheet_names(self, file: Buffer | str, data_source: str) -> list:
        # Check the file extension
        _, file_extension = os.path.splitext(data_source)

        if file_extension in ['.xlsx', '.xlsm', '.xltx', '.xltm']:
            # Use openpyxl for .xlsx files
            workbook = openpyxl.load_workbook(file, read_only=True, data_only=True)
            sheet_names = workbook.sheetnames
        elif file_extension in ['.xls', '.xlt', '.xla']:
            # Use xlrd for .xls files
            workbook = pd.ExcelFile(file)
            sheet_names = workbook.sheet_names
        else:
            raise ValueError("Unsupported file format")

        return sheet_names


    def get_file_extension(self, data_source: str) -> str:
        return os.path.splitext(data_source)[1]
