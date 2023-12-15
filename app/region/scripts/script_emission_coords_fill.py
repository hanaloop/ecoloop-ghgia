import asyncio
from app.database import get_connection
from app.emission_data.service import IEmissionDataService
from tqdm import tqdm
from app.iorgsites.service import IOrgSiteService
from app.region.service import RegionService
from app.utils.string import get_coords_from_detail

##TODO: Temporary, this needs to happen automatically when the emission is created, but prisma is not fetching the region in include for some reason
async def main():
    db = get_connection()
    await db.connect()
    emission_service = IEmissionDataService()
    region_service   = RegionService()
    site_service = IOrgSiteService()
    emissions = await emission_service.fetch_some(where={"longitude": None,"source":{"startswith": "calc:", "not": "gir4"} })
    for emission in tqdm(emissions, total=len(emissions)):
            emission.site = await site_service.fetch_one(where={"uid": emission.siteUid})
            await emission_service.update(data={"longitude": emission.site.longitude, "latitude": emission.site.latitude, 'regionName': emission.site.addressSubRegion}, where={"uid": emission.uid})

if __name__ == "__main__":
    asyncio.run(main())
