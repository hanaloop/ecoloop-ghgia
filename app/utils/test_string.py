import pytest

from app.utils.string import get_first_level_category

def test_get_first_level_category():
    assert get_first_level_category("a.b.c.d") == "a.b"
    assert get_first_level_category("x.y.z") == "x.y"
    assert get_first_level_category("123.456.789") == "123.456"
    assert get_first_level_category("foo.bar.baz") == "foo.bar"
