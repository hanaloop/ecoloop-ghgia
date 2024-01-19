import pandas as pd
import prisma
from app.utils.data_types import parse_to_date, try_cast
from app.utils.file import FileUtils
from app.emission_data.service import IEmissionDataService
from app.iorganizations.service import IOrganizationService
from app.config.column_mapping import ets_report_col_map
from tqdm import tqdm
from app.foundation.field_type_match import model_fields_into_type_map, cast_dict_to_types

class EtsReportImporter:
    def __init__(self):
        self.files = FileUtils()
        self.emission_service = IEmissionDataService()
        self.organization_service = IOrganizationService()
        self.data_start_row = 5
        self.sheet_def = {"명세서 주요정보(2022)_할당대상업체_23.12":{"start_row": 5, "end_row": 712}, "명세서 주요정보(2022)_목표관리업체_23.12":{"start_row": 5, "end_row": 394}}

    async def import_data(self, filepath: str):
        filetype = self.files.get_file_extension(filepath)
        sheets = self.files.get_excel_sheet_names(filepath, filepath)
        df = pd.DataFrame()
        for sheet_name in sheets:
            _sheet_data = await self.files.read_to_pd(path=filepath, file_type=filetype, sheet=sheet_name, starting_row=self.sheet_def[sheet_name]["start_row"], last_row=self.sheet_def[sheet_name]["end_row"])
            _sheet_data.rename(columns=ets_report_col_map, inplace=True)
            df = pd.concat([df, _sheet_data], ignore_index=True)
        emissions_df, iorganization_df = await self.prepare(df)
        emission_types = model_fields_into_type_map(prisma.models.IEmissionData.model_fields)
        iorganization_types = model_fields_into_type_map(prisma.models.IOrganization.model_fields)
        for row1, row2 in tqdm(zip(emissions_df.to_dict(orient="records"), iorganization_df.to_dict(orient="records")), total=len(emissions_df)):
            row2 = cast_dict_to_types(row2, iorganization_types)
            created_org = await self.organization_service.update_or_create(data=row2, where={"legalName": row2["legalName"]})
            row1["organizationUid"] = created_org.uid
            row1 = cast_dict_to_types(row1, emission_types)
            await self.emission_service.update_or_create(data=row1, where={"source": row1["source"], "periodStartDt": row1["periodStartDt"], "periodEndDt": row1["periodEndDt"], "organizationUid": row1["organizationUid"]})


    async def prepare(self, df: pd.DataFrame):
        newDf = df.rename(columns=ets_report_col_map)
        newDf = newDf[newDf.columns.intersection(ets_report_col_map.values())] ##TODO: Check if they exist first
        emissions_df = newDf.loc[:,['year', 'emissionTotal', 'energyTotal'] ]
        iorganization_df = newDf.loc[:,['sectorMain', 'sectorSub', 'legalName', 'sizeCategory', 'verificationBody', 'regulationCriteria', 'notes']]
        applicable_regulations = ['ETS']
        ##We have to use list comprehension to create a list inside a cell otherwise pandas just assigns a simple string to each row
        ##https://stackoverflow.com/questions/49725203/adding-the-same-list-to-each-row-in-a-pandas-dataframe-in-a-new-column

        iorganization_df["applicableRegulations"] = [applicable_regulations for _ in range(len(iorganization_df))]
        emissions_df['source'] = 'orig:gir-ets'
        emissions_df['periodStartDt'] = emissions_df['year'].apply(lambda x: parse_to_date(str(x) + '-01-01', '%Y-%m-%d'))
        emissions_df['periodEndDt'] = emissions_df['year'].apply(lambda x: parse_to_date(str(x) + '-12-31', '%Y-%m-%d'))
        emissions_df['periodLength'] = '1Y'
        emissions_df.drop('year', axis=1, inplace=True)
        emissions_df['emissionTotal'] = pd.to_numeric(emissions_df['emissionTotal'], errors='coerce')
        emissions_df['energyTotal'] = pd.to_numeric(emissions_df['energyTotal'], errors='coerce')
        emissions_df['emissionTotal'].fillna(0, inplace=True)
        emissions_df['energyTotal'].fillna(0, inplace=True)
        return emissions_df, iorganization_df
