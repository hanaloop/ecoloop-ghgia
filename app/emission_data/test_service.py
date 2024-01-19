import pytest
from datetime import datetime
from dateutil.relativedelta import relativedelta
from app.emission_data.service import IEmissionDataService
from pytest_mock import mocker
import prisma

# Test case 1: No sites
@pytest.mark.asyncio
async def test_create_org_emission_no_sites(mocker):
    service = IEmissionDataService()

    data = {
        "uid": "org_uid",
        "year": 2020,
        "emissionTotal": 100,
        "source": "source",
        "energyHeat": 50,
        "energyElectricity": 30,
        "energyFuel": 20,
        "energyTotal": 100,
        "sites": None
    }
    model_data = prisma.models.IOrganization.model_construct(**{"uid": "org_uid", "sites": []})
    mocker.patch("app.emission_data.service.IEmissionDataService.create")
    mocker.patch("app.emission_data.service.IEmissionDataService.update_or_create")
    mocker.patch("prisma.client.actions.IOrganizationActions.find_first", return_value=model_data)
    await service.create_org_emission(data)
    prisma.client.actions.IOrganizationActions.find_first.assert_called_once()
    service.create.assert_not_called()

@pytest.mark.asyncio
async def test_create_org_emission_one_site_zero_area(mocker):
    # Test case 2: One site with zero manufacturing facility area
    service = IEmissionDataService()

    data = {
        "uid": "org_uid",
        "year": 2020,
        "emissionTotal": 100,
        "source": "source",
        "energyHeat": 50,
        "energyElectricity": 30,
        "energyFuel": 20,
        "energyTotal": 100,
    }
    site = {
        "manufacturingFacilityArea": 0,
        "uid": "site_uid"
    }
    expected_data = {
        "periodStartDt": datetime(2020, 1, 1),
        "periodEndDt": datetime(2021, 1, 1),
        "emissionTotal": 0,
        "emissionDirect": 0,
        "emissionIndirect": 0,
        "longitude": None,
        "latitude": None,
        "regionUid": None,
        "regionName": None,
        "source": "source",
        "energyHeat": 0,
        "energyElectricity": 0,
        "energyFuel": 0,
        "energyTotal": 0,
        "periodLength": "1Y",
        "pollutantId": "tCO2eq",
        "siteUid": "site_uid"

    }
    site = prisma.models.IOrgSite.model_construct(**site)
    model_data = prisma.models.IOrganization.model_construct(**{"uid": "org_uid", "sites": [site]})
    mocker.patch("app.emission_data.service.IEmissionDataService.create")
    mocker.patch("app.emission_data.service.IEmissionDataService.update_or_create")
    mocker.patch("prisma.client.actions.IOrganizationActions.find_first", return_value=model_data)
    return_value = await service.create_org_emission(data)
    prisma.client.actions.IOrganizationActions.find_first.assert_called_once()
    service.create.assert_called_once()
    assert service.create.call_args_list[0][1]["data"] == expected_data


@pytest.mark.asyncio
async def test_create_org_emission_one_site_non_zero_area(mocker):
    service = IEmissionDataService()

    # Test case 3: One site with non-zero manufacturing facility area
    data = {
        "uid": "org_uid",
        "year": 2020,
        "emissionTotal": 100,
        "source": "source",
        "energyHeat": 50,
        "energyElectricity": 30,
        "energyFuel": 20,
        "energyTotal": 100,
    }
    sites = [
        {
            "manufacturingFacilityArea": 75,
            "uid": "site_uid_1"
        },
        {
            "manufacturingFacilityArea": 25,
            "uid": "site_uid_2"
        }
    ]

    expected_data = [{
        "periodStartDt": datetime(2020, 1, 1),
        "periodEndDt": datetime(2021, 1, 1),
        "emissionTotal": 75,
        "emissionDirect": 0,
        "emissionIndirect": 0,
        "longitude": None,
        "latitude": None,
        "regionUid": None,
        "regionName": None,
        "source": "source",
        "energyHeat": 37.5,
        "energyElectricity": 22.5,
        "energyFuel": 15,
        "energyTotal": 75,
        "siteUid": "site_uid_1",
        "periodLength": "1Y",
        "pollutantId": "tCO2eq"
    }, 
    {
        "periodStartDt": datetime(2020, 1, 1),
        "periodEndDt": datetime(2021, 1, 1),
        "emissionTotal": 25,
        "emissionDirect": 0,
        "emissionIndirect": 0,
        "longitude": None,
        "latitude": None,
        "regionUid": None,
        "regionName": None,
        "source": "source",
        "energyHeat": 12.5,
        "energyElectricity": 7.5,
        "energyFuel": 5.0,
        "energyTotal": 25.0,
        "siteUid": "site_uid_2",
        "periodLength": "1Y",
        "pollutantId": "tCO2eq"


    }]
    site_1 = prisma.models.IOrgSite.model_construct(**sites[0])
    site_2 = prisma.models.IOrgSite.model_construct(**sites[1])
    model_data = prisma.models.IOrganization.model_construct(**{"uid": "org_uid", "sites": [site_1, site_2]})
    mocker.patch("app.emission_data.service.IEmissionDataService.create")
    mocker.patch("app.emission_data.service.IEmissionDataService.update_or_create")
    mocker.patch("prisma.client.actions.IOrganizationActions.find_first", return_value=model_data)
    await service.create_org_emission(data)
    prisma.client.actions.IOrganizationActions.find_first.assert_called_once()
    call_args = [kwargs['data'] for args, kwargs in service.create.call_args_list]
    assert call_args == expected_data
