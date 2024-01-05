import asyncio
from app.code.service import CodeService
from app.database import get_connection
from app.foundation.arg_parse import parse_args

# @parse_args
async def main(path: str=".seed_data/code.ecoloop.import.csv"):
    db = get_connection()
    await db.connect()
    service = CodeService()
    await service.upload_data(path=path)


if __name__ == "__main__":
    asyncio.run(main())
