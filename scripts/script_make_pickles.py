import asyncio
import pickle
from app.database import get_connection
from app.emission_data.adapters.gir1_import_adapter import GirImportAdapter 
from app.emission_data.adapters.gir4_import_adapter import GirCategoryAdapter
from app.iorgsites.service import IOrgSiteService

async def main():
    connection = get_connection()
    await connection.connect()
    importer_gir1 = GirImportAdapter()
    importer = GirCategoryAdapter()
    # data1 =  await importer.prepare(data_source="./test_data/emission_data.gir4.import.xls")
    # data =  await importer_gir1.prepare(path="./test_data/emission_data.gir1.import.csv")
    factory_data = await IOrgSiteService().prepare_data(path="./test_data/factoryOnData.xlsx")
    # with open('./test_data/adapter_gir1.pkl', 'wb') as handle:
    #     pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    # with open('./test_data/adapter_gir4.pkl', 'wb') as handle:
    #     pickle.dump(data1, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('./test_data/factory_data.pkl', 'wb') as handle:
        pickle.dump(factory_data, handle, protocol=pickle.HIGHEST_PROTOCOL)



if __name__ == "__main__":
    asyncio.run(main())
