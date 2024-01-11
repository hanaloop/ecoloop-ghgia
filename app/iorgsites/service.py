from datetime import datetime
import json
import logging
import os
from typing import AsyncIterator
from typing_extensions import Buffer
import hashlib
import numpy as np
from pydantic import Json
from tqdm import tqdm
from app.emission_data.service import IEmissionDataService
from app.region.service import RegionService
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
from app.config.column_mapping import ipcc_to_gir
from app.isitecategoryrels.service import ISiteCategoryRelService
from app.utils.string import get_category_list
from app.config.column_mapping import address_dict
from app.iorgsites.adapters.adapter_address import fix_address_string
from app.utils.string import get_coords_from_detail, get_regions_as_tuple
from app.utils.data_types import parse_to_date


class IOrgSiteService:
    def __init__(self):
        self.prisma = get_connection()
        self.region_service = RegionService()
        self.requests = RequestService()
        self.rel_service = ISiteCategoryRelService()
        self.emission_service = IEmissionDataService()


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

    @return_list
    async def create(self, data: prisma.types.IOrgSiteCreateInput) -> prisma.models.IOrgSite | None:
        """
        Creates a new org site with the given data.

        Parameters:
            - data: An instance of prisma.types.IOrgSiteCreateInput representing the data for the new org site.

        Returns:
            None
        """
        return await self.prisma.iorgsite.create(data=data)


    async def update(
        self, data: prisma.models.IOrgSite, where: prisma.types.IOrgSiteWhereUniqueInput, include: prisma.types.IOrgSiteInclude | None = None
    ) ->  prisma.models.IOrgSite | None:
        """
        Update the given organization site with the provided data.

        Args:
            data (prisma.models.IOrgSite): The data to update the organization site with.
            where (prisma.types.IOrgSiteWhereUniqueInput): The unique identifier for the organization site.

        Returns:
            None
        """
        return await self.prisma.iorgsite.update(where=where, data=data, include=include)

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

    async def fetch_one(self, where: prisma.types.IOrgSiteWhereInput, include: prisma.types.IOrgSiteInclude | None = None) -> prisma.models.IOrgSite | None:
        """
        Fetches one record from the 'OrgSite' table based on the given where clause.

        Args:
            where (prisma.types.IOrgSiteWhereInput): The unique identifier of the record to fetch.

        Returns:
            A IOrgSite object representing the fetched record.
        """
        return await self.prisma.iorgsite.find_first(where=where, include=include)

    async def fetch_some(
        self, where: prisma.types.IOrgSiteWhereInput, include: prisma.types.IOrgSiteInclude | None = None
    ) -> list[prisma.models.IOrgSite]:
        """
        Fetches some data based on the given where clause.

        Args:
            where: An input object type that represents the conditions used to filter the data.

        Returns:
            A list of IOrgSite objects that match the given conditions.
        """
        return await self.prisma.iorgsite.find_many(where=where, include=include)
    
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
        self, take=10, skip=0, order=None, where=None, include=None
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
            take=take, skip=skip, order=order, where=where, include=include
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
    def hash_row(self, row: pd.Series | dict) -> str:
        """
        Hashes the row to create a unique key

        Args:
            row (_type_): _description_

        Returns:
            str: _description_
        """
        if "factoryManagementNumber" not in row or "companyName" not in row or "landAddress" not in row:
            raise ValueError("Row must contain factoryManagementNumber, companyName, landAddress")
        combined = (
            str(row["factoryManagementNumber"])
            + str(row["companyName"])
            + str(row["landAddress"])
        )
        # print (hashlib.sha256(combined.encode()).hexdigest())e
        return hashlib.sha256(combined.encode()).hexdigest()

    def transform_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforms the given DataFrame by renaming columns based on the `iorgsite_map` dictionary. Then, it replaces "-" with `None` in specific columns and converts them to datetime objects. Finally, it converts the "sectorIdMain" and "factoryManagementNumber" columns to strings.

        Parameters:
        - df (pd.DataFrame): The input DataFrame to be transformed.

        Returns:
        - pd.DataFrame: The transformed DataFrame.
        """
        newDf = df.rename(columns=iorgsite_map)
        newDf = newDf[newDf.columns.intersection(iorgsite_map.values())] ##TODO: Check if they exist first
        for col in [
            "registrationDate",
            "registrationDateInitial",
            "approvalDateInitial",
        ]:
            newDf[col] = newDf[col].replace("-", None)
            ## Something weird is going on with the column types here, while there is NaNs in the date columns, they cannot be replaced
            ## with None. So that makes it difficult to convert them to datetime. At the same time, the actual numeric values, somehow turn into
            ## floats. Must investigate why this is happening.
            newDf[col] = newDf[col].where(pd.notnull(newDf[col]), None)
            newDf[col] = newDf[col].apply(lambda x: parse_to_date(x, dt_boundary_from=datetime(1910, 1, 1), dt_boundary_to=datetime.now())) 
            newDf[col].replace(
                {np.nan: None}, inplace=True)
        newDf["sectorIdMain"] = newDf["sectorIdMain"].astype(str)
        newDf['factoryManagementNumber'] = newDf['factoryManagementNumber'].astype(str)
        newDf['operationStartDt'] = newDf['registrationDateInitial'] ##For now it is the same, later we can change this when we have other data
        return newDf

    @catch_errors_decorator
    async def upload_iorgsites(
        self, buffer: Buffer = None, path: str = None
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
        if buffer and not path:
            data_source = "web"
        elif path and not buffer:
            data_source = os.path.basename(path)
        files = FileUtils()
        source = await files.read_to_pd(data_source, file=buffer, path=path)
        source = self.transform_data(source)
        source["dataSource"] = data_source
        source["keyHash"] = source.apply(lambda row: self.hash_row(row), axis=1)
        upserted_data = []
        # Reason I iterate through the index although it is not used, is because otherwise iterrows returns a tuple,
        # which means I have to destructure it later
        for index, row in tqdm(source.iterrows(), total=len(source)):
            await self.upsert(data=row.to_dict(), where={"keyHash": row["keyHash"]})
        await self.update_relations_alt()
        return upserted_data

    async def get_site_structured_address(self, site: prisma.models.IOrgSite) -> tuple:
        request_addr = (site.streetAddress).strip() or site.landAddress.strip()
        request_addr = fix_address_string(request_addr)
        response = await self.requests.request(
            KAKAO_API_BURL,
            headers={"Authorization": f"KakaoAK {KAKAO_API_KEY}"},
            params={
                "query": request_addr,
            },
        )
        api_loc_response = json.loads(response.text)
        
        if api_loc_response.get("meta").get("total_count") == 0 and site.landAddress:
            request_addr = fix_address_string(site.landAddress)
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

    #TODO: Seems like there is empty strings in the xlsx file. Clear them when importing
    @catch_errors_decorator
    async def populate_single_address(
        self, uid: str= None, site: prisma.models.IOrgSite = None
    ) -> prisma.models.IOrgSite | None:
        """
        Populates a single address for a given site.

        Parameters:
            - site (prisma.models.IOrgSite): The site for which to populate the address.

        Returns:
            prisma.models.IOrgSite | None: The updated site object.
        """
        if not site and not uid:
            raise Exception("Neither site nor uid is provided.")
        if site is None:
            site = await self.prisma.iorgsite.find_unique(where={"uid": uid})
        elif uid is None:
            uid = site.uid
        structured_address, address_detail = await self.get_site_structured_address(
            site
        )
        latitude, longitude = get_coords_from_detail(address_detail)
        if not address_detail.get("type") == "auto_parsed":
            region, subregion = get_regions_as_tuple(address_dict.get(structured_address))
        else:
            region, subregion = get_regions_as_tuple(structured_address)
        site.addressRegionName = region or None
        site.addressSubRegion = subregion or None
        if region and subregion:
            site = await self.connect_address(site)
        if latitude is None or longitude is None:
            latitude, longitude = site.addressRegion.latitude if site.addressRegion else None, site.addressRegion.longitude if site.addressRegion else None
        return await self.prisma.iorgsite.update(
            where={"uid": site.uid},
            data={
                "structuredAddress": address_dict.get(structured_address) or structured_address,
                "addressDetails": Json(address_detail),
                "latitude": float(latitude) if latitude is not None else None,
                "longitude": float(longitude) if longitude is not None else None,
                "addressRegionName": region,
                "addressSubRegion": subregion
            },
        )

    async def connect_address(self, site: prisma.models.IOrgSite) -> None:
        """
        Connects an organization site with its address.

        Args:
            site (prisma.models.IOrgSite): The organization site to connect.

        Returns:
            None
        """
        # district = get_parent_region(site.addressRegionName) if site.addressRegionName else None

        # if not district:
        #     return

        # FOR SOME REASON INTELLISENSE GAVE ERROR WITH THIS COMMENT region = get_parent_region(site.addressRegionName) if site.addressRegionName else None
        addressRegion = await self.region_service.fetch_one(
            where={
                "name": site.addressSubRegion,
                "parent": {
                    "is": {"name": site.addressRegionName}
                }
            }
        )

        if addressRegion is None:
            return site

        return  await self.update(
            data={"addressRegionUid": addressRegion.uid}, where={"uid": site.uid}, include={"addressRegion": True}
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
                sector_conv = ipcc_to_gir.get(sector)
                category_list = get_category_list(sector_conv, return_lvl_from=2, return_lvl_to=3) if sector_conv else []
                for category in category_list:
                    lvl = len(category.split("."))
                    relation_obj = {
                        "siteUid": uid,
                        "sectorId": sector,
                        "contributionMagnitudeSector": contribution_magnitude,
                        "categoryName": category,
                        "siteAddress": site.structuredAddress,
                        "isMainSector": site.sectorIdMain == sector if site.sectorIdMain and site.sectorIdMain else None,
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
                    await self.emission_service.calc_emissions_dt_range(rels)
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
        site =  await self.fetch_one(where={"uid": uid})
        if site:
            rel = await self.update_relation_single(site=site)
            await self.populate_single_address(site=site)
            if rel:
                await self.emission_service.calc_emissions_dt_range(rel)

    async def update_relations_alt(self)-> None:
        """
        Update the relations of the object asynchronously. This is the alternative version of this function
        since it only fetches the sites that are include mapped sectors.

        :return: None
        """
        sites = await self.prisma.query_raw(
            query = f"""
            SELECT *
            FROM "IOrgSite"
            WHERE "sectorIds" ~ ('(^|\s*,\s*)(' || array_to_string(ARRAY{list(ipcc_to_gir.keys())}::text[], '|') || ')(\s*,|$)');
            """, model=prisma.models.IOrgSite
        )
        for site in tqdm(sites, total=len(sites), desc="Updating relations"):
            await self.populate_single_address(site=site)
            await self.update_relation_single(site=site)

    async def add_site(self, site: prisma.models.IOrgSite) -> None:
        try:
            site["keyHash"] = self.hash_row(site)
            site = await self.prisma.iorgsite.create(data=site)
            if site.structuredAddress is None:
                site = await self.populate_single_address(site=site)
            await self.update_relation_single(site=site)
        except Exception as e:
            return e
