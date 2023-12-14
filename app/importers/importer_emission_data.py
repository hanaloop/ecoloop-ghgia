import prisma
from tqdm import tqdm
from app.utils.file import FileUtils
from app.emission_data.service import IEmissionDataService
from app.foundation.field_type_match import match_to_types, sort_fields_by_inner_annotation
from app.emission_data.adapters.gir4_import_adapter import GirCategoryAdapter

service = IEmissionDataService()
adapters = GirCategoryAdapter()
class EmissionDataImporter:
    async def import_data(self, filepath: str, adapter=None):
        """
        Import data from a file and create new records in the service.

        Args:
            filepath (str): The path to the file containing the data.
            adapter (Adapter, optional): The adapter to use for the data. Defaults to None.

        Returns:
            None
        """
        adapter = adapters
        files = FileUtils()
        if not adapter: #TODO: Later select adapters accordingly
            file_type = files.get_file_extension(filepath)
            df_data = await files.read_to_pd(path=filepath, file_type=file_type)
        else :
            df_data = await adapters.prepare(path=filepath, data_source=filepath)
        data_format = sort_fields_by_inner_annotation(prisma.models.IEmissionData.model_fields)
        formatted_df = match_to_types(data=df_data, sorted_annotations=data_format)
        for row in tqdm(formatted_df.to_dict(orient="records"), total=len(formatted_df)):
            new_row = {key: value for key, value in row.items() if value is not None}
            await service.create(data=new_row)                                  
        