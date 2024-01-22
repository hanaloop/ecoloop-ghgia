import asyncio
from app.database import get_connection
from app.emission_data.service import IEmissionDataService
from tqdm import tqdm
from app.iorgsites.service import IOrgSiteService
from app.region.service import RegionService

##TODO: Temporary, this needs to happen automatically when the emission is created, but prisma is not fetching the region in include for some reason
async def main():
    db = get_connection()
    await db.connect()
    emission_service = IEmissionDataService()
    region_service   = RegionService()
    site_service = IOrgSiteService()
    emissions = await emission_service.fetch_many(where={"region": None,"source":{"startswith": "calc:", "not": "orig:gir-db4"} })
    for emission in tqdm(emissions, total=len(emissions)):
            emission.site = await site_service.fetch_one(where={"uid": emission.siteUid}, include={"addressRegion": True})
            address_region_uid = emission.site.addressRegion.uid if emission.site.addressRegion else None
            await emission_service.update(data={"longitude": emission.site.longitude, "latitude": emission.site.latitude, 'regionName': emission.site.addressSubRegion, 'regionUid': address_region_uid}, where={"uid": emission.uid})

if __name__ == "__main__":
    asyncio.run(main())
