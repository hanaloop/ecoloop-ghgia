from deprecated import deprecated
import httpx

@deprecated(reason="Use httpx method instead")
def __construct_url(base_url_template: str, params: dict) -> str:
    """
    Constructs a URL using a base URL template and the instance variables of the class.

    Args:
        base_url_template (str): The base URL template to use for constructing the URL.

    Returns:
        string: returns a url string that can be used to fetch data from openDart


    Raises:
        None

    Examples:
        >>> obj = ClassName()
        >>> obj.construct_url("https://example.com/{file_name}")
        'https://example.com/filename?crtfc_key=key'

        Notes:
        The URL is constructed using the base URL template and the instance variables of the class.
        The necessary variables should be initialized when instantiating the class
    """
    first_part = base_url_template + "?" + params.items[0]
    query_string = first_part + "&".join(
        [f"{key}={value}" for key, value in params.items[1:]]
    )
    return f"{base_url_template}?{query_string}"

async def fetch_from_url(url: str, params: dict = {}, headers: dict = {}) -> httpx.Response:
    """
    Fetches data from the specified URL using the provided parameters and headers.

    Args:
        url (str): The URL to fetch data from.
        params (dict, optional): The parameters to include in the request. Defaults to None.
        headers (dict, optional): The headers to include in the request. Defaults to None.

    Returns:
        httpx.Response: The response object containing the data fetched from the URL.

    Raises:
        None

    Examples:
        >>> obj = ClassName()
        >>> obj.fetch("https://example.com/data")
        <Response [200]>
    """
    return await httpx.get(url, params=params, headers=headers)