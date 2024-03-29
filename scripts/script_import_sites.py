import asyncio
from app.foundation.arg_parse import parse_args
from app.iorgsites.service import IOrgSiteService
from app.database import get_connection

@parse_args
async def main(path: str):
    connection = get_connection()
    await connection.connect()
    fe = IOrgSiteService()
    await fe.upload_iorgsites(path=path)

if __name__ == "__main__":
    asyncio.run(main())

