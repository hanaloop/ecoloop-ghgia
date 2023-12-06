from httpx import Headers, QueryParams
import httpx
from aiolimiter import AsyncLimiter

MAX_CALLS_PER_SECOND = 1
MAX_CALLS_PER_MINUTE = MAX_CALLS_PER_SECOND * 60
MAX_CALLS_PER_HOUR = MAX_CALLS_PER_MINUTE * 60
MAX_CALLS_PER_DAY = MAX_CALLS_PER_HOUR * 24
ONE_MINUTE = 60
ONE_HOUR = 60 * ONE_MINUTE  ##TODO: Make this env variable
ONE_DAY = 24 * ONE_HOUR

## Note on the limiter, up to max_rate acquisitions are allowed within the set time period in a burst.


class RequestService:
    def __init__(self) -> None:
        self.__client = httpx.AsyncClient()
        self.rate_limit = AsyncLimiter(MAX_CALLS_PER_SECOND, MAX_CALLS_PER_SECOND)

    async def __request__(self, base_url: str, headers: Headers, params: QueryParams):
        """
        Sends an asynchronous request to the specified base URL with the given headers and query parameters.

        Args:
            base_url (str): The base URL to send the request to.
            headers (Headers): The headers to include in the request.
            params (QueryParams): The query parameters to include in the request.

        Returns:
            The response object received from the request.
        """
        response = await self.__client.get(base_url, headers=headers, params=params)
        return response

    async def request(self, base_url: str, headers: Headers, params: QueryParams):
        """
        Send a request to the specified base URL with the provided headers and query parameters. Uses rate limiting.

        Args:
            base_url (str): The base URL for the request.
            headers (Headers): The headers to include in the request.
            params (QueryParams): The query parameters to include in the request.

        Returns:
            The response from the request.

        Raises:
            Any exceptions that may occur during the request.
        """
        async with self.rate_limit:
            response = await self.__request__(base_url, headers, params)
        return response
