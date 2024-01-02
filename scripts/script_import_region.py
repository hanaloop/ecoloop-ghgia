import asyncio

from app.database import get_connection
from app.foundation.arg_parse import parse_args
from app.importers.importer_region import RegionImporter

@parse_args
async def main(path:str):
    db = get_connection()
    await db.connect()
    importer = RegionImporter()
    await importer.import_data(path)


if __name__ == "__main__":
    asyncio.run(main())
