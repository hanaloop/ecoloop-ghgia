import asyncio
from app.database import get_connection
from app.importers.importer_emission_data import EmissionDataImporter
from app.foundation.arg_parse import parse_args

@parse_args
async def main(path: str):
    db = get_connection()
    await db.connect()
    importer = EmissionDataImporter()
    await importer.import_data(path)


if __name__ == "__main__":
    asyncio.run(main())
