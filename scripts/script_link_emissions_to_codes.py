from app.code.service import CodeService
from app.database import get_connection
import asyncio

async def main():
    service = CodeService()
    db = get_connection()
    await db.connect()
    await service.link_emissions_to_codes()


if __name__ == "__main__":
    asyncio.run(main())
