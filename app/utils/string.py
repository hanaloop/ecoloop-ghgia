def get_second_level_category (x: str):
    """
        Return the first level category of a given gir category.

        Parameters:
        x (str): The input string representing a category.

        Returns:
        str: The first level category.

        Example:
        >>> get_first_level_category("a.b.c.d")
        'a.b'
    """
    return '.'.join(x.split('.')[:2])


def get_category_list(x: str, return_lvl_from: int, return_lvl_to: int | None = None)->list[str]:
    """
    Generate a list of ipcc categories based on a given string.

    Parameters:
        x (str): The input string.
        return_lvl_from (int): The starting level of categories to include in the list.
        return_lvl_to (int | None): The ending level of categories to include in the list. If not provided, all levels will be included.

    Returns:
        list[str]: A list of categories based on the input string.
    """
    x = x.replace(' ', '')
    x = x.strip('.')
    if not return_lvl_to:
        return_lvl_to = len(x.split('.'))
    if return_lvl_from > return_lvl_to:
        raise ValueError("return_lvl_from must be less than or equal to return_lvl_to.")
    lvl_list = []
    for i in range(return_lvl_from, return_lvl_to+1):
        lvl_list.append(".".join(x.split('.')[:i]))
    return lvl_list

def get_coords_from_detail(detail: dict):
    latitude = detail.get('latitude', None)
    longitude = detail.get('longitude', None)
    if not latitude or not longitude:
        latitude = detail.get('lat', None)
        longitude = detail.get('lon', None)
    if not latitude or not longitude:
        latitude = detail.get('y', None)
        longitude = detail.get('x', None)
    return latitude, longitude


def get_parent_region(x: str):
    return x.split(' ')[0]

def get_regions_as_tuple(structured_address: str):
    """
    Retrieves the regions from the given structured address and returns them as a tuple.

    Parameters:
    - address_detail (str): The address detail from which to retrieve the regions.

    Returns:
    - tuple: A tuple containing the regions extracted from the address detail.
    """
    if not structured_address:
        return None, None
    divisions = structured_address.split("|")
    if len(divisions) == 1:
        return divisions[0].split(" ")[0], None
    try:
        region1 = divisions[0].split(" ")[0]
    except:
        region1 = divisions[0]
    try:
        region2 = divisions[1].split(" ")[0]
    except:
        region2 = divisions[1]
    region1.strip()
    region2.strip()
    return region1, region2
