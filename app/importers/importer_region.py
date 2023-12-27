import numpy as np
import prisma
from app.utils.file import FileUtils
from app.region.service import RegionService
from app.foundation.field_type_match import sort_fields_by_inner_annotation, match_df_to_types

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
        model_types = sort_fields_by_inner_annotation(prisma.models.Region.model_fields)
        files = FileUtils()
        df_data = await files.read_to_pd(path=filepath, file_type="csv")
        df_data = match_df_to_types(sorted_annotations=model_types, data=df_data)
        df_data.replace(np.nan, None, inplace=True)
        dict_data = df_data.to_dict(orient="records")
        await service.create_many(data=dict_data)                    
