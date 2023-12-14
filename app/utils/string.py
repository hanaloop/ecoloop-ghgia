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
