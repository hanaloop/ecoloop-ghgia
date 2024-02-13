import asyncio
import pickle
from app.database import get_connection
from app.emission_data.adapters.gir1_import_adapter import GirImportAdapter 
from app.emission_data.adapters.gir4_import_adapter import GirCategoryAdapter
from app.iorgsites.service import IOrgSiteService


to_pickle = [{
    "location":"./test_data/emission_data.gir1.import.csv",
    "importer":GirImportAdapter() },{
    "location":"./test_data/emission_data.gir4.import.xls"
    ,"importer":GirCategoryAdapter()},
    {"location":"./test_data/factoryOnData.xlsx",
    "importer":IOrgSiteService()}]
async def main():
    connection = get_connection()
    await connection.connect()
    for data in to_pickle:
        importer = data["importer"]
        data =  await importer.prepare(data["location"])
        with open(f'./test_data/{importer.__class__.__name__}.pkl', 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    asyncio.run(main())
