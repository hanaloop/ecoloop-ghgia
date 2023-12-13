import asyncio
from app.database import get_connection
from app.iorgsites.service import IOrgSiteService

service = IOrgSiteService()
async def main():
    db = get_connection()
    await db.connect()
    await service.update_relations_alt()

if __name__ == "__main__":
    asyncio.run(main())
