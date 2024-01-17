import pandas as pd
from app.utils.data_types import key_of_value
from app.utils.file import FileUtils
from app.config.column_mapping import ipcc_to_gir_code


class GirImportAdapter:
    def __init__(self):
        self.files = FileUtils()

    async def prepare(self, path: str, **kwargs) -> pd.DataFrame:
        file_type = self.files.get_file_extension(path)
        df_data = await self.files.read_to_pd(path=path, file_type=file_type)
        df_data['pollutantId'] = 'CO2eq'
        df_data['source'] = "gir1"
        df_data["categoryName"] = df_data["categoryName"].apply(lambda x: key_of_value(ipcc_to_gir_code, x)[0] if x in ipcc_to_gir_code.values() else x)
        df_data.drop(["sid", "uid", "dateCreated", "dateModified", "emissionElec" ,"emissionSteam", "emissionOthers"] , axis=1, inplace=True)
        return df_data
