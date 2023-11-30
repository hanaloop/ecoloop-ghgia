import datetime
from typing_extensions import Buffer
import glob
import hashlib
import os
import numpy as np
from tqdm import tqdm
from utils.timer import Timer
from utils.file import read_to_pd
import prisma
from pyparsing import Literal
from utils.file_type import return_list
from database import get_connection
from prisma import Json
from config.column_mapping import code_dict
from config.env_config import DATABASE_URL
from config.column_mapping import factory_map
import pandas as pd
from fuzzywuzzy import fuzz
from utils.exception import CustomException
from utils.timer import Timer
##Using service directly causes circular import error


class FactoryOnSiteService:
    def __init__(self):
        self.prisma = get_connection()


    async def upsert(self, data: prisma.models.IOrgSite, where: prisma.types.IOrgSiteWhereInput):
        try:
            existing_record = await self.prisma.iorgsite.find_first(where = where)

            if existing_record:
                await self.prisma.iorgsite.update(
                    where={"uid": existing_record.uid}, data = data
                )
            else:
                await self.prisma.iorgsite.create(data = data)

        except Exception as e:
            raise CustomException(data, e)
    
    @return_list
    async def create(self, data: prisma.types.IOrgSiteCreateInput):
        try:
            return await self.prisma.iorgsite.create(data = data)
        except Exception as e:
            raise CustomException(data, e)
    @return_list
    async def update(self, data: prisma.models.IOrgSite, where: prisma.types.IOrgSiteWhereInput) -> None:
        try:
            await self.prisma.iorgsite.update(where = where, data = data)
        except Exception as e:
            raise CustomException(data, e)

    async def delete(self, where: prisma.types.IOrgSiteWhereInput) -> None:
        try:
            await self.prisma.iorgsite.delete(where = where)
        except Exception as e:
            raise CustomException(where, e)
        
    async def fetch_some(self, where: prisma.types.IOrgSiteWhereInput) -> list[prisma.models.IOrgSite]:
        try:
            return await self.prisma.iorgsite.find_first(where = where)
        except Exception as e:
            raise CustomException(where, e)
        
    async def fetch_all(self):
        try:
            return await self.prisma.iorgsite.find_many()
        except Exception as e:
            raise CustomException(e)
    

    async def create(self, data: prisma.types.IOrgSiteCreateInput) -> None:
        try:
            await self.prisma.iorgsite.create(data = data)
        except Exception as e:
            raise CustomException(data, e)
    
    @return_list
    async def create_many(self, data: prisma.types.IOrgSiteCreateInput) -> None:
        try:
            await self.prisma.iorgsite.create_many(data = data)
        except Exception as e:
            raise CustomException(data, e)

    async def group_by(self, count=None, by = None, sum = None, order = None, having = None) -> list[prisma.models.IOrgSite]:
        try:
            return await self.prisma.iorgsite.group_by(count = count, by = by, sum = sum, order = order, having = having)
        except Exception as e:
            raise CustomException({
                "count": count,
                "by": by,
                "sum": sum,
                "order": order,
                "having": having
            }, e)
        
    async def _fetch_page(self, cursor: str, page_size=10) -> tuple[list[prisma.models.IOrgSite], str]:
        results = await self.prisma.iorgsite.find_many(
            take=page_size,
            cursor={'id': cursor} if cursor else None,
            order={'id': 'asc'}  
        )

        next_cursor = results[-1].id if results else None
        return results, next_cursor
    
    async def fetch_paged(self, take = 10, skip = 0, order = None) -> list[prisma.models.IOrgSite]:
        results = await self.prisma.iorgsite.find_many(
            take=take,
            skip=skip,
            order=order  
        )

        return results

    async def fetch_all_paginated(self):
        pass

    async def fetch_count(self) -> int:
        try:
            return await self.prisma.iorgsite.count()
        except Exception as e:
            raise CustomException(e)

    #Business logic
    def hash_row(self, row: pd.Series) -> str:
        """
        Hashes the row to create a unique key

        Args:
            row (_type_): _description_

        Returns:
            str: _description_
        """
        combined = str(row["businessRegistrationNum"]) + str(row["companyName"]) + str(row["landAddress"])
        # print (hashlib.sha256(combined.encode()).hexdigest())
        return hashlib.sha256(combined.encode()).hexdigest()

    def format_df(self, df:pd.DataFrame) -> pd.DataFrame:
        newDf = df.rename(columns=factory_map)
        for col in ["approvalDate", "registrationDate", "registrationDateInitial", "approvalDateInitial"]:
            newDf[col] = newDf[col].replace("-", None, inplace=True)
            newDf[col] = pd.to_datetime(newDf[col]).replace({np.nan: None}, inplace=True)
        newDf["sectorIdMain"] = newDf["sectorIdMain"].astype(str)
        newDf["factoryManagementNumber"] = newDf["factoryManagementNumber"].astype(str)
        return newDf
    
    async def upload_IorgSites(self, data_source: str, buffer: Buffer = None, path: str = None) -> None:
        source = await read_to_pd(buffer = buffer, path = path)
        source["dataSource"] = data_source
        source = self.format_df(source)
        source["keyHash"] = source.apply(lambda row: self.hash_row(row), axis = 1)
        for index, row in tqdm(source.iterrows(), total=len(source)):
            await self.upsert(data = row.to_dict(), where={"keyHash": row["keyHash"]})

