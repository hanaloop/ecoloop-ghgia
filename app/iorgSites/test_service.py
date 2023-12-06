import hashlib
from database import get_connection
from iorgsites.service import IOrgSiteService
import pytest_asyncio
import pandas as pd 

service = IOrgSiteService()
@pytest_asyncio.fixture
async def setup_db():
    db_connection = get_connection()
    await db_connection.connect()
    yield   # This is where the test function will execute
    await db_connection.disconnect()

@pytest_asyncio.fixture
async def cleanup_db(setup_db):
    await service.delete_all()
     


def test_hash_row():
    # Testing for different combinations of values in the row
    row1 = pd.Series({
        "businessRegistrationNum": "12345",
        "companyName": "ABC Corp",
        "landAddress": "123 Main St"
    })
    expected1 = hashlib.sha256("12345ABC Corp123 Main St".encode()).hexdigest()
    assert service.hash_row(row1) == expected1
    row2 = pd.Series({
        "businessRegistrationNum": "67890",
        "companyName": "XYZ Corp",
        "landAddress": "456 Elm St"
    })
    expected2 = hashlib.sha256("67890XYZ Corp456 Elm St".encode()).hexdigest()
    assert service.hash_row(row2) == expected2

    # Testing for empty values in the row
    row3 = pd.Series({
        "businessRegistrationNum": "",
        "companyName": "",
        "landAddress": ""
    })
    expected3 = hashlib.sha256("".encode()).hexdigest()
    assert service.hash_row(row3) == expected3

    # Testing for row with None values
    row4 = pd.Series({
        "businessRegistrationNum": None,
        "companyName": None,
        "landAddress": None
    })
    expected4 = hashlib.sha256("NoneNoneNone".encode()).hexdigest()
    assert service.hash_row(row4) == expected4
