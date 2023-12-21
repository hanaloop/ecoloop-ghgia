from app.foundation.adapter_prisma import PrismaAdapter

adapter = PrismaAdapter()
def test_to_query_args_simple():
    test = adapter.to_query_args(query={"field": "value"})
    assert test == {"field": "value"}

def test_to_query_args_many_args():
    test = adapter.to_query_args(query={"field": "value", "field2": "value2"})
    assert test == {"field": "value", "field2": "value2"}

def test_to_query_args_complex_list():
    test = adapter.to_query_args(query={"field:in":"value1,value2"})
    assert test == {"field": {"in":[ "value1" ,"value2"]}}

def test_to_query_args_with_operator():
    test = adapter.to_query_args(query={"field:equals":"value"})
    assert test == {"field": {"equals": "value"}}
