import datetime

##TODO: Replace with a create_partial model later
import datetime
from prisma.models import IEmissionData

def create_partial_gir1(**kwargs) -> IEmissionData:
    total_emissions_gir1 = IEmissionData.model_construct(**kwargs.get("total_emissions_gir1", {}))
    total_emissions_gir1.emissionTotal = total_emissions_gir1.emissionTotal or 0
    total_emissions_gir1.categoryName = kwargs.get("categoryName")
    total_emissions_gir1.pollutantId = "CO2eq"
    total_emissions_gir1.periodStartDt = datetime.datetime(2020, 1, 1)  # TODO: Change when we actually have variable dates
    total_emissions_gir1.periodEndDt = datetime.datetime(2020, 12, 31)
    total_emissions_gir1.periodLength = "1Y"
    total_emissions_gir1.source = "gir1"
    return total_emissions_gir1