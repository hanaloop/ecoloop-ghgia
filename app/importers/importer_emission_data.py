import prisma
from tqdm import tqdm
from app.utils.file import FileUtils
from app.emission_data.service import IEmissionDataService
from app.foundation.field_type_lister import match_to_types, sort_fields_by_inner_annotation

service = IEmissionDataService()

class EmissionDataImporter:
    async def import_data(self, filepath: str):
        """
        Import data from a file and create new records in the service.

        Args:
            filepath (str): The path to the file containing the data.

        Returns:
            None
        """
        files = FileUtils()
        df_data = await files.read_to_pd(path=filepath, file_type="csv")
        data_format = sort_fields_by_inner_annotation(prisma.models.IEmissionData.model_fields)
        formatted_df = match_to_types(data=df_data, sorted_annotations=data_format)
        for row in tqdm(formatted_df.to_dict(orient="records"), total=len(formatted_df)):
            new_row = {key: value for key, value in row.items() if value is not None}
            await service.create(data=new_row)                                  
        