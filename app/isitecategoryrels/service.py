import datetime
from tqdm import tqdm
from app.database import get_connection
import prisma
from app.emission_data.models.partial_emission_data import create_partial_gir1
from app.foundation.exception import catch_errors_decorator
from app.emission_data.service import IEmissionDataService
from app.config.column_mapping import ipcc_to_gir_code
from app.utils.data_types import to_dict
from app.utils.string import get_second_level_category
import pandas as pd


class ISiteCategoryRelService:
    def __init__(self):
        self.prisma = get_connection()
        self.emission_data_service = IEmissionDataService()

    async def delete_all(self) -> int:
        """
        Deletes all records in the 'ISiteCategoryRel' table.

        Returns:
            int: The number of deleted records.
        """
        return await self.prisma.isitecategoryrel.delete_many()

    @catch_errors_decorator
    async def delete_many(self, where: prisma.types.ISiteCategoryRelWhereInput) -> int:
        """
        Deletes multiple records in the 'ISiteCategoryRel' table based on the given where condition.

        Args:
            where (prisma.types.ISiteCategoryRelWhereInput): The where condition to delete records.

        Returns:
            int: The number of deleted records.
        """
        await self.prisma.isitecategoryrel.delete_many(where=where)

    async def update_or_create(
        self,
        data: prisma.models.ISiteCategoryRel,
        where: prisma.types.IOrgSiteWhereInput,
    ) -> prisma.models.ISiteCategoryRel:
        """
        Update or create a record in the database based on the given data and where condition.

        Args:
            data (prisma.models.ISiteCategoryRel): The data to update or create the record with.
            where (prisma.types.IOrgSiteWhereInput): The condition to search for an existing record.

        Returns:
            The updated or created record.

        """
        existing_record = await self.prisma.isitecategoryrel.find_first(where=where)

        if existing_record:
            return await self.prisma.isitecategoryrel.update(
                where={"uid": existing_record.uid}, data=data
            )
        else:
            return await self.prisma.isitecategoryrel.create(data=data)

    async def upsert(
        self,
        data: prisma.types.ISiteCategoryRelUpsertInput,
        where: prisma.types.ISiteCategoryRelWhereUniqueInput,
        include=None,
    ) -> int:
        """
        Upserts an organization site in the database.

        Args:
            data (prisma.types.ISiteCategoryRelUpsertInput): The data to be upserted.
            where (prisma.types.ISiteCategoryRelWhereUniqueInput): The unique identifier of the organization site.
            include (Optional): The related models and fields to include in the upsert operation.

        Returns:
            The upserted record.
        """

        await self.prisma.isitecategoryrel.upsert(
            data={"create": data, "update": data}, where=where, include=include
        )

    async def create(
        self, data: prisma.types.ISiteCategoryRelCreateInput
    ) -> prisma.models.ISiteCategoryRel | None:
        """
        Creates a new org site with the given data.

        Parameters:
            - data: An instance of prisma.types.IOrgSiteCreateInput representing the data for the new org site.

        Returns:
            None
        """
        return await self.prisma.isitecategoryrel.create(data=data)

    async def update(
        self,
        data: prisma.models.ISiteCategoryRel,
        where: prisma.types.IOrgSiteWhereUniqueInput,
    ) -> prisma.models.ISiteCategoryRel | None:
        """
        Update the given organization site with the provided data.

        Args:
            data (prisma.models.ISiteCategoryRel): The data to update the organization site with.
            where (prisma.types.IOrgSiteWhereUniqueInput): The unique identifier for the organization site.

        Returns:
            The updated rerord or None if no record was found.
        """
        return await self.prisma.isitecategoryrel.update(where=where, data=data)

    async def delete(self, where: prisma.types.IOrgSiteWhereInput) -> None:
        """
        Deletes a record from the OrgSite table based on the given criteria.

        Parameters:
            where (prisma.types.IOrgSiteWhereInput): The criteria used to determine which records to delete.

        Returns:
            None
        """
        await self.prisma.isitecategoryrel.delete(where=where)

    async def fetch_some(
        self,
        where: prisma.types.IOrgSiteWhereInput,
        include: prisma.types.IOrgSiteInclude | None = None,
    ) -> list[prisma.models.ISiteCategoryRel]:
        """
        Fetches some data based on the given where clause.

        Args:
            where: An input object type that represents the conditions used to filter the data.

        Returns:
            A list of ISiteCategoryRel objects that match the given conditions.
        """
        return await self.prisma.isitecategoryrel.find_many(
            where=where, include=include
        )

    async def fetch_one(
        self, where: prisma.types.IOrgSiteWhereInput
    ) -> prisma.models.ISiteCategoryRel | None:
        """
        Fetches a single record based on the given where clause.

        Args:
            where: An input object type that represents the conditions used to filter the data.

        Returns:
            An ISiteCategoryRel object that matches the given conditions or None if no record is found.
        """
        return await self.prisma.isitecategoryrel.find_first(where=where)

    async def fetch_all(self) -> list[prisma.models.ISiteCategoryRel]:
        """
        Fetches all data from the OrgSite table.

        Returns:
            A list of ISiteCategoryRel objects representing all records in the OrgSite table.
        """
        return await self.prisma.isitecategoryrel.find_many()

    async def create_many(self, data: prisma.types.IOrgSiteCreateInput) -> int:
        """
        Create multiple org sites.

        Args:
            data (prisma.types.IOrgSiteCreateInput): The data to create multiple org sites.

        Returns:
            The number of org sites created.
        """
        await self.prisma.isitecategoryrel.create_many(data=data)

    async def group_by(
        self, count=None, by=None, sum=None, order=None, having=None
    ) -> list[prisma.models.ISiteCategoryRel]:
        """
        A decorator that catches any errors that occur during the execution of the `group_by` function.

        Args:
            count (Optional): The count parameter of the `group_by` function.
            by (Optional): The by parameter of the `group_by` function.
            sum (Optional): The sum parameter of the `group_by` function.
            order (Optional): The order parameter of the `group_by` function.
            having (Optional): The having parameter of the `group_by` function.

        Returns:
            list[prisma.models.ISiteCategoryRel]: A list of `prisma.models.ISiteCategoryRel` objects.
        """
        return await self.prisma.isitecategoryrel.group_by(
            count=count, by=by, sum=sum, order=order, having=having
        )

    async def _fetch_page(
        self, cursor: str, page_size=10
    ) -> tuple[list[prisma.models.ISiteCategoryRel], str]:
        """
        Fetches a page of org sites from the database.

        Args:
            cursor (str): The cursor used for pagination.
            page_size (int, optional): The number of results per page. Defaults to 10.

        Returns:
            Tuple[List[prisma.models.ISiteCategoryRel], str]: A tuple containing a list of org sites
                and the next cursor for pagination.
        """
        results = await self.prisma.isitecategoryrel.find_many(
            take=page_size,
            cursor={"id": cursor} if cursor else None,
            order={"id": "asc"},
        )
        next_cursor = results[-1].id if results else None
        return results, next_cursor

    async def fetch_paged(
        self, take=10, skip=0, order=None
    ) -> list[prisma.models.ISiteCategoryRel]:
        """
        Fetches a paged list of org sites.

        Args:
            take (int): The number of items to take per page.
            skip (int): The number of items to skip.
            order (Optional[str]): The field to order the results by.

        Returns:
            list[prisma.models.ISiteCategoryRel]: The list of org sites.
        """
        results = await self.prisma.isitecategoryrel.find_many(
            take=take, skip=skip, order=order
        )
        return results

    async def fetch_all_paginated(self):
        pass

    async def fetch_count(self) -> int:
        """
        Fetches the count of the ISiteCategoryRel table.

        Returns:
            int: The count of the ISiteCategoryRel table.
        """
        return await self.prisma.isitecategoryrel.count()

    async def calculate_emissions(self, year: int) -> None:
        """
        Calculate emission ratios and emissions for the given site category relations.

        Args:
            relations (list[prisma.models.ISiteCategoryRel]): A list of site category relations.

        Returns:
            None: This function does not return anything.
        """
        date_from = datetime.datetime(year, 1, 1)
        date_to = datetime.datetime(year, 12, 31)
        relations = await self.fetch_some(
            where={"site": {"is": {"operationStartDt": {"lte": date_from}}}},
            include={"site": True},
        )

        if not relations or len(relations) == 0:
            raise Exception("No relations found")
        relations_df = [to_dict(rel) for rel in relations]
        relations_df = pd.DataFrame(relations_df)
        totalContributionMagnitudeInSector = relations_df.groupby("categoryName")[
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
                total_emission = await self.emission_data_service.fetch_one(
                    where={
                        "categoryName": category_name,
                        "periodStartDt": {"gte": date_from},
                        "periodEndDt": {"lte": date_to},
                        "pollutantId": "CO2",
                        "source":"gir4",
                    }
                )
            else:
                category_name = ipcc_to_gir_code.get(
                    get_second_level_category(relation.categoryName)
                )
                total_emission = await self.emission_data_service.group_by(
                    by=["categoryName", "pollutantId"],
                    sum={"emissionTotal": True},
                    having={
                        "categoryName": category_name,
                    },
                    where={
                        "periodStartDt": {"gte": date_from},
                        "periodEndDt": {"lte": date_to},
                        "source": "gir1",
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
            matching_item = totalContributionMagnitudeInSector.loc[category_name]
            if matching_item is not None:
                contributionRatio = (
                    relation.contributionMagnitudeSector / matching_item
                )

                emission = contributionRatio * total_emission_gas
                await self.emission_data_service.update_or_create(
                    data={
                        "categoryName": category_name,
                        "periodStartDt": total_emission.periodStartDt,
                        "periodEndDt": total_emission.periodEndDt,
                        "emissionTotal": emission,
                        "periodLength": total_emission.periodLength,
                        "source": "calc:" + total_emission.source,
                        "regionUid": relation.site.addressRegionUid,
                        "siteUid": relation.siteUid,
                        "pollutantId": total_emission.pollutantId,
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

    # async def api_to_gir_address(self):
    #     """
    #     Converts the API addresses to GIR addresses
    #     """
    #     data = await self.prisma.isitecategoryrel.find_many(where=None, include={"region":True})
    #     data_df = pd.DataFrame.from_records([s.__dict__ for s in data])
    #     data_df["modifiedAddress"] = data_df["structuredAddress"].map(address_dict)
    #     parse_json_fields(["settings", "addressDetail", "additionalProps"], data_df)
    #     data_df.replace(np.nan, None, inplace=True)
    #     dat_dict = data_df.to_dict(orient="records")
    #     for data in tqdm(dat_dict, total=len(dat_dict)):
    #         if data["regionUid"] is not None:
    #             data["region"] = {"connect":{"uid":data["regionUid"]}}
    #         else:
    #             del data["region"]
    #         del data["regionUid"]

    #         await self.update(data=data, where={"uid":data["uid"], })

    # async def find_region_uids(self):
    #     """
    #     finds and matches the regionUids from the modifiedAddress field, in the ISiteCategoryRel table
    #     """
    #     rel = await self.prisma.isitecategoryrel.find_many(where={"regionUid":None})
    #     rel_df = pd.DataFrame.from_records([s.__dict__ for s in rel])
    #     rel_df[["region", "district"]] = rel_df["modifiedAddress"].str.split("|", expand=True)
    #     rel_df[["district", "unmatched"]] = rel_df["district"].str.split(" ", expand=True)
    #     reg = await self.prisma.region.find_many(include={"parent":True}, where={"type":"district"})
    #     reg_df = pd.DataFrame.from_records([s.__dict__ for s in reg])
    #     for rel_idx in tqdm(rel_df.index, total=len(rel_df)):
    #         for reg_idx in reg_df.index:
    #             # r = reg_df["region"][reg_idx]
    #             # f = rel_df["uid"][rel_idx]
    #             if rel_df["district"][rel_idx] == reg_df["name"][reg_idx]:
    #                 test = reg_df["parent"][reg_idx]
    #                 if rel_df["region"][rel_idx] == reg_df["parent"][reg_idx].name:
    #                     await self.update(data={"regionUid":reg_df["uid"][reg_idx]}, where={"uid":rel_df["uid"][rel_idx]})
    #                 print(f"no match for {rel_df['uid'][rel_idx]}: {rel_df['modifiedAddress'][rel_idx]}")
