import pandas as pd
import pytest

import pandas as pd
import pytest
from app.emission_data.adapters.gir4_import_adapter import GirCategoryAdapter

sample_pickle = pd.read_pickle('./test_data/adapter_gir4.pkl')
@pytest.mark.asyncio
async def test_prepare():
    adapter = GirCategoryAdapter()

    # Test case 1: Test with a valid path and data_source is None
    path = "./test_data/emission_data.gir4.import.xls"
    pd.testing.assert_frame_equal(await adapter.prepare(path), sample_pickle)

    # Test case 2: Test with an invalid path
    path = "invalid_file.xls"
    with pytest.raises(FileNotFoundError):
        await adapter.prepare(path)

    # Test case 3: Test with an invalid filetype
    path = "./test_data/emission_data.gir4.import.csv"
    with pytest.raises(ValueError):
        await adapter.prepare(path)
