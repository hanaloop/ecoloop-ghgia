import asyncio
import os
import pytest
import pytest_asyncio
from app.code.service import CodeService
from app.database import get_connection
from app.config.env_config import ENV_IS_GITHUB
service = CodeService()

@pytest_asyncio.fixture
async def setup_db():
    test_db_url = os.getenv("TEST_DATABASE_URL")
    pytest.MonkeyPatch().setenv("DATABASE_URL", test_db_url)
    db_connection = get_connection()
    await db_connection.connect()
    yield
    await db_connection.code.delete_many()
    
    await db_connection.disconnect()


@pytest.mark.asyncio
@pytest.mark.skipif(ENV_IS_GITHUB, reason="database not available on github actions env")
async def test_upload_data_with_path(setup_db):
    path = "./test_data/code.ecoloop.import.csv"
    data = await service.upload_data(path=path)
    assert data

@pytest.mark.asyncio
@pytest.mark.skipif(ENV_IS_GITHUB, reason="database not available on github actions env")
async def test_upload_data_with_no_data_source_or_buffer(setup_db):
    with pytest.raises(Exception):
        asyncio.run(service.upload_data())

@pytest.mark.asyncio
@pytest.mark.skipif(ENV_IS_GITHUB, reason="database not available on github actions env")
async def test_upload_data_with_no_path_or_buffer(setup_db):
    data_source = "web"
    with pytest.raises(Exception):
        asyncio.run(service.upload_data(data_source=data_source))
