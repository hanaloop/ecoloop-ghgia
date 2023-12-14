import json
import logging
from typing import AsyncIterator
from typing_extensions import Buffer
import hashlib
import numpy as np
from pydantic import Json
from tqdm import tqdm
from app.utils.file import FileUtils
import prisma
from app.utils.file_type import return_list
from app.database import get_connection
from app.config.column_mapping import iorgsite_map
import pandas as pd
from app.foundation.exception import catch_errors_decorator
from app.requests.service import RequestService
from app.config.env_config import KAKAO_API_BURL, KAKAO_API_KEY
from prisma import Json
from app.config.column_mapping import code_dict
from app.isitecategoryrels.service import ISiteCategoryRelService
from app.utils.string import get_second_level_category, get_category_list
from app.config.column_mapping import address_dict
from app.iorgsites.adapters.address_adapter import format_address_string


class IOrgSiteService:
    def __init__(self):
        self.prisma = get_connection()
        self.requests = RequestService()
        self.rel_service = ISiteCategoryRelService()

    @catch_errors_decorator
    async def delete_all(self):
        """
        Deletes all records in the 'iorgsite' table.
        """
        return await self.prisma.iorgsite.delete_many()

    @catch_errors_decorator
    async def update_or_create(
        self, data: prisma.models.IOrgSite, where: prisma.types.IOrgSiteWhereInput
    ):
        """
        Update or create a record in the database based on the given data and where condition.

        Args:
            data (prisma.models.IOrgSite): The data to update or create the record with.
            where (prisma.types.IOrgSiteWhereInput): The condition to search for an existing record.

        Returns:
            None
        """
        existing_record = await self.prisma.iorgsite.find_first(where=where)

        if existing_record:
            return await self.prisma.iorgsite.update(
                where={"uid": existing_record.uid}, data=data
            )
        else:
            return await self.prisma.iorgsite.create(data=data)

    @catch_errors_decorator
    async def upsert(
        self,
        data: prisma.types.IOrgSiteCreateInput,
        where: prisma.types.IOrgSiteWhereUniqueInput,
        include=None,
    )-> prisma.models.IOrgSite | None:
        """
        Upserts an organization site in the database.

        Args:
            data (prisma.types.IOrgSiteCreateInput): The data to be upserted.
            where (prisma.types.IOrgSiteWhereUniqueInput): The unique identifier of the organization site.
            include (Optional): The related models and fields to include in the upsert operation.

        Returns:
            None
        """
        return await self.prisma.iorgsite.upsert(
            data={"create": data, "update": data}, where=where
        )

    @catch_errors_decorator
    @return_list
    async def create(self, data: prisma.types.IOrgSiteCreateInput) -> None:
        """
        Creates a new org site with the given data.

        Parameters:
            - data: An instance of prisma.types.IOrgSiteCreateInput representing the data for the new org site.

        Returns:
            None
        """
        return await self.prisma.iorgsite.create(data=data)

    @catch_errors_decorator
    @return_list
    async def update(
        self, data: prisma.models.IOrgSite, where: prisma.types.IOrgSiteWhereUniqueInput
    ) -> prisma.models.IOrgSite:
        """
        Update the given organization site with the provided data.

        Args:
            data (prisma.models.IOrgSite): The data to update the organization site with.
            where (prisma.types.IOrgSiteWhereUniqueInput): The unique identifier for the organization site.

        Returns:
            None
        """
        return await self.prisma.iorgsite.update(where=where, data=data)

    @catch_errors_decorator
    async def delete(self, where: prisma.types.IOrgSiteWhereInput) -> None:
        """
        Deletes a record from the OrgSite table based on the given criteria.

        Parameters:
            where (prisma.types.IOrgSiteWhereInput): The criteria used to determine which records to delete.

        Returns:
            None
        """
        return await self.prisma.iorgsite.delete(where=where)

    @catch_errors_decorator
    async def find_many(
        self,
        where: prisma.types.IOrgSiteWhereInput,
        include: prisma.types.IOrgSiteInclude | None = None,
        order: prisma.types.IOrgSiteOrderByInput
        | list[prisma.types.IOrgSiteOrderByInput]
        | None = None,
    ) -> list[prisma.models.IOrgSite]:
        """
        Fetches some data based on the given where clause.

        Args:
            where: An input object type that represents the conditions used to filter the data.

        Returns:
            A list of IOrgSite objects that match the given conditions.
        """
        return await self.prisma.iorgsite.find_many(
            where=where, include=include, order=order
        )

    @catch_errors_decorator
    async def fetch_all(self) -> list[prisma.models.IOrgSite]:
        """
        Fetches all data from the OrgSite table.

        Returns:
            A list of IOrgSite objects representing all records in the OrgSite table.
        """
        return await self.prisma.iorgsite.find_many()

    @catch_errors_decorator
    @return_list
    async def create_many(self, data: prisma.types.IOrgSiteCreateInput) -> None:
        """
        Create multiple org sites.

        Args:
            data (prisma.types.IOrgSiteCreateInput): The data to create multiple org sites.

        Returns:
            None: This function does not return anything.
        """
        return await self.prisma.iorgsite.create_many(data=data)

    @catch_errors_decorator
    async def group_by(
        self, count=None, by=None, sum=None, order=None, having=None
    ) -> list[prisma.models.IOrgSite]:
        """
        A decorator that catches any errors that occur during the execution of the `group_by` function.

        Args:
            count (Optional): The count parameter of the `group_by` function.
            by (Optional): The by parameter of the `group_by` function.
            sum (Optional): The sum parameter of the `group_by` function.
            order (Optional): The order parameter of the `group_by` function.
            having (Optional): The having parameter of the `group_by` function.

        Returns:
            list[prisma.models.IOrgSite]: A list of `prisma.models.IOrgSite` objects.
        """
        return await self.prisma.iorgsite.group_by(
            count=count, by=by, sum=sum, order=order, having=having
        )

    @catch_errors_decorator
    async def _fetch_page( ##TODO: Make sure this works
        self, cursor: str, page_size=10
    ) -> tuple[list[prisma.models.IOrgSite], str]:
        """
        Fetches a page of org sites from the database.

        Args:
            cursor (str): The cursor used for pagination.
            page_size (int, optional): The number of results per page. Defaults to 10.

        Returns:
            Tuple[List[prisma.models.IOrgSite], str]: A tuple containing a list of org sites
                and the next cursor for pagination.
        """
        results = await self.prisma.iorgsite.find_many(
            take=page_size,
            cursor={"uid": cursor} if cursor else None,
            order={"sid": "asc"},
        )
        next_cursor = results[-1].uid if results else None
        return results, next_cursor

    @catch_errors_decorator
    async def fetch_paged(
        self, take=10, skip=0, order=None
    ) -> list[prisma.models.IOrgSite]:
        """
        Fetches a paged list of org sites.

        Args:
            take (int): The number of items to take per page.
            skip (int): The number of items to skip.
            order (Optional[str]): The field to order the results by.

        Returns:
            list[prisma.models.IOrgSite]: The list of org sites.
        """
        results = await self.prisma.iorgsite.find_many(
            take=take, skip=skip, order=order
        )
        return results

    @catch_errors_decorator
    async def fetch_all_paginated(self, page_size=10) -> AsyncIterator[list[prisma.models.IOrgSite]]:
        cursor = None
        while True:
            results, cursor = await self._fetch_page(cursor = cursor, page_size=page_size)
            if not results:
                break
            yield results

    @catch_errors_decorator
    async def fetch_count(self) -> int:
        """
        Fetches the count of the iorgsite table.

        Returns:
            int: The count of the iorgsite table.
        """
        return await self.prisma.iorgsite.count()

    # Business logic
    @catch_errors_decorator
    def hash_row(self, row: pd.Series) -> str:
        """
        Hashes the row to create a unique key

        Args:
            row (_type_): _description_

        Returns:
            str: _description_
        """
        combined = (
            str(row["businessRegistrationNum"])
            + str(row["companyName"])
            + str(row["landAddress"])
        )
        # print (hashlib.sha256(combined.encode()).hexdigest())e
        return hashlib.sha256(combined.encode()).hexdigest()

    @catch_errors_decorator
    def transform_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforms the given DataFrame by renaming columns based on the `iorgsite_map` dictionary. Then, it replaces "-" with `None` in specific columns and converts them to datetime objects. Finally, it converts the "sectorIdMain" and "factoryManagementNumber" columns to strings.

        Parameters:
        - df (pd.DataFrame): The input DataFrame to be transformed.

        Returns:
        - pd.DataFrame: The transformed DataFrame.
        """
        newDf = df.rename(columns=iorgsite_map)
        for col in [
            "approvalDate",
            "registrationDate",
            "registrationDateInitial",
            "approvalDateInitial",
        ]:
            newDf[col] = newDf[col].replace("-", None, inplace=True)
            newDf[col] = pd.to_datetime(newDf[col]).replace(
                {np.nan: None}, inplace=True
            )
        newDf["sectorIdMain"] = newDf["sectorIdMain"].astype(str)
        newDf["factoryManagementNumber"] = newDf["factoryManagementNumber"].astype(str)
        return newDf

    @catch_errors_decorator
    async def upload_iorgsites(
        self, data_source: str, buffer: Buffer = None, path: str = None
    ) -> None:
        """
        Uploads data from a given data source to the iorgsites table.

        Parameters:
            - data_source (str): The source of the data to be uploaded.
            - buffer (Buffer, optional): A buffer containing the data. Defaults to None.
            - path (str, optional): The path to the file containing the data. Defaults to None.

        Returns:
            None
        """
        files = FileUtils()
        source = await files.read_to_pd(data_source, file=buffer, path=path)
        source["dataSource"] = data_source
        source = self.transform_data(source)
        source["keyHash"] = source.apply(lambda row: self.hash_row(row), axis=1)
        upserted_data = []
        for index, row in tqdm(source.iterrows(), total=len(source)):
            upserted_row = await self.upsert(data=row.to_dict(), where={"keyHash": row["keyHash"]})
            upserted_data.append(upserted_row)
            # await self.populate_single_address(site=upserted_row) # Could also do this here but it will take long time with the rate limit
            # await self.update_relation_single(site=upserted_row)
        return upserted_data

    async def get_site_structured_address(self, site: prisma.models.IOrgSite) -> tuple:
        request_addr = site.streetAddress or site.landAddress
        request_addr = format_address_string(request_addr)
        response = await self.requests.request(
            KAKAO_API_BURL,
            headers={"Authorization": f"KakaoAK {KAKAO_API_KEY}"},
            params={
                "query": request_addr,
            },
        )
        api_loc_response = json.loads(response.text)
        
        if api_loc_response.get("meta").get("total_count") == 0 and site.landAddress:
            request_addr = format_address_string(site.landAddress)
            response = await self.requests.request(
                KAKAO_API_BURL,
                headers={"Authorization": f"KakaoAK {KAKAO_API_KEY}"},
                params={
                    "query": request_addr,
                },
            )
            api_loc_response = json.loads(response.text)
        if api_loc_response.get("meta").get("total_count") == 0:
            try:
                region1 = request_addr.split(" ")[0]
                region2 = request_addr.split(" ")[1]
                region1.strip()
                region2.strip()
                address_detail = {"type":"auto_parsed"}
            except:
                return None, None
        else:
            region1 = api_loc_response.get("documents")[0].get("address", {}).get("region_1depth_name")
            region2 = api_loc_response.get("documents")[0].get("address", {}).get("region_2depth_name")
            address_detail = api_loc_response.get("documents")[0] if api_loc_response.get("documents") else None

            if region1 is None or region2 is None:
                return None, None

        structured_address = f"{region1}|{region2}"
        return structured_address, address_detail

    @catch_errors_decorator
    async def populate_addresses(self) -> None:
        """
        Asynchronously populates addresses.

        Returns:
            None

        Raises:
            Exception: If an error occurs during the population of addresses.
        """
        sites = await self.find_many(where={"structuredAddress": None})
        for site in tqdm(sites, total=len(sites)):
            await self.populate_single_address(site)

    @catch_errors_decorator
    async def populate_single_address(
        self, uid: str= None, site: prisma.models.IOrgSite = None
    ) -> None:
        """
        Populates a single address for a given site.

        Parameters:
            - site (prisma.models.IOrgSite): The site for which to populate the address.

        Returns:
            None
        """
        if site is None:
            site = await self.prisma.iorgsite.find_unique(where={"uid": uid})
        elif uid is None:
            uid = site.uid
        structured_address, address_detail = await self.get_site_structured_address(
            site
        )
        return await self.prisma.iorgsite.update(
            where={"uid": site.uid},
            data={
                "structuredAddress": address_dict.get(structured_address) or structured_address,
                "addressDetails": Json(address_detail),
            },
        )

    async def update_relation_single(self, uid: str = None, site: prisma.models.IOrgSite = None) -> None:
        """
        Creates (or Updates) relation per category level of a single site in the database.

        Args:
            uid (str, optional): The UID of the site. Defaults to None.
            site (prisma.models.IOrgSite, optional): The site object. Defaults to None.

        Raises:
            Exception: Raised if neither site nor uid is provided.

        Returns:
            None: This function does not return anything.
        """
        if not site and not uid:
            raise Exception("Either site or uid must be provided")

        if not uid:
            uid = site.uid
        elif not site:
            site = await self.prisma.iorgsite.find_unique(where={"uid": uid})

        if site.sectorIds and site.sectorIdMain:
            proxy_field = site.buildingArea #This is just for comparison purposes, change to manufacturingFacilityArea
            if proxy_field <= 0:
                logging.warn(f"Skipping {uid} as proxy field is <= 0")
                return
            sectors = site.sectorIds.split(",")
            sector_count = len(sectors)
            contribution_magnitude = proxy_field / sector_count

            await self.rel_service.delete_many(where={"siteUid": uid}) #TODO: This is slower but we need to have this in order to account for chancing sectorids
            for sector in sectors:
                sector = sector.strip()
                sector_conv = code_dict.get(sector)
                category_list = get_category_list(sector_conv, return_lvl_from=2, return_lvl_to=3) if sector_conv else []
                for category in category_list:
                    lvl = len(category.split("."))
                    relation_obj = {
                        "siteUid": uid,
                        "sectorId": sector,
                        "contributionMagnitudeSector": contribution_magnitude,
                        "categoryName": category,
                        "siteAddress": site.structuredAddress,
                        "isMainSector": site.sectorIdMain == sector,
                        "categoryLevel": lvl,
                        "structuredAddress": site.structuredAddress,
                    }
                    # At the moment we are always creating as we delete (see above)
                    await self.rel_service.update_or_create(
                        data=relation_obj,
                        where={"siteUid": uid, "sectorId": relation_obj["sectorId"], 'categoryLevel': lvl},
                    )

    async def update_relations(self) -> None:
        """
        Updates the relations between sites and calculates emission ratios.

        This function iterates over all the sites in the database and updates their relations
        by calling the `update_relation_single` method for each site. If any relations are updated,
        it then calls the `calculate_emission_ratios` method of the `rel_service` to calculate the
        emission ratios. This function is quite slow, so the alternative function should be used
        if it is not necessary to create relations for all sites, even if they do not have mapped
        sectors.

        Parameters:
            None

        Returns:
            None
        """
        site_count = await self.prisma.iorgsite.count()
        pbar = tqdm(total=site_count)
        
        async for sites in self.fetch_all_paginated(page_size=100):
            for site in sites:
                rels = await self.update_relation_single(site=site)
                if rels:
                    await self.rel_service.calculate_emission_ratios(rels)
                pbar.update(1)
        
        pbar.close()

    async def update_site_dependency(self, uid: str) -> None:
        """
        Updates the site dependency with the given UID.

        Args:
            uid (str): The UID of the site.

        Returns:
            None: This function does not return anything.
        """
        site =  await self.find_many(where={"uid": uid})
        if site:
            rel = await self.update_relation_single(site=site[0])
            if rel:
                await self.rel_service.calculate_emission_ratios(rel)

    async def update_relations_alt(self)-> None:
        """
        Update the relations of the object asynchronously. This is the alternative version of this function
        since it only fetches the sites that are include mapped sectors.

        :return: None
        """
        # sites = await self.prisma.query_raw(
        #     query = f"""
        #     SELECT *
        #     FROM "IOrgSite"
        #     WHERE "sectorIds" ~ ('(^|\s*,\s*)(' || array_to_string(ARRAY{list(code_dict.keys())}::text[], '|') || ')(\s*,|$)') AND "structuredAddress" IS  NULL;
        #     """, model=prisma.models.IOrgSite
        # )
        # for site in tqdm(sites, total=len(sites), desc="Updating relations"):
        #     # await self.update_relation_single(site=site)
        #     await self.populate_single_address(site=site)
        rels = await self.rel_service.fetch_some(where=  {   "NOT": {"categoryName": None}})
        await self.rel_service.calculate_emission_ratios(rels)



    