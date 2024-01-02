
##TODO: Replace with a create_partial model later
from prisma.models import IEmissionData

def create_partial_gir1(**kwargs) -> IEmissionData:
    total_emissions_gir1 = IEmissionData.model_construct(**kwargs.get("total_emission", {}))
    total_emissions_gir1.emissionTotal = total_emissions_gir1.emissionTotal or 0
    total_emissions_gir1.categoryName = kwargs.get("categoryName")
    total_emissions_gir1.pollutantId = "CO2eq"
    total_emissions_gir1.periodStartDt = kwargs.get("date_from")
    total_emissions_gir1.periodEndDt = kwargs.get("date_to")
    total_emissions_gir1.periodLength = "1Y"
    total_emissions_gir1.source = "gir1"
    return total_emissions_gir1
