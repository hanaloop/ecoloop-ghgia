import datetime
from typing_extensions import Buffer
import glob
import hashlib
import os
import numpy as np
from tqdm import tqdm
from utils.timer import Timer

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


    async def upsert(self, data: prisma.models.IOrgSite, where):
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
    async def create(self, data):
        try:
            return await self.prisma.iorgsite.create(data = data)
        except Exception as e:
            raise CustomException(data, e)
    @return_list
    async def update(self, data: prisma.models.IOrgSite, where):
        try:
            await self.prisma.iorgsite.update(where = where, data = data)
        except Exception as e:
            raise CustomException(data, e)

    async def delete(self, where):
        try:
            await self.prisma.iorgsite.delete(where = where)
        except Exception as e:
            raise CustomException(where, e)
        
    async def get_some(self, where):
        try:
            return await self.prisma.iorgsite.find_first(where = where)
        except Exception as e:
            raise CustomException(where, e)
        
    async def get_all(self):
        try:
            return await self.prisma.iorgsite.find_many()
        except Exception as e:
            raise CustomException(e)\
    

    async def create(self, data):
        try:
            return await self.prisma.iorgsite.create(data = data)
        except Exception as e:
            raise CustomException(data, e)
    
    @return_list
    async def create_many(self, data):
        try:
            return await self.prisma.iorgsite.create_many(data = data)
        except Exception as e:
            raise CustomException(data, e)

    async def group_by(self, count=None, by = None, sum = None, order = None, having = None):
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
        
    async def _fetch_page(self, cursor, page_size=10):
        results = await self.prisma.iorgsite.find_many(
            take=page_size,
            cursor={'id': cursor} if cursor else None,
            order={'id': 'asc'}  
        )

        next_cursor = results[-1].id if results else None
        return results, next_cursor
    async def fetch_all_paginated(self):
        all_results = []
        current_cursor = None

        while True:
            results, current_cursor = await self._fetch_page(prisma, current_cursor)
            all_results.extend(results)

            if not results or current_cursor is None:
                break

        return all_results

    async def fetch_count(self):
        try:
            return await self.prisma.iorgsite.count()
        except Exception as e:
            raise CustomException(e)

    #Business logic
    def hash_row(self, row) -> str:
        """
        Hashes the row to create a unique key

        Args:
            row (_type_): _description_

        Returns:
            str: _description_
        """
        combined = str(row["businessRegistrationNum"]) + str(row["companyName"]) + str(row["landAddress"])
        print (hashlib.sha256(combined.encode()).hexdigest())
        return hashlib.sha256(combined.encode()).hexdigest()

    def format_df(self, df:pd.DataFrame) -> pd.DataFrame:
        newDf = df.rename(columns=factory_map)
        newDf["sectorIdMain"] = newDf["sectorIdMain"].astype(str)
        newDf['registrationDate'] = pd.to_datetime(newDf["registrationDate"]).replace({np.nan: None}, inplace=True)
        newDf['registrationDateInitial'] = pd.to_datetime(newDf["registrationDateInitial"]).replace({np.nan: None}, inplace=True)
        newDf["approvalDateInitial"] = pd.to_datetime(newDf["approvalDateInitial"]).replace({np.nan: None}, inplace=True)
        newDf["approvalDate"] = pd.to_datetime(newDf["approvalDate"], ).replace({np.nan: None}, inplace=True)
        newDf["factoryManagementNumber"] = newDf["factoryManagementNumber"].astype(str)
        return newDf
    
    async def read_to_pd(self, data_source: str, buffer: Buffer = None, path: str = None):
        ##does it read csv? TODO:
        if (not buffer and not path) or (buffer and path):
            raise Exception("Either buffer or path must be provided")
        file = buffer or path
        df = pd.read_excel(file).fillna("")
        df.replace("",None,inplace=True)
        df["dataSource"] = data_source
        df = self.format_df(df)
        df["keyHash"] = df.apply(lambda row: self.hash_row(row), axis = 1)
        for index, row in tqdm(df.iterrows()):
            await self.upsert(data = row.to_dict(), where={"keyHash": row["keyHash"]})

