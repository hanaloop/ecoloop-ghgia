import asyncio

from app.database import get_connection
from app.iorgsites.service import IOrgSiteService
from app.emission_data.service import IEmissionDataService
from tqdm import tqdm

##Temporary until we merge the relation services
async def main():
    db = get_connection()
    await db.connect()
    site_service = IOrgSiteService()
    emission_data_service = IEmissionDataService()
    emissions = await emission_data_service.fetch_many(where={"latitude": None, "longitude": None, "source": {"startswith": "calc:"}}, include={"site": True})
    for emission in tqdm(emissions, total=len(emissions)):
        emission.site = await site_service.fetch_one(where={"uid": emission.siteUid}, include={"addressRegion": True})
        if emission.site.longitude and emission.site.latitude:
            emission.latitude = emission.site.latitude
            emission.longitude = emission.site.longitude
        elif emission.site.addressRegion and emission.site.addressRegion.longitude and emission.site.addressRegion.latitude:
            emission.latitude = emission.site.addressRegion.latitude
            emission.longitude = emission.site.addressRegion.longitude
            emission.settings = {'coordinates': "matched from region's coordinates"}
        else:
            continue
        ##TODO: Now I am including manually the site here, but I need to figure out why the site was not connected in the other branch
        await emission_data_service.update(data={"latitude": emission.latitude, "longitude": emission.longitude}, where={"uid": emission.uid}) 


if __name__ == "__main__":
    asyncio.run(main())
