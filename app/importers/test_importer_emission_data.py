import os
import pytest
import pytest_asyncio
from app.config.env_config import ENV_IS_GITHUB
from app.database import get_connection

from app.importers.importer_emission_data import EmissionDataImporter



@pytest.fixture
def obj():
    obj = EmissionDataImporter()  # Create an instance of your class here
    obj.adapters = {
        'adapter1': 'adapter1_instance',
        'adapter2': 'adapter2_instance',
        'adapter3': 'adapter3_instance'
    }
    return obj

@pytest_asyncio.fixture
async def setup_db(obj):
    test_db_url = os.getenv("TEST_DATABASE_URL")
    pytest.MonkeyPatch().setenv("DATABASE_URL", test_db_url)
    db_connection = get_connection()
    await db_connection.connect()
    yield
    await obj.delete_all()
    
    await db_connection.disconnect()

def test_adapter_found(obj):
    filepath = '/path/to/adapter1/file.txt'
    result = obj.get_adapter_from_file(filepath)
    assert result == 'adapter1_instance'

def test_adapter_not_found(obj):
    filepath = '/path/to/invalid/file.txt'
    result = obj.get_adapter_from_file(filepath)
    assert result is None

def test_adapter_not_found_in_file(obj):
    filepath = '/path/to/adapter4/file.txt'
    result = obj.get_adapter_from_file(filepath)
    assert result is None

@pytest.skipif(ENV_IS_GITHUB, reason="database not available on github actions env")
@pytest.mark.asyncio
async def test_import_file(obj, setup_db):
    filepath = './test_data/emission_data.gir1.import.csv'
    result = await obj.import_data(filepath)
    assert result
