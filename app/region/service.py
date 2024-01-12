
import prisma
from app.database import get_connection

class RegionService:
    def __init__(self):
        self.prisma = get_connection()
    
    async def delete_all(self):
        """
        Deletes all records in the 'Region' table.
        """
        return await self.prisma.region.delete_many()

    async def update_or_create(
        self,
        data: prisma.models.Region,
        where: prisma.types.RegionWhereInput,
    ):
        """
        Update or create a record in the database based on the given data and where condition.

        Args:
            data (prisma.models.Region): The data to update or create the record with.
            where (prisma.types.RegionWhereInput): The condition to search for an existing record.

        Returns:
            None
        """
        existing_record = await self.prisma.region.find_first(where=where)

        if existing_record:
            return await self.prisma.region.update(
                where={"uid": existing_record.uid}, data=data
            )
        else:
            return await self.prisma.region.create(data=data)

    async def fetch_one(self, where: prisma.types.RegionWhereUniqueInput, include=None)-> prisma.models.Region:
        """
        Fetches one record from the 'Region' table based on the given where clause.

        Args:
            where (prisma.types.RegionWhereUniqueInput): The unique identifier of the record to fetch.

        Returns:
            A Region object representing the fetched record.
        """
        return await self.prisma.region.find_first(where=where, include=include)

    async def upsert(
        self,
        data: prisma.types.RegionCreateInput,
        where: prisma.types.RegionWhereUniqueInput,
        include=None,
    ):
        """
        Upserts an organization in the database.

        Args:
            data (prisma.types.RegionCreateInput): The data to be upserted.
            where (prisma.types.RegionWhereUniqueInput): The unique identifier of the organization.
            include (Optional): The related models and fields to include in the upsert operation.

        Returns:
            None
        """
        return await self.prisma.region.upsert(
            data={"create": data, "update": data}, where=where
        )

    async def create(self, data: prisma.types.RegionCreateInput) -> prisma.models.Region:
        """
        Creates a new organization with the given data.

        Parameters:
            - data: An instance of prisma.types.RegionCreateInput representing the data for the new organization.

        Returns:
            None
        """
        return await self.prisma.region.create(data=data)

    async def update(
        self,
        data: prisma.models.Region,
        where: prisma.types.RegionWhereUniqueInput,
    ) -> prisma.models.Region:
        """
        Update the given organization with the provided data.

        Args:
            data (prisma.models.Region): The data to update the organization with.
            where (prisma.types.RegionWhereUniqueInput): The unique identifier for the organization.

        Returns:
            None
        """
        return await self.prisma.region.update(where=where, data=data)

    async def delete(self, where: prisma.types.RegionWhereInput) -> None:
        """
        Deletes a record from the OrgSite table based on the given criteria.

        Parameters:
            where (prisma.types.RegionWhereInput): The criteria used to determine which records to delete.

        Returns:
            None
        """
        return await self.prisma.region.delete(where=where)

    async def fetch_many(
        self, where: prisma.types.RegionWhereInput
    ) -> list[prisma.models.Region]:
        """
        Fetches some data based on the given where clause.

        Args:
            where: An input object type that represents the conditions used to filter the data.

        Returns:
            A list of Region objects that match the given conditions.
        """
        return await self.prisma.region.find_first(where=where)

    async def fetch_all(self) -> list[prisma.models.Region]:
        """
        Fetches all data from the OrgSite table.

        Returns:
            A list of Region objects representing all records in the OrgSite table.
        """
        return await self.prisma.region.find_many()

    async def create_many(self, data: prisma.types.RegionCreateInput) -> None:
        """
        Create multiple organizations.

        Args:
            data (prisma.types.RegionCreateInput): The data to create multiple organizations.

        Returns:
            None: This function does not return anything.
        """
        return await self.prisma.region.create_many(data=data)

    async def group_by(
        self, count=None, by=None, sum=None, order=None, having=None
    ) -> list[prisma.models.Region]:
        """
        A decorator that catches any errors that occur during the execution of the `group_by` function.

        Args:
            count (Optional): The count parameter of the `group_by` function.
            by (Optional): The by parameter of the `group_by` function.
            sum (Optional): The sum parameter of the `group_by` function.
            order (Optional): The order parameter of the `group_by` function.
            having (Optional): The having parameter of the `group_by` function.

        Returns:
            list[prisma.models.Region]: A list of `prisma.models.Region` objects.
        """
        return await self.prisma.region.group_by(
            count=count, by=by, sum=sum, order=order, having=having
        )

    async def _fetch_page(
        self, cursor: str, page_size=10
    ) -> tuple[list[prisma.models.Region], str]:
        """
        Fetches a page of organizations from the database.

        Args:
            cursor (str): The cursor used for pagination.
            page_size (int, optional): The number of results per page. Defaults to 10.

        Returns:
            Tuple[List[prisma.models.Region], str]: A tuple containing a list of organizations
                and the next cursor for pagination.
        """
        results = await self.prisma.region.find_many(
            take=page_size,
            cursor={"id": cursor} if cursor else None,
            order={"id": "asc"},
        )
        next_cursor = results[-1].id if results else None
        return results, next_cursor

    async def fetch_paged(
        self, take=10, skip=0, order=None
    ) -> list[prisma.models.Region]:
        """
        Fetches a paged list of organizations.

        Args:
            take (int): The number of items to take per page.
            skip (int): The number of items to skip.
            order (Optional[str]): The field to order the results by.

        Returns:
            list[prisma.models.Region]: The list of organizations.
        """
        results = await self.prisma.region.find_many(
            take=take, skip=skip, order=order
        )
        return results

    async def fetch_all_paginated(self):
        pass

    async def fetch_count(self) -> int:
        """
        Fetches the count of the Region table.

        Returns:
            int: The count of the Region table.
        """
        return await self.prisma.region.count()
