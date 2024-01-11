import asyncio
from app.database import get_connection
from app.emission_data.service import IEmissionDataService
from app.foundation.arg_parse import parse_args

service = IEmissionDataService()

@parse_args
async def main(year_from: int=2020, year_to: int = 2021):
    db = get_connection()
    await db.connect()
    for year in range(year_from, year_to): ##Range is end exclusive, thus 2021 means until 2020
        await service.calc_emissions_dt_range(year=year)

if __name__ == "__main__":
    asyncio.run(main())
