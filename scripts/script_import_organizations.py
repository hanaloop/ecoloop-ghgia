import asyncio
from app.foundation.arg_parse import parse_args
from app.iorganizations.service import IOrganizationService
from app.database import get_connection

@parse_args
async def main(path: str):
    connection = get_connection()
    await connection.connect()
    fe = IOrganizationService()
    await fe.upload_organizations(path=path)

if __name__ == "__main__":
    asyncio.run(main())

