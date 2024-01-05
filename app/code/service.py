import os
from typing_extensions import Buffer
import prisma
from app.database import get_connection
from app.utils.file import FileUtils
from tqdm import tqdm
from app.foundation.field_type_match import cast_dict_to_types, model_fields_into_type_map

class CodeService:
    """
    A service class for interacting with the 'Code' table in the database.
    """
    def __init__(self):
        self.prisma = get_connection()

      
    async def delete_all(self):
        """
        Deletes all records in the 'Code' table.
        """
        await self.prisma.code.delete_many()

    async def update_or_create(
        self,
        data: prisma.models.Code,
        where: prisma.types.CodeWhereInput,
    ):
        """
        Update or create a record in the database based on the given data and where condition.

        Args:
            data (prisma.models.Code): The data to update or create the record with.
            where (prisma.types.CodeWhereInput): The condition to search for an existing record.

        Returns:
            None
        """
        existing_record = await self.prisma.code.find_first(where=where)

        if existing_record:
            await self.prisma.code.update(
                where={"uid": existing_record.uid}, data=data
            )
        else:
            await self.prisma.code.create(data=data)

    async def upsert(
        self,
        data: prisma.types.CodeCreateInput,
        where: prisma.types.CodeWhereUniqueInput,
        include=None,
    ):
        """
        Upserts an organization in the database.

        Args:
            data (prisma.types.CodeCreateInput): The data to be upserted.
            where (prisma.types.CodeWhereUniqueInput): The unique identifier of the organization.
            include (Optional): The related models and fields to include in the upsert operation.

        Returns:
            None
        """
        await self.prisma.code.upsert(
            data={"create": data, "update": data}, where=where
        )

    async def create(self, data: prisma.types.CodeCreateInput) -> prisma.models.Code:
        """
        Creates a new organization with the given data.

        Parameters:
            - data: An instance of prisma.types.CodeCreateInput representing the data for the new organization.

        Returns:
            None
        """
        return await self.prisma.code.create(data=data)

    async def update(
        self,
        data: prisma.models.Code,
        where: prisma.types.CodeWhereUniqueInput,
    ) -> prisma.models.Code:
        """
        Update the given organization with the provided data.

        Args:
            data (prisma.models.Code): The data to update the organization with.
            where (prisma.types.CodeWhereUniqueInput): The unique identifier for the organization.

        Returns:
            None
        """
        return await self.prisma.code.update(where=where, data=data)

    async def delete(self, where: prisma.types.CodeWhereInput) -> None:
        """
        Deletes a record from the OrgSite table based on the given criteria.

        Parameters:
            where (prisma.types.CodeWhereInput): The criteria used to determine which records to delete.

        Returns:
            None
        """
        await self.prisma.code.delete(where=where)

    async def fetch_some(
        self, where: prisma.types.CodeWhereInput, include: prisma.types.CodeInclude | None = None
    ) -> list[prisma.models.Code]:
        """
        Fetches some data based on the given where clause.

        Args:
            where: An input object type that represents the conditions used to filter the data.

        Returns:
            A list of Code objects that match the given conditions.
        """
        return await self.prisma.code.find_many(where=where, include=include)

    async def fetch_one(
        self, where: prisma.types.CodeWhereInput
    )-> prisma.models.Code | None:
        """
        Fetches a single record based on the given where clause.

        Args:
            where: An input object type that represents the conditions used to filter the data.

        Returns:
            An Code object that matches the given conditions or None if no record is found.
        """
        return await self.prisma.code.find_first(where=where)


    async def create_many(self, data: prisma.types.CodeCreateInput) -> None:
        """
        Create multiple organizations.

        Args:
            data (prisma.types.CodeCreateInput): The data to create multiple organizations.

        Returns:
            None: This function does not return anything.
        """
        await self.prisma.code.create_many(data=data)

    async def group_by(
        self, count=None, by=None, sum=None, order=None, having=None, where: prisma.types.CodeWhereInput = None
    ) -> list[prisma.models.Code]:
        """
        A decorator that catches any errors that occur during the execution of the `group_by` function.

        Args:
            count (Optional): The count parameter of the `group_by` function.
            by (Optional): The by parameter of the `group_by` function.
            sum (Optional): The sum parameter of the `group_by` function.
            order (Optional): The order parameter of the `group_by` function.
            having (Optional): The having parameter of the `group_by` function.

        Returns:
            list[prisma.models.Code]: A list of `prisma.models.Code` objects.
        """
        return await self.prisma.code.group_by(
            count=count, by=by, sum=sum, order=order, having=having, where=where
        )

    async def _fetch_page(
        self, cursor: str, page_size=10
    ) -> tuple[list[prisma.models.Code], str]:
        """
        Fetches a page of organizations from the database.

        Args:
            cursor (str): The cursor used for pagination.
            page_size (int, optional): The number of results per page. Defaults to 10.

        Returns:
            Tuple[List[prisma.models.Code], str]: A tuple containing a list of organizations
                and the next cursor for pagination.
        """
        results = await self.prisma.code.find_many(
            take=page_size,
            cursor={"id": cursor} if cursor else None,
            order={"id": "asc"},
        )
        next_cursor = results[-1].id if results else None
        return results, next_cursor

    async def fetch_paged(
        self, take=10, skip=0, order=None, where: prisma.types.CodeWhereInput = None
    ) -> list[prisma.models.Code]:
        """
        Fetches a paged list of organizations.

        Args:
            take (int): The number of items to take per page.
            skip (int): The number of items to skip.
            order (Optional[str]): The field to order the results by.

        Returns:
            list[prisma.models.Code]: The list of organizations.
        """
        results = await self.prisma.code.find_many(
            take=take, skip=skip, order=order, where=where
        )
        return results

    async def fetch_all_paginated(self):
        pass

    async def fetch_count(self) -> int:
        """
        Fetches the count of the Code table.

        Returns:
            int: The count of the Code table.
        """
        return await self.prisma.code.count()

    # Business logic


    async def upload_data(self, data_source: str=None, buffer: Buffer = None, path: str = None):
        if not data_source and buffer:
            data_source = "web"
        elif path and not buffer:
            data_source = os.path.basename(path)
        else:
            data_source = None
        if not path and not buffer:
            raise Exception("No data source provided")
        files = FileUtils()
        model_annotation = model_fields_into_type_map(
            prisma.models.Code.model_fields
        )
        df = await files.read_to_pd(data_source, buffer, path)

        df['parentUid'] = df['parentUid'].apply(lambda x: None if x=='' else x)
        data_to_upload = df.to_dict(orient="records")
        for i, row in enumerate(data_to_upload):
            data_to_upload[i] = cast_dict_to_types(row, model_annotation)
        await self.create_many(data=data_to_upload)
