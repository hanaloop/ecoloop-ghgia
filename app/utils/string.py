def get_first_level_category (x: str):
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
