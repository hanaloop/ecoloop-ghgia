import asyncio

from app.database import get_connection
from app.importers.importer_region import RegionImporter
##Careful! If you have already imported data you will get duplicates
async def main():
    db = get_connection()
    await db.connect()
    importer = RegionImporter()
    await importer.import_data("app/.seed_data/region.ecoloop.import.csv")


if __name__ == "__main__":
    asyncio.run(main())