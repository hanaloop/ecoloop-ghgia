from app.foundation.adapter_prisma import PrismaAdapter

adapter = PrismaAdapter()


def test_to_query_args_simple():
    test = adapter.to_query_args(query={"field": "value"})
    assert test == {"field": "value"}


def test_to_query_args_many_args():
    test = adapter.to_query_args(query={"field": "value", "field2": "value2"})
    assert test == {"field": "value", "field2": "value2"}


def test_to_query_args_complex_list():
    test = adapter.to_query_args(query={"field:in": "value1,value2"})
    assert test == {"field": {"in": ["value1", "value2"]}}


def test_to_query_args_with_operator():
    test = adapter.to_query_args(query={"field:equals": "value"})
    assert test == {"field": {"equals": "value"}}


class TestToPageableResponse:
    def setup_method(self):
        self.obj = PrismaAdapter()

    def test_empty_response(self):
        query = {"_pageNum": 0, "_pageSize": 10}
        response = None
        count = 0
        result = self.obj.to_pageable_response(query, response, count)
        assert result is None

    def test_non_empty_response(self):
        query = {"_pageNum": 0, "_pageSize": 10}
        response = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        count = 15
        result = self.obj.to_pageable_response(query, response, count)
        assert result.number == 0
        assert result.numberOfElements == 15
        assert result.size == 10
        assert result.first
        assert not result.last
        assert result.totalPages == 2
        assert result.totalElements == 15
        assert result.content == response

    def test_page_number_greater_than_zero(self):
        query = {"_pageNum": 1, "_pageSize": 10}
        response = [1, 2, 3, 4, 5]
        count = 15
        result = self.obj.to_pageable_response(query, response, count)
        assert result.number == 1
        assert result.numberOfElements == 5
        assert result.size == 10
        assert not result.first
        assert result.last
        assert result.totalPages == 2
        assert result.totalElements == 15
        assert result.content == [1, 2, 3, 4, 5]

    def test_page_size_greater_than_count(self):
        query = {"_pageNum": 0, "_pageSize": 20}
        response = [1, 2, 3, 4, 5]
        count = 5
        result = self.obj.to_pageable_response(query, response, count)
        assert result.number == 0
        assert result.numberOfElements == 5
        assert result.size == 20
        assert result.first
        assert result.last
        assert result.totalPages == 1
        assert result.totalElements == 5
        assert result.content == [1, 2, 3, 4, 5]


class TestToIncludeExcludeArgs:
    def setup_method(self):
        self.obj = PrismaAdapter()

    def test_empty_arg(self):
        arg = []
        result = self.obj.to_include_exclude_args(arg)
        assert result is None

    def test_single_element_arg(self):
        arg = "element"
        result = self.obj.to_include_exclude_args(arg)
        assert result == {"element": True}

    def test_multiple_element_arg(self):
        arg = ["element1", "element2", "element3"]
        result = self.obj.to_include_exclude_args(arg)
        assert result == {"element1": True, "element2": True, "element3": True}

    def test_non_list_arg(self):
        arg = "element"
        assert self.obj.to_include_exclude_args(arg) == {"element": True}
