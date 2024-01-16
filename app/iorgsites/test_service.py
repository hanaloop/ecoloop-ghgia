import hashlib
from unittest.mock import MagicMock
from app.config.env_config import ENV_IS_GITHUB
from app.database import get_connection
from app.iorgsites.service import IOrgSiteService
from app.isitecategoryrels.service import ISiteCategoryRelService
import pytest_asyncio
import pandas as pd 
import os
import pytest
import json
from unittest.mock import patch
from app.utils.file import FileUtils

file = FileUtils()
service = IOrgSiteService()
rel_service = ISiteCategoryRelService()
@pytest_asyncio.fixture
async def setup_db():
    test_db_url = os.getenv("TEST_DATABASE_URL")
    pytest.MonkeyPatch().setenv("DATABASE_URL", test_db_url)
    db_connection = get_connection()
    await db_connection.connect()
    yield   # This is where the test function will execute
    await service.delete_all()
    await rel_service.delete_all()
    await db_connection.disconnect()

# @pytest_asyncio.fixture
# async def cleanup_db(setup_db):
#     await service.delete_all()
     


def test_hash_row():
    # Testing for different combinations of values in the row
    row1 = pd.Series({
        "factoryManagementNumber": "12345",
        "companyName": "ABC Corp",
        "landAddress": "123 Main St"
    })
    expected1 = hashlib.sha256("12345ABC Corp123 Main St".encode()).hexdigest()
    assert service.hash_row(row1) == expected1
    row2 = pd.Series({
        "factoryManagementNumber": "67890",
        "companyName": "XYZ Corp",
        "landAddress": "456 Elm St"
    })
    expected2 = hashlib.sha256("67890XYZ Corp456 Elm St".encode()).hexdigest()
    assert service.hash_row(row2) == expected2

    # Testing for empty values in the row
    row3 = pd.Series({
        "factoryManagementNumber": "",
        "companyName": "",
        "landAddress": ""
    })
    expected3 = hashlib.sha256("".encode()).hexdigest()
    assert service.hash_row(row3) == expected3

    # Testing for row with None values
    row4 = pd.Series({
        "factoryManagementNumber": None,
        "companyName": None,
        "landAddress": None
    })
    expected4 = hashlib.sha256("NoneNoneNone".encode()).hexdigest()
    assert service.hash_row(row4) == expected4



@pytest.mark.asyncio
@pytest.mark.skipif(ENV_IS_GITHUB, reason="database not available on github actions env")
async def test_upload_iorgsites_path(setup_db):
    path = "test_data/factoryOnData.xlsx"
    data = await service.upload_iorgsites(path=path)
    assert len(data) == file.count_excel_rows(path, count_header=False)
    
@pytest.mark.skipif(ENV_IS_GITHUB, reason="database not available on github actions env")
def test_upload_iorgsites_buffer_and_path(setup_db):
    buffer = MagicMock()
    path = "./test_data/factoryOnData.xls"
    service.upload_iorgsites(buffer=buffer, path=path)

@pytest.mark.asyncio
@pytest.mark.skipif(ENV_IS_GITHUB, reason="database not available on github actions env")
async def test_upload_iorgsites_no_arguments(setup_db):
    service.upload_iorgsites()

@pytest.mark.skip("WIP")
@pytest.mark.asyncio
async def test_request_address_with_streetAddress():
    site = MagicMock()
    site.streetAddress = "서울특별시 강남구 역삼동"

    expected_request_addr = "서울특별시 강남구 역삼동"
    expected_query_params = {
        "query": "서울특별시 강남구 역삼동"
    }
    expected_response = MagicMock()
    expected_api_loc_response = {
        "meta": {
            "total_count": 0
        }
    }
    expected_region1 = "Region1"
    expected_region2 = "Region2"
    expected_address_detail = {
        "type": "auto_parsed"
    }
    expected_structured_address = "Region1|Region2"

    with patch('iorgsites.adapters.adapter_address.fix_address_string') as mock_fix_address_string:
            with patch('app.requests.service.RequestService.request') as mock_requests:
                mock_requests.request.return_value = expected_response
                expected_response.text.return_value = json.dumps(expected_api_loc_response)

                mock_fix_address_string.return_value = expected_request_addr

                mock_requests.request.assert_called_with(
                    "fake_url",
                    headers={"Authorization": "KakaoAK fake_key"},
                    params=expected_query_params
                )

                instance = IOrgSiteService()
                result = await instance.get_site_structured_address(site)

                assert result[0] == expected_structured_address
                assert result[1] == expected_address_detail

@pytest.mark.skip("WIP")
@pytest.mark.asyncio
async def test_request_address_with_landAddress():
    site = MagicMock()
    site.streetAddress = None
    site.landAddress = "경기도 성남시 분당구"

    expected_request_addr = "경기도 성남시 분당구"
    expected_query_params = {
        "query": "경기도 성남시 분당구"
    }
    expected_response = MagicMock()
    expected_api_loc_response = {
        "meta": {
            "total_count": 0
        }
    }
    expected_region1 = "Region1"
    expected_region2 = "Region2"
    expected_address_detail = {
        "type": "auto_parsed"
    }
    expected_structured_address = "Region1|Region2"

    with patch('prisma.api.fix_address_string') as mock_fix_address_string:
        with patch('prisma.api.KAKAO_API_KEY', "fake_key"):
            with patch('prisma.api.KAKAO_API_BURL', "fake_url"):
                with patch('prisma.api.requests') as mock_requests:
                    mock_requests.request.return_value = expected_response
                    expected_response.text.return_value = json.dumps(expected_api_loc_response)

                    mock_fix_address_string.return_value = expected_request_addr

                    mock_requests.request.assert_called_with(
                        "fake_url",
                        headers={"Authorization": "KakaoAK fake_key"},
                        params=expected_query_params
                    )

                    instance = IOrgSiteService()
                    result = await instance.get_site_structured_address(site)

                    assert result[0] == expected_structured_address
                    assert result[1] == expected_address_detail
