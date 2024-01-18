import pandas as pd
import pytest

import pandas as pd
import pytest
from app.emission_data.adapters.gir1_import_adapter import GirImportAdapter

sample_pickle = pd.read_pickle('./test_data/adapter_gir1.pkl')
@pytest.mark.skip("we changed the structure of the database, need to recreate the sample pickle")
@pytest.mark.asyncio
async def test_prepare():
    adapter = GirImportAdapter()

    # Test case 1: Test with a valid path and data_source is None
    path = "./test_data/emission_data.gir1.import.csv"
    pd.testing.assert_frame_equal(await adapter.prepare(path), sample_pickle)

    # Test case 2: Test with an invalid path
    path = "invalid_file.csv"
    with pytest.raises(FileNotFoundError):
        await adapter.prepare(path)

