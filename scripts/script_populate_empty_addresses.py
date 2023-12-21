import asyncio

import prisma
from tqdm import tqdm
from app.database import get_connection
from app.iorgsites.service import IOrgSiteService
from app.config.column_mapping import ipcc_to_gir

service = IOrgSiteService()
async def main():
    db = get_connection()
    await db.connect()
    sites = await db.iorgsite.query_raw(
        query = f"""
        SELECT *
        FROM "IOrgSite"
        WHERE "sectorIds" ~ ('(^|\s*,\s*)(' || array_to_string(ARRAY{list(ipcc_to_gir.keys())}::text[], '|') || ')(\s*,|$)') AND "structuredAddress" IS NULL;
        """
    )
    for site in tqdm(sites, total=len(sites)):
        await service.populate_single_address(site=site)

if __name__ == "__main__":
    asyncio.run(main())
