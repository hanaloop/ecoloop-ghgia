from typing_extensions import Buffer
import pandas as pd
from app.foundation.exception import CatchError
import magic 

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