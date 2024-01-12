import asyncio
from app.database import get_connection
from app.iorgsites.service import IOrgSiteService
from tqdm import tqdm

from app.utils.string import get_coords_from_detail

async def main():
    db = get_connection()
    await db.connect()
    site_service = IOrgSiteService()
    sites = await site_service.fetch_many(where={"longitude": None, "structuredAddress": {"not": None}})
    for site in tqdm(sites, total=len(sites)):
        latitude, longitude = get_coords_from_detail(site.addressDetails)
        await site_service.update(where={"uid": site.uid}, data= {"longitude": longitude, "latitude": latitude})


if __name__ == "__main__":
    asyncio.run(main())
