from typing_extensions import Buffer
import pandas as pd
import prisma
from app.utils.file_type import return_list
from app.database import get_connection
from app.iorganizations.models import DartApiRequest
from app.foundation.exception import CatchError
from app.foundation.api_fetch import fetch_from_url
from tqdm import tqdm
from app.utils.file import FileUtils
from app.config.column_mapping import iorganization_map


class iOrganizationService:
    def __init__(self):
        self.prisma = get_connection()

    @CatchError
    async def delete_all(self):
        """
        Deletes all records in the 'IOrganization' table.
        """
        await self.prisma.iorganization.delete_many()

    @CatchError
    async def update_or_create(
        self,
        data: prisma.models.IOrganization,
        where: prisma.types.IOrganizationWhereInput,
    ):
        """
        Update or create a record in the database based on the given data and where condition.

        Args:
            data (prisma.models.IOrganization): The data to update or create the record with.
            where (prisma.types.IOrganizationWhereInput): The condition to search for an existing record.

        Returns:
            None
        """
        existing_record = await self.prisma.iorganization.find_first(where=where)

        if existing_record:
            await self.prisma.iorganization.update(
                where={"uid": existing_record.uid}, data=data
            )
        else:
            await self.prisma.iorganization.create(data=data)

    @CatchError
    async def upsert(
        self,
        data: prisma.types.IOrganizationCreateInput,
        where: prisma.types.IOrganizationWhereUniqueInput,
        include=None,
    ):
        """
        Upserts an organization in the database.

        Args:
            data (prisma.types.IOrganizationCreateInput): The data to be upserted.
            where (prisma.types.IOrganizationWhereUniqueInput): The unique identifier of the organization.
            include (Optional): The related models and fields to include in the upsert operation.

        Returns:
            None
        """
        await self.prisma.iorganization.upsert(
            data={"create": data, "update": data}, where=where
        )

    @CatchError
    @return_list
    async def create(self, data: prisma.types.IOrganizationCreateInput) -> None:
        """
        Creates a new organization with the given data.

        Parameters:
            - data: An instance of prisma.types.IOrganizationCreateInput representing the data for the new organization.

        Returns:
            None
        """
        await self.prisma.iorganization.create(data=data)

    @CatchError
    @return_list
    async def update(
        self,
        data: prisma.models.IOrganization,
        where: prisma.types.IOrganizationWhereUniqueInput,
    ) -> None:
        """
        Update the given organization with the provided data.

        Args:
            data (prisma.models.IOrganization): The data to update the organization with.
            where (prisma.types.IOrganizationWhereUniqueInput): The unique identifier for the organization.

        Returns:
            None
        """
        await self.prisma.iorganization.update(where=where, data=data)

    @CatchError
    async def delete(self, where: prisma.types.IOrganizationWhereInput) -> None:
        """
        Deletes a record from the OrgSite table based on the given criteria.

        Parameters:
            where (prisma.types.IOrganizationWhereInput): The criteria used to determine which records to delete.

        Returns:
            None
        """
        await self.prisma.iorganization.delete(where=where)

    @CatchError
    async def fetch_some(
        self, where: prisma.types.IOrganizationWhereInput
    ) -> list[prisma.models.IOrganization]:
        """
        Fetches some data based on the given where clause.

        Args:
            where: An input object type that represents the conditions used to filter the data.

        Returns:
            A list of IOrganization objects that match the given conditions.
        """
        return await self.prisma.iorganization.find_first(where=where)

    @CatchError
    async def fetch_all(self) -> list[prisma.models.IOrganization]:
        """
        Fetches all data from the OrgSite table.

        Returns:
            A list of IOrganization objects representing all records in the OrgSite table.
        """
        return await self.prisma.iorganization.find_many()

    @CatchError
    @return_list
    async def create_many(self, data: prisma.types.IOrganizationCreateInput) -> None:
        """
        Create multiple organizations.

        Args:
            data (prisma.types.IOrganizationCreateInput): The data to create multiple organizations.

        Returns:
            None: This function does not return anything.
        """
        await self.prisma.iorganization.create_many(data=data)

    @CatchError
    async def group_by(
        self, count=None, by=None, sum=None, order=None, having=None
    ) -> list[prisma.models.IOrganization]:
        """
        A decorator that catches any errors that occur during the execution of the `group_by` function.

        Args:
            count (Optional): The count parameter of the `group_by` function.
            by (Optional): The by parameter of the `group_by` function.
            sum (Optional): The sum parameter of the `group_by` function.
            order (Optional): The order parameter of the `group_by` function.
            having (Optional): The having parameter of the `group_by` function.

        Returns:
            list[prisma.models.IOrganization]: A list of `prisma.models.IOrganization` objects.
        """
        return await self.prisma.iorganization.group_by(
            count=count, by=by, sum=sum, order=order, having=having
        )

    @CatchError
    async def _fetch_page(
        self, cursor: str, page_size=10
    ) -> tuple[list[prisma.models.IOrganization], str]:
        """
        Fetches a page of organizations from the database.

        Args:
            cursor (str): The cursor used for pagination.
            page_size (int, optional): The number of results per page. Defaults to 10.

        Returns:
            Tuple[List[prisma.models.IOrganization], str]: A tuple containing a list of organizations
                and the next cursor for pagination.
        """
        results = await self.prisma.iorganization.find_many(
            take=page_size,
            cursor={"id": cursor} if cursor else None,
            order={"id": "asc"},
        )
        next_cursor = results[-1].id if results else None
        return results, next_cursor

    @CatchError
    async def fetch_paged(
        self, take=10, skip=0, order=None
    ) -> list[prisma.models.IOrganization]:
        """
        Fetches a paged list of organizations.

        Args:
            take (int): The number of items to take per page.
            skip (int): The number of items to skip.
            order (Optional[str]): The field to order the results by.

        Returns:
            list[prisma.models.IOrganization]: The list of organizations.
        """
        results = await self.prisma.iorganization.find_many(
            take=take, skip=skip, order=order
        )
        return results

    @CatchError
    async def fetch_all_paginated(self):
        pass

    @CatchError
    async def fetch_count(self) -> int:
        """
        Fetches the count of the IOrganization table.

        Returns:
            int: The count of the IOrganization table.
        """
        return await self.prisma.iorganization.count()

    # Business logic

    @CatchError
    async def upload_organizations(
        self, data_source: str, buffer: Buffer = None, path: str = None
    ) -> list[prisma.models.IOrganization]:
        """
        Get organizations from the given data source.

        Args:
            data_source (str): The name of the data source.
            buffer (Buffer, optional): The buffer object.
            path (str, optional): The path to the file.

        Returns:
            list[prisma.models.IOrganization]: A list of organizations.
        """
        files = FileUtils()
        source = await files.read_to_pd(data_source, buffer, path)
        source.rename(columns=iorganization_map, inplace=True)
        source["erefId"] = "dartId:" + source["erefId"].astype(str)
        source["dateModified"] = pd.to_datetime(source["dateModified"])
        for row in tqdm(source.to_dict(orient="records"), total=len(source)):
            await self.upsert(
                data=row, where={"erefId": row["erefId"]}
            )  ##TODO: What is the best way to terminate the execution here when there is a problem with the data instead of crashing the server?

    # async def fetch_corp_details(self):
    #     """
    #     Asynchronously fetches corporate details from the Dart API.

    #     :return: None
    #     """
    #     config = DartApiRequest()
    #     config.file_name = "company"
    #     corporates = await self.fetch_some(where={"businessRegistNum":None})
    #     for corporate in tqdm(corporates, total=len(corporates)):
    #             config.corp_code = str(corporate.dartId)
    #             async for res in dapi.request():
    #                 print(res)
    #                 res = res.json()
    #                 response_status = res.get("status")
    #                 if response_status == "000":
    #                     await self.upsert(data={"corpRegistNum":res["jurir_no"], "businessRegistNum":res["bizr_no"], "phoneNum":res["phn_no"],"corpNameEng":res["corp_name_eng"] }, where={"dartId":res["corp_code"]})
