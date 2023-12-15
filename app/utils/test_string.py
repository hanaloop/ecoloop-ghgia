from app.utils.string import get_coords_from_detail, get_second_level_category
from app.utils.string import get_category_list

def test_get_first_level_category():
    assert get_second_level_category("a.b.c.d") == "a.b"
    assert get_second_level_category("x.y.z") == "x.y"
    assert get_second_level_category("123.456.789") == "123.456"
    assert get_second_level_category("foo.bar.baz") == "foo.bar"



def test_get_category_list():
    # Test case 1: Single level category
    assert get_category_list("a", return_lvl_from=1) == ['a']

    # Test case 2: Two level category
    assert sorted(get_category_list("a.b", return_lvl_from=1)) == sorted(['a.b', 'a'])

    # Test case 3: Three level category
    assert get_category_list("a.b.c", return_lvl_from=2) == ['a.b', 'a.b.c']

    # Test case 5: Empty category
    assert get_category_list("", return_lvl_from=1) == ['']

    # Test case 7: Category with leading and trailing dots
    assert get_category_list(".a.b.c.", return_lvl_from=1) == ['a', 'a.b', 'a.b.c']

    # Test case 8: Category with spaces
    assert get_category_list("a . b . c", return_lvl_from=1) == ['a', 'a.b', 'a.b.c']

    # Test case 10: Category with numbers
    assert get_category_list("2.A.1", return_lvl_from=1) == ['2', '2.A', '2.A.1']


def test_both_coords_exist():
    detail = {'latitude': 123.456, 'longitude': 987.654}
    expected_result = (123.456, 987.654)
    assert get_coords_from_detail(detail) == expected_result

def test_only_latitude_exists():
    detail = {'latitude': 123.456}
    expected_result = (123.456, None)
    assert get_coords_from_detail(detail) == expected_result

def test_only_longitude_exists():
    detail = {'longitude': 987.654}
    expected_result = (None, 987.654)
    assert get_coords_from_detail(detail) == expected_result

def test_neither_coord_exists():
    detail = {}
    expected_result = (None, None)
    assert get_coords_from_detail(detail) == expected_result
