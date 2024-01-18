import asyncio
from app.database import get_connection
from app.foundation.arg_parse import parse_args
from app.importers.importer_ets_report import EtsReportImporter

@parse_args
async def main(path: str):
    connection = get_connection()
    await connection.connect()
    importer = EtsReportImporter()
    await importer.import_data(path)


if __name__ == "__main__":
    asyncio.run(main())
