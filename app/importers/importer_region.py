import numpy as np
import prisma
from app.utils.file import FileUtils
from app.region.service import RegionService
from app.foundation.field_type_match import model_fields_into_type_map, cast_dict_to_types

service = RegionService()

class RegionImporter:
    async def import_data(self, filepath: str):
        """
        Imports data from a CSV file and creates multiple records in the service.

        Parameters:
            filepath (str): The path to the CSV file to import.

        Returns:
            None
        """
        model_types = model_fields_into_type_map(prisma.models.Region.model_fields)
        files = FileUtils()
        df_data = await files.read_to_pd(path=filepath, file_type="csv")
        df_data.replace(np.nan, None, inplace=True)
        dict_data = df_data.to_dict(orient="records")
        for row in dict_data:
            cast_dict_to_types(row, model_types)
        try:
            return await service.create_many(data=dict_data)
        except Exception as e:
            print(f'Error: row {row} failed. Perhaps it already exists. {e}')
