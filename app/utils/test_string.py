from app.utils.string import get_second_level_category
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
