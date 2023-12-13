import asyncio

from app.utils.file import FileUtils
from app.config.column_mapping import iorgsite_map
from app.iorgsites.service import IOrgSiteService

service = IOrgSiteService()

file = FileUtils()
async def main():
    test = await file.read_to_pd(path="app/.seed_data/factoryOnData.xlsx", file_type="xlsx")
    test.rename(columns=iorgsite_map, inplace=True)
    test['hash'] = test.apply(lambda row: service.hash_row(row), axis=1)
    newdf = test[test.duplicated('hash', keep=False)]
    newdf.to_excel("app/.seed_data/factoryOnDataDuplicate.xlsx")
    print(len(test))


if __name__ == "__main__":
    asyncio.run(main())
