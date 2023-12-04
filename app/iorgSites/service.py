from typing_extensions import Buffer
import hashlib
import numpy as np
from tqdm import tqdm
from utils.file import read_to_pd
import prisma
from utils.file_type import return_list
from database import get_connection
from config.column_mapping import iorgsite_map
import pandas as pd
from app.foundation.exception import CatchError

##Using service directly causes circular import error


class FactoryOnSiteService:
    def __init__(self):
        self.prisma = get_connection()

    @CatchError
    async def delete_all(self):
        """
        Deletes all records in the 'iorgsite' table.
        """
        await self.prisma.iorgsite.delete_many()

    @CatchError
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
            await self.prisma.iorgsite.update(
                where={"uid": existing_record.uid}, data=data
            )
        else:
            await self.prisma.iorgsite.create(data=data)

    @CatchError
    async def upsert(
        self,
        data: prisma.types.IOrgSiteCreateInput,
        where: prisma.types.IOrgSiteWhereUniqueInput,
        include=None,
    ):
        await self.prisma.iorgsite.upsert(data=data, where=where)
        """
        Upserts an organization site in the database.

        Args:
            data (prisma.types.IOrgSiteCreateInput): The data to be upserted.
            where (prisma.types.IOrgSiteWhereUniqueInput): The unique identifier of the organization site.
            include (Optional): The related models and fields to include in the upsert operation.

        Returns:
            None
        """

    @CatchError
    @return_list
    async def create(self, data: prisma.types.IOrgSiteCreateInput) -> None:
        """
        Creates a new org site with the given data.

        Parameters:
            - data: An instance of prisma.types.IOrgSiteCreateInput representing the data for the new org site.

        Returns:
            None
        """
        await self.prisma.iorgsite.create(data=data)

    @CatchError
    @return_list
    async def update(
        self, data: prisma.models.IOrgSite, where: prisma.types.IOrgSiteWhereUniqueInput
    ) -> None:
        """
        Update the given organization site with the provided data.

        Args:
            data (prisma.models.IOrgSite): The data to update the organization site with.
            where (prisma.types.IOrgSiteWhereUniqueInput): The unique identifier for the organization site.

        Returns:
            None
        """
        await self.prisma.iorgsite.update(where=where, data=data)

    @CatchError
    async def delete(self, where: prisma.types.IOrgSiteWhereInput) -> None:
        """
        Deletes a record from the OrgSite table based on the given criteria.

        Parameters:
            where (prisma.types.IOrgSiteWhereInput): The criteria used to determine which records to delete.

        Returns:
            None
        """
        await self.prisma.iorgsite.delete(where=where)

    @CatchError
    async def fetch_some(
        self, where: prisma.types.IOrgSiteWhereInput
    ) -> list[prisma.models.IOrgSite]:
        """
        Fetches some data based on the given where clause.

        Args:
            where: An input object type that represents the conditions used to filter the data.

        Returns:
            A list of IOrgSite objects that match the given conditions.
        """
        return await self.prisma.iorgsite.find_first(where=where)

    @CatchError
    async def fetch_all(self) -> list[prisma.models.IOrgSite]:
        """
        Fetches all data from the OrgSite table.
        
        Returns:
            A list of IOrgSite objects representing all records in the OrgSite table.
        """
        return await self.prisma.iorgsite.find_many()

    @CatchError
    @return_list
    async def create_many(self, data: prisma.types.IOrgSiteCreateInput) -> None:
        """
        Create multiple org sites.

        Args:
            data (prisma.types.IOrgSiteCreateInput): The data to create multiple org sites.

        Returns:
            None: This function does not return anything.
        """
        await self.prisma.iorgsite.create_many(data=data)

    @CatchError
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

    @CatchError
    async def _fetch_page(
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
            cursor={"id": cursor} if cursor else None,
            order={"id": "asc"},
        )
        next_cursor = results[-1].id if results else None
        return results, next_cursor

    @CatchError
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

    @CatchError
    async def fetch_all_paginated(self):
        pass

    @CatchError
    async def fetch_count(self) -> int:
        """
        Fetches the count of the iorgsite table.

        Returns:
            int: The count of the iorgsite table.
        """
        return await self.prisma.iorgsite.count()

    # Business logic
    @CatchError
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
        # print (hashlib.sha256(combined.encode()).hexdigest())
        return hashlib.sha256(combined.encode()).hexdigest()

    @CatchError
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

    @CatchError
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
        source = await read_to_pd(buffer=buffer, path=path)
        source["dataSource"] = data_source
        source = self.transform_data(source)
        source["keyHash"] = source.apply(lambda row: self.hash_row(row), axis=1)
        for index, row in tqdm(source.iterrows(), total=len(source)):
            await self.upsert(data=row.to_dict(), where={"keyHash": row["keyHash"]})
