import asyncio
from app.database import get_connection
from app.importers.importer_emission_data import EmissionDataImporter

##Careful! If you have already imported data you will get duplicates
async def main():
    db = get_connection()
    await db.connect()
    importer = EmissionDataImporter()
    await importer.import_data("app/.seed_data/emission_data.ecoloop.import.csv")


if __name__ == "__main__":
    asyncio.run(main())
