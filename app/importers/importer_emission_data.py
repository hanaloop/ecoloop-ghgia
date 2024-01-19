import prisma
from tqdm import tqdm
from app.emission_data.adapters.gir4_import_adapter import GirCategoryAdapter
from app.emission_data.adapters.gir1_import_adapter import GirImportAdapter
from app.region.service import RegionService
from app.utils.file import FileUtils
from app.emission_data.service import IEmissionDataService
from app.foundation.field_type_match import cast_dict_to_types, model_fields_into_type_map

service = IEmissionDataService()
adapter_gir4 = GirCategoryAdapter()
adapter_gir1 = GirImportAdapter()
class EmissionDataImporter:
    def __init__(self):
        self.adapters = {
            "gir4": adapter_gir4,
            "gir1": adapter_gir1
        }
        self.region_service = RegionService()

    async def get_adapter(self, data_source: str):
        return self.adapters[data_source]


    def get_adapter_from_file(self, filepath: str):
        for data_source in self.adapters:
            if data_source in filepath:
                return self.adapters[data_source]
        return None
    
    async def import_data(self, filepath: str):
        """
        Import data from a file and create new records in the service.

        Args:
            filepath (str): The path to the file containing the data.
            adapter (Adapter, optional): The adapter to use for the data. Defaults to None.

        Returns:
            None
        """
        files = FileUtils()
        adapter = self.get_adapter_from_file(filepath)
        if not adapter: #TODO: Later select adapters accordingly
            file_type = files.get_file_extension(filepath)
            df_data = await files.read_to_pd(path=filepath, file_type=file_type)
        else :
            df_data = await adapter.prepare(path=filepath, data_source=filepath)
        data_format = model_fields_into_type_map(prisma.models.IEmissionData.model_fields)
        # df_data = df_data[df_data.columns.intersection(prisma.models.IEmissionData.model_fields.keys())]
        for row in tqdm(df_data.to_dict(orient="records"), total=len(df_data)):
            new_row = cast_dict_to_types(row, data_format)
            # new_row = {key: value for key, value in row.items() if value is not None}
            if new_row['regionUid']:
                region = await self.region_service.fetch_one(where={"uid": new_row["regionUid"]})
                new_row['latitude'] = region.latitude
                new_row['longitude'] = region.longitude
            try:
                await service.update_or_create(data=new_row, where={"source": new_row["source"], "categoryName": new_row["categoryName"], "periodStartDt": new_row["periodStartDt"], "periodEndDt": new_row["periodEndDt"], "pollutantId": new_row["pollutantId"], "regionName": new_row["regionName"]})
            except Exception as e:
                print(f'Error: row {new_row} failed. Perhaps it already exists. {e}')   
            finally:
                pass
        