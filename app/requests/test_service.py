from aiolimiter import AsyncLimiter
import pytest
from httpx import Headers, QueryParams
from tqdm import tqdm
from app.iorgsites.service import RequestService
import time

TEST_COUNT = 20 ## Kind of arbitrary but the way test limiter works, it starts capping the speed after the limit has been hit. It then caps it to a degree that doesn't go over the limit for the rest of the time period i.e. slowly matching the required rpm

@pytest.fixture
def mock_client(mocker):
    # Mock the AsyncClient
    mock = mocker.patch('app.iorgsites.service.RequestService.request', return_value='Mocked Response')
    return mock

@pytest.mark.asyncio
async def test_request_method(mock_client):
    service = RequestService()
    service.rate_limit = AsyncLimiter(1, 1) ## 1 request per second, in case our limiter is set up differently
    response = await service.request('https://example.com', Headers(), QueryParams())
    assert response == 'Mocked Response'

@pytest.mark.asyncio
async def test_rate_limiting_behavior():
    service = RequestService()
    base_url = 'https://example.com'
    headers = Headers()
    params = QueryParams()
    curr_time = time.time()
    # Make multiple requests to trigger rate limiting
    for _ in tqdm(range(TEST_COUNT), total=TEST_COUNT):
        await service.request(base_url, headers, params)
    end_time = time.time()
    res_time = end_time - curr_time
    # print(f"Response time: {res_time}")
    # Check if actual rate matches the expected rate
    test_per_sec = TEST_COUNT / res_time
    assert test_per_sec == pytest.approx(service.rate_limit.max_rate / service.rate_limit.time_period, 0.2)

@pytest.mark.asyncio
async def test_error_handling_in_request_method(mock_client):
    mock_client.side_effect = Exception("Network Error")

    service = RequestService()
    with pytest.raises(Exception):
        await service.request('https://example.com', Headers(), QueryParams())
