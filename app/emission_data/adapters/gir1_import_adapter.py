import pandas as pd
from app.utils.file import FileUtils


class GirImportAdapter:
    def __init__(self):
        self.files = FileUtils()

    async def prepare(self, path: str, **kwargs) -> pd.DataFrame:
        file_type = self.files.get_file_extension(path)
        df_data = await self.files.read_to_pd(path=path, file_type=file_type)
        df_data['pollutantId'] = 'CO2eq'
        df_data['source'] = "gir1"
        return df_data
