import asyncio
from app.iorgsites.service import IOrgSiteService
from app.database import get_connection
async def main():
    connection = get_connection()
    await connection.connect()
    fe = IOrgSiteService()
    await fe.upload_iorgsites(path="./.seed_data/factoryOnData.xlsx", data_source="xlsx")

if __name__ == "__main__":
    asyncio.run(main())
