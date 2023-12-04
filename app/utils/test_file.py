from typing_extensions import Buffer
import pytest
from unittest.mock import MagicMock
import pandas as pd
import pytest_asyncio

from app.utils.file import read_to_pd

@pytest.fixture
def buffer():
    return MagicMock()

@pytest.fixture
def path():
    return "path/to/excel.xlsx"

@pytest_asyncio.fixture
async def test_read_csv_with_buffer(buffer):
    # Test reading CSV with buffer
    df = pd.DataFrame([["a", "b"], ["c", "d"]], columns=["col1", "col2"])
    buffer.read_excel.return_value = df

    result = await read_to_pd(buffer=buffer)

    assert result.equals(df)

@pytest_asyncio.fixture
async def test_read_csv_with_path(path):
    # Test reading CSV with path
    df = pd.DataFrame([["a", "b"], ["c", "d"]], columns=["col1", "col2"])
    pd.read_excel.return_value = df

    result = await read_to_pd(path=path)

    assert result.equals(df)

@pytest_asyncio.fixture
async def test_read_excel_with_buffer(buffer: Buffer):
    # Test reading Excel with buffer
    df = pd.DataFrame([["a", "b"], ["c", "d"]], columns=["col1", "col2"])
    buffer.read_excel.return_value = df

    result = await read_to_pd(buffer=buffer)

    assert result.equals(df)

@pytest_asyncio.fixture
async def test_read_excel_with_path(path):
    # Test reading Excel with path
    df = pd.DataFrame([["a", "b"], ["c", "d"]], columns=["col1", "col2"])
    pd.read_excel.return_value = df

    result = await read_to_pd(path=path)

    assert result.equals(df)

@pytest_asyncio.fixture
async def test_invalid_arguments(buffer, path):
    # Test raising an exception when both buffer and path are provided
    with pytest.raises(Exception):
        await read_to_pd(buffer=buffer, path=path)