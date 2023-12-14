import datetime
import pytest

from app.emission_data.models.partial_emission_data import create_partial_gir1

def test_create_partial_gir1():
    kwargs = {
        "total_emission": {
            "emissionTotal": None
        },
        "categoryName": "Category 1"
    }
    
    result = create_partial_gir1(**kwargs)
    
    assert result.emissionTotal == 0
    assert result.categoryName == "Category 1"
    assert result.pollutantId == "CO2eq"
    assert result.periodStartDt == datetime.datetime(2020, 1, 1)
    assert result.periodEndDt == datetime.datetime(2020, 12, 31)
    assert result.periodLength == "1Y"
    assert result.source == "gir1"

if __name__ == "__main__":
    pytest.main()
