from typing_extensions import Buffer
import pandas as pd
import prisma
from tqdm import tqdm
from app.config.column_mapping import code_dict
from app.database import get_connection
from app.emission_data.adapters.gir4_import_adapter import GirCategoryAdapter
from app.utils.file import FileUtils

class IEmissionDataService():
    def __init__(self) -> None:
        self.prisma = get_connection()

  
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
            await self.prisma.iemissiondata.update(
                where={"uid": existing_record.uid}, data=data
            )
        else:
            await self.prisma.iemissiondata.create(data=data)

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
        await self.prisma.iemissiondata.upsert(
            data={"create": data, "update": data}, where=where
        )

    async def create(self, data: prisma.types.IEmissionDataCreateInput) -> prisma.models.IEmissionData:
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
        where: prisma.types.IEmissionDataWhereUniqueInput,
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

    async def fetch_some(
        self, where: prisma.types.IEmissionDataWhereInput
    ) -> list[prisma.models.IEmissionData]:
        """
        Fetches some data based on the given where clause.

        Args:
            where: An input object type that represents the conditions used to filter the data.

        Returns:
            A list of IEmissionData objects that match the given conditions.
        """
        return await self.prisma.iemissiondata.find_many(where=where)

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
        self, count=None, by=None, sum=None, order=None, having=None, where: prisma.types.IEmissionDataWhereInput = None
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
        self, take=10, skip=0, order=None
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
            take=take, skip=skip, order=order
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


    async def upload_data(self, data_source: str, buffer: Buffer = None, path: str = None):
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
        find_where = {"categoryName": {"in": list(code_dict.values())}}
        res = await self.fetch_some(where=find_where)
        df = pd.DataFrame([vars(d) for d in res])
        inverse_map = {v: k for k, v in code_dict.items()}
        df["category"] = df["categoryName"].map(inverse_map)
        return df

