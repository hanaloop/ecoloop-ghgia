import os
import pytest
import pytest_asyncio
from app.importers.importer_region import RegionImporter
from app.database import get_connection
from pytest_mock import MockerFixture
from app.config.env_config import ENV_IS_GITHUB
from app.region.service import RegionService

@pytest_asyncio.fixture
async def setup_db():
    test_db_url = os.getenv("TEST_DATABASE_URL")
    pytest.MonkeyPatch().setenv("DATABASE_URL", test_db_url)
    await get_connection().connect()
    yield   # This is where the test function will execute
    await RegionService().delete_all()
    await get_connection().disconnect()

@pytest.mark.asyncio
@pytest.mark.skipif(ENV_IS_GITHUB, reason="database not available on github actions env")
async def test_import_region(mocker: MockerFixture, setup_db):
    mocker.patch("app.region.service.RegionService.create_many", return_value=[])

    importer = RegionImporter()
    filepath = "test_data/region.csv"
    await importer.import_data(filepath)
    # Assert that service.create_many() was called
    assert RegionService().create_many.called ## pylint: disable=no-member

@pytest.mark.asyncio
@pytest.mark.skipif(ENV_IS_GITHUB, reason="database not available on github actions env")
async def test_import_region_intergration(setup_db):
    importer = RegionImporter()
    filepath = "test_data/region.csv"
    data = await importer.import_data(filepath)
    assert data
