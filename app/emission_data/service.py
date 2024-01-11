import datetime
import logging
from typing_extensions import Buffer
import numpy as np
import pandas as pd
import prisma
from sklearn.preprocessing import MinMaxScaler
from tqdm import tqdm
from app.config.column_mapping import ipcc_to_gir, ipcc_to_gir_code
from app.database import get_connection
from app.emission_data.adapters.gir4_import_adapter import GirCategoryAdapter
from app.emission_data.models.partial_emission_data import create_partial_gir1
from app.isitecategoryrels.service import ISiteCategoryRelService
from app.utils.file import FileUtils
from app.utils.object import list_of_objects_to_dict
from app.config.column_mapping import ipcc_to_gir_code
from app.utils.data_types import parse_to_date, to_dict
from app.utils.string import get_second_level_category

class IEmissionDataService:
    def __init__(self) -> None:
        self.prisma = get_connection()
        self.relation_service = ISiteCategoryRelService()
        self.logger = logging.getLogger("api.iemissiondata")
        
    async def delete_all(self):
        """
        Deletes all records in the 'IEmissionData' table.
        """
        await self.prisma.iemissiondata.delete_many()

    async def update_or_create(
        self,
        data: prisma.models.IEmissionData,
        where: prisma.types.IEmissionDataWhereInput,
    ):
        """
        Update or create a record in the database based on the given data and where condition.

        Args:
            data (prisma.models.IEmissionData): The data to update or create the record with.
            where (prisma.types.IEmissionDataWhereInput): The condition to search for an existing record.

        Returns:
            None
        """
        existing_record = await self.prisma.iemissiondata.find_first(where=where)

        if existing_record:
            return await self.prisma.iemissiondata.update(
                where={"uid": existing_record.uid}, data=data
            )
        else:
            return await self.prisma.iemissiondata.create(data=data)

    async def upsert(
        self,
        data: prisma.types.IEmissionDataCreateInput,
        where: prisma.types.IEmissionDataWhereUniqueInput,
        include=None,
    ):
        """
        Upserts an organization in the database.

        Args:
            data (prisma.types.IEmissionDataCreateInput): The data to be upserted.
            where (prisma.types.IEmissionDataWhereUniqueInput): The unique identifier of the organization.
            include (Optional): The related models and fields to include in the upsert operation.

        Returns:
            None
        """
        return await self.prisma.iemissiondata.upsert(
            data={"create": data, "update": data}, where=where
        )

    async def create(
        self, data: prisma.types.IEmissionDataCreateInput
    ) -> prisma.models.IEmissionData:
        """
        Creates a new organization with the given data.

        Parameters:
            - data: An instance of prisma.types.IEmissionDataCreateInput representing the data for the new organization.

        Returns:
            None
        """
        return await self.prisma.iemissiondata.create(data=data)

    async def update(
        self,
        data: prisma.models.IEmissionData,
        where: prisma.types.IEmissionDataWhereUniqueInput = None,
    ) -> prisma.models.IEmissionData:
        """
        Update the given organization with the provided data.

        Args:
            data (prisma.models.IEmissionData): The data to update the organization with.
            where (prisma.types.IEmissionDataWhereUniqueInput): The unique identifier for the organization.

        Returns:
            None
        """
        return await self.prisma.iemissiondata.update(where=where, data=data)

    async def delete(self, where: prisma.types.IEmissionDataWhereInput) -> None:
        """
        Deletes a record from the OrgSite table based on the given criteria.

        Parameters:
            where (prisma.types.IEmissionDataWhereInput): The criteria used to determine which records to delete.

        Returns:
            None
        """
        await self.prisma.iemissiondata.delete(where=where)

    async def fetch_many(
        self, where: prisma.types.IEmissionDataWhereInput, include=None
    ) -> list[prisma.models.IEmissionData]:
        """
        Fetches some data based on the given where clause.

        Args:
            where: An input object type that represents the conditions used to filter the data.

        Returns:
            A list of IEmissionData objects that match the given conditions.
        """
        return await self.prisma.iemissiondata.find_many(where=where, include=include)

    async def fetch_one(
        self, where: prisma.types.IEmissionDataWhereInput
    ) -> prisma.models.IEmissionData | None:
        """
        Fetches a single record based on the given where clause.

        Args:
            where: An input object type that represents the conditions used to filter the data.

        Returns:
            An IEmissionData object that matches the given conditions or None if no record is found.
        """
        return await self.prisma.iemissiondata.find_first(where=where)

    async def fetch_all(self) -> list[prisma.models.IEmissionData]:
        """
        Fetches all data from the OrgSite table.

        Returns:
            A list of IEmissionData objects representing all records in the OrgSite table.
        """
        return await self.prisma.iemissiondata.find_many()

    async def create_many(self, data: prisma.types.IEmissionDataCreateInput) -> None:
        """
        Create multiple organizations.

        Args:
            data (prisma.types.IEmissionDataCreateInput): The data to create multiple organizations.

        Returns:
            None: This function does not return anything.
        """
        await self.prisma.iemissiondata.create_many(data=data)

    async def group_by(
        self,
        count=None,
        by=None,
        sum=None,
        order=None,
        having=None,
        where: prisma.types.IEmissionDataWhereInput = None,
    ) -> list[prisma.models.IEmissionData]:
        """
        A decorator that catches any errors that occur during the execution of the `group_by` function.

        Args:
            count (Optional): The count parameter of the `group_by` function.
            by (Optional): The by parameter of the `group_by` function.
            sum (Optional): The sum parameter of the `group_by` function.
            order (Optional): The order parameter of the `group_by` function.
            having (Optional): The having parameter of the `group_by` function.

        Returns:
            list[prisma.models.IEmissionData]: A list of `prisma.models.IEmissionData` objects.
        """
        return await self.prisma.iemissiondata.group_by(
            count=count, by=by, sum=sum, order=order, having=having, where=where
        )

    async def _fetch_page(
        self, cursor: str, page_size=10
    ) -> tuple[list[prisma.models.IEmissionData], str]:
        """
        Fetches a page of organizations from the database.

        Args:
            cursor (str): The cursor used for pagination.
            page_size (int, optional): The number of results per page. Defaults to 10.

        Returns:
            Tuple[List[prisma.models.IEmissionData], str]: A tuple containing a list of organizations
                and the next cursor for pagination.
        """
        results = await self.prisma.iemissiondata.find_many(
            take=page_size,
            cursor={"id": cursor} if cursor else None,
            order={"id": "asc"},
        )
        next_cursor = results[-1].id if results else None
        return results, next_cursor

    async def fetch_paged(
        self,
        take=10,
        skip=0,
        order=None,
        where: prisma.types.IEmissionDataWhereInput = None,
        include=None,
    ) -> list[prisma.models.IEmissionData]:
        """
        Fetches a paged list of organizations.

        Args:
            take (int): The number of items to take per page.
            skip (int): The number of items to skip.
            order (Optional[str]): The field to order the results by.

        Returns:
            list[prisma.models.IEmissionData]: The list of organizations.
        """
        results = await self.prisma.iemissiondata.find_many(
            take=take, skip=skip, order=order, where=where, include=include
        )
        return results

    async def fetch_all_paginated(self):
        pass

    async def fetch_count(self) -> int:
        """
        Fetches the count of the IEmissionData table.

        Returns:
            int: The count of the IEmissionData table.
        """
        return await self.prisma.iemissiondata.count()

    # Business logic

    async def upload_data(
        self, data_source: str, buffer: Buffer = None, path: str = None
    ):
        gir4_adp = GirCategoryAdapter()
        files = FileUtils()
        if "gir4" in data_source.lower():
            df = await gir4_adp.prepare(data_source, buffer, data_source)
        for row in tqdm(df.to_dict(orient="records"), total=len(df)):
            await self.create(data=row)

    async def match_codes(self):
        """_summary_
        Matches the codes in the dictionary to the industry numbers in each factory, and returns the dataframe
        Returns:
            dataframe: dataframe with matched codes
        """
        find_where = {"categoryName": {"in": list(ipcc_to_gir.values())}}
        res = await self.fetch_many(where=find_where)
        df = pd.DataFrame([vars(d) for d in res])
        inverse_map = {v: k for k, v in ipcc_to_gir.items()}
        df["category"] = df["categoryName"].map(inverse_map)
        return df

    async def calculate_emissions(self) -> None:
        date_boundaries = await self.get_date_boundaries()
        date_from = date_boundaries.get("from")
        date_to = date_boundaries.get("to")
        date_from = parse_to_date(date_from)
        date_to = parse_to_date(date_to)
        for year in tqdm(range(date_from.year, date_to.year + 1)):
            logging.getLogger("api.iemissiondata").debug(f"Calculating emissions for year {year}...")
            await self.calc_emissions_dt_range(year=year)
        

    async def calc_emissions_dt_range(self, year: int) -> None:
        """
        Calculate emission ratios and emissions for the given site category relations.

        Args:
            relations (list[prisma.models.ISiteCategoryRel]): A list of site category relations.

        Returns:
            None: This function does not return anything.
        """
        date_from = datetime.datetime(year, 1, 1)
        date_to = datetime.datetime(year, 12, 31)
        relations = await self.relation_service.fetch_many(
            where={"site": {"is": {"operationStartDt": {"lte": date_from}}}},
            include={"site": True},
        )

        if not relations or len(relations) == 0:
            raise Exception("No relations found")
        relations_df = [to_dict(rel) for rel in relations]
        relations_df = pd.DataFrame(relations_df)
        total_contribution_magnitude_in_sector = relations_df.groupby("categoryName")[
            "contributionMagnitudeSector"
        ].sum()

        for relation in tqdm(
            relations, total=len(relations), desc="calculate_emission_ratios"
        ):
            if relation.categoryName is None:
                continue

            if relation.categoryLevel > 2:
                # E.g. category_name_gir4 = 2.A
                category_name = relation.categoryName
                total_emission = await self.fetch_one(
                    where={
                        "categoryName": category_name,
                        "periodStartDt": {"gte": date_from},
                        "periodEndDt": {"lte": date_to},
                        "pollutantId": "CO2",
                        "NOT": {"source": {"startsWith": "calc:"}},
                    }
                )
            else:
                category_name = ipcc_to_gir_code.get(
                    get_second_level_category(relation.categoryName)
                )
                total_emission = await self.group_by(
                    by=["categoryName", "pollutantId"],
                    sum={"emissionTotal": True},
                    having={
                        "categoryName": category_name,
                    },
                    where={
                        "periodStartDt": {"gte": date_from},
                        "periodEndDt": {"lte": date_to},
                        "NOT": {"source": {"startsWith": "calc:"}},
                    },
                )
                category_name = relation.categoryName
                total_emission = total_emission[0]
                total_emission["emissionTotal"] = (
                    total_emission["_sum"]["emissionTotal"] / 1000
                )  ##TODO: Create unit conversion function
                total_emission = create_partial_gir1(
                    total_emission=total_emission, categoryName=category_name, date_from=date_from, date_to=date_to
                )

            if total_emission is None or total_emission.emissionTotal is None:
                continue
            total_emission_gas = total_emission.emissionTotal
            matching_item = total_contribution_magnitude_in_sector.loc[category_name]
            if matching_item is not None:
                contribution_ratio = (
                    relation.contributionMagnitudeSector / matching_item
                )

                emission = contribution_ratio * total_emission_gas
                return await self.update_or_create(
                    data={
                        "categoryName": category_name,
                        "periodStartDt": total_emission.periodStartDt,
                        "periodEndDt": total_emission.periodEndDt,
                        "emissionTotal": emission,
                        "pollutantId": total_emission.pollutantId,
                        "periodLength": total_emission.periodLength,
                        "source": "calc:" + total_emission.source,
                        "regionUid": relation.site.addressRegionUid,
                        "siteUid": relation.siteUid,
                        "regionName": relation.site.addressSubRegion,
                        "longitude": relation.site.longitude,
                        "latitude": relation.site.latitude,
                        "categoryRelUid": relation.uid,
                    },
                    where={
                        "categoryName": relation.categoryName,
                        "periodStartDt": total_emission.periodStartDt,
                        "periodEndDt": total_emission.periodEndDt,
                        "siteUid": relation.siteUid,
                        "pollutantId": total_emission.pollutantId,
                        "source": "calc:" + total_emission.source,
                        "regionUid": relation.site.addressRegionUid,
                        "categoryRelUid": relation.uid,
                    },
                )

    async def fetch_grouped_by_region( ##TODO: Refactor into smaller pieces
        self,
        year_start: str,
        year_end: str,
    ):
        if year_start is None:
            year_start = "2019-01-01T00:00:00.000Z"
        if year_end is None:
            year_end = "2020-01-01T00:00:00.000Z"
        gir_4_calc = await self.prisma.iemissiondata.find_many(
            where={
                "source": "calc:gir4",
                "regionUid": {"not": None},
                "periodStartDt": {"gte": year_start},
                "periodEndDt": {"lte": year_end},
            },
            include={"region": True},
        )

        gir_1_calc = await self.prisma.iemissiondata.find_many(
            where={
                "source": "calc:gir1",
                "regionUid": {"not": None},
                "periodStartDt": {"gte": year_start},
                "periodEndDt": {"lte": year_end},
            },
            include={"region": True},
        )

        gir_1 = await self.prisma.iemissiondata.group_by(
            where={
                "source": "gir1",
                "categoryName": {"in": list(ipcc_to_gir_code.values())},
                "periodStartDt": {"gte": year_start},
                "periodEndDt": {"lte": year_end},
            },
            by=[
                "categoryName",
                "regionName",
                "source",
                "latitude",
                "longitude",
            ],
            sum={"emissionTotal": True},
        )
        if len(gir_1) == 0 or len(gir_4_calc) == 0 or len(gir_1_calc) == 0:
            return {}

        gir_1_df = pd.DataFrame.from_records(gir_1)
        gir_1_df["emissionTotal"] = gir_1_df["_sum"].apply(
            lambda x: x.get("emissionTotal") / 1000 if x.get("emissionTotal") else 0
        )

        # gir_4_group_df = pd.DataFrame.from_records(gir_4_group)
        # gir_1_group_df = pd.DataFrame.from_records(gir_1_group)
        # print(gir_1_df["_sum"].head(10))
        gir_4_calc_df = pd.DataFrame(list_of_objects_to_dict(gir_4_calc))
        gir_4_calc_df["latitude"] = gir_4_calc_df.apply(
            lambda x: x["region"].latitude, axis=1
        )
        gir_4_calc_df["longitude"] = gir_4_calc_df.apply(
            lambda x: x["region"].longitude, axis=1
        )
        gir_1_calc_df = pd.DataFrame(list_of_objects_to_dict(gir_1_calc))
        gir_1_calc_df["latitude"] = gir_1_calc_df.apply(
            lambda x: x["region"].latitude, axis=1
        )
        gir_1_calc_df["longitude"] = gir_1_calc_df.apply(
            lambda x: x["region"].longitude, axis=1
        )
        gir_4_calc_groupped = gir_4_calc_df.groupby(["regionUid"], as_index=False).agg(
            {
                "emissionTotal": "sum",
                "latitude": "mean",
                "longitude": "mean",
                "regionName": "first",
            }
        )
        gir_1_calc_groupped = gir_1_calc_df.groupby(
            by=["regionUid"], as_index=False
        ).agg(
            {
                "emissionTotal": "sum",
                "latitude": "mean",
                "longitude": "mean",
                "regionName": "first",
            }
        )

        gir_1_groupped = gir_1_df.groupby(by=["regionName"], as_index=False).agg(
            {"emissionTotal": "sum", "latitude": "mean", "longitude": "mean"}
        )
        gir_1_groupped.fillna("")
        gir_1_calc_groupped.fillna("")
        gir_4_calc_groupped.fillna("")
        scaler = MinMaxScaler(feature_range=(0, 1))

        gir_1_groupped["norm"] = scaler.fit_transform(gir_1_groupped[["emissionTotal"]])
        gir_4_calc_groupped["norm"] = scaler.transform(
            gir_4_calc_groupped[["emissionTotal"]]
        )
        gir_1_calc_groupped["norm"] = scaler.transform(
            gir_1_calc_groupped[["emissionTotal"]]
        )
        return {
            "gir4Calc": gir_4_calc_groupped.to_dict("records"),
            "gir1Calc": gir_1_calc_groupped.to_dict("records"),
            "gir1": gir_1_groupped.to_dict("records"),
        }

    async def get_date_boundaries(self):
        """
        Retrieves the maximum and minimum date boundaries of the emission data.

        Parameters:
            where (prisma.types.IEmissionDataWhereInput, optional): The filter to apply to the emission data. Defaults to None.

        Returns:
            A dictionary containing the maximum and minimum date boundaries of the emission data.
        """
        boundaries = await self.prisma.query_raw(
            query="""SELECT MIN("periodStartDt") AS from, MAX("periodEndDt") AS to from "IEmissionData" WHERE source like 'calc:%'"""
        )

        return boundaries[0]
