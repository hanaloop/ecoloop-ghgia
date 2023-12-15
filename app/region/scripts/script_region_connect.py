import asyncio
from app.database import get_connection
from app.iorgsites.service import IOrgSiteService
from tqdm import tqdm

async def main():
    db = get_connection()
    await db.connect()
    site_service = IOrgSiteService()
    sites = await site_service.fetch_some(where={"addressRegion": None, "structuredAddress": {"not": None}})
    for site in tqdm(sites, total=len(sites)):
        await site_service.connect_address(site)


if __name__ == "__main__":
    asyncio.run(main())
