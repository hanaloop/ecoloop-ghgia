import asyncio
from app.database import get_connection
from app.importers.importer_emission_data import EmissionDataImporter
from app.emission_data.adapters.gir4_import_adapter import GirCategoryAdapter
##Careful! If you have already imported data you will get duplicates
async def main():
    adapter = GirCategoryAdapter()
    db = get_connection()
    await db.connect()
    importer = EmissionDataImporter()
    await importer.import_data("app/.seed_data/emission_data.gir4.import.xls")


if __name__ == "__main__":
    asyncio.run(main())
