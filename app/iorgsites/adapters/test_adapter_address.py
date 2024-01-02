import pandas as pd
import pytest
from app.iorgsites.adapters.adapter_address import format_address_df, fix_address_string

@pytest.fixture
def sample_dataframe():
    # Create a sample DataFrame for testing
    df = pd.DataFrame({"address": ["123 Main St (Suite 102)", "456 Elm St (Unit 101)"]})
    return df

@pytest.mark.skip("Do not remember how function was used")
def test_format_address_df(sample_dataframe):
    address_col = "address"

    # Expected result after formatting the addresses
    expected_df = pd.DataFrame({"address": ["123 Main St", "456 Elm St"]})

    # Call the function to format the addresses
    result_df = format_address_df(sample_dataframe, address_col)

    # Check if the result matches the expected output
    assert expected_df.equals(result_df)


def test_address_with_parentheses():
    address = "서울시 강남구 역삼동 123번지 (4층)"
    expected = "서울시 강남구 역삼동 123번지"
    assert fix_address_string(address) == expected

def test_address_with_korean_address():
    address = "부산시 해운대구 우동 456필지"
    expected = "부산시 해운대구 우동"
    assert fix_address_string(address) == expected

@pytest.mark.skip("We are currently not using the pattern")
def test_address_with_outer_pattern():
    address = "대구시 중구 동인동 외 외"
    expected = "대구시 중구 동인동"
    assert fix_address_string(address) == expected

@pytest.mark.skip("We are currently not using the pattern")
def test_address_with_outer_whitespace():
    address = "인천시 남구 남동 외"
    expected = "인천시 남구 남동"
    assert fix_address_string(address) == expected


@pytest.mark.skip("We are currently not using the pattern")
def test_address_with_bonzi():
    address = "인천시 남구 남동 34번지"
    expected = "인천시 남구 남동"
    assert fix_address_string(address) == expected

def test_address_with_comma():
    address = "부산시 해운대구 우동, 456필지"
    expected = "부산시 해운대구 우동"
    assert fix_address_string(address) == expected


def test_address_with_extra_whitespace():
    address = "   인천시 남구 남동 34번지   "
    expected = "인천시 남구 남동 34번지"
    assert fix_address_string(address) == expected
