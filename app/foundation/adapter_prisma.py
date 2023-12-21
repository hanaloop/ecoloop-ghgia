from enum import Enum
import json
from typing import Optional
from typing_extensions import Any
from fastapi import Body, Query
import prisma
from pydantic import BaseModel, Field
from prisma.models import IOrgSite

class QueryArgs:
    def __init__(
        self,
        query=Query(
            default={},
            title="Query",
            required=False,
        ),
        _pageSize: Optional[int] = Query(default=20, title="Take", required=False),
        _pageNum: Optional[int] = Query(default=0, title="Page", required=False),
        sort = Query(default=None, title="Sort", required=False),
    ) -> None:
        self.query = query
        self.pageSize = _pageSize
        self.currentPage = _pageNum
        self.sort = sort

class TestObj(BaseModel):
    def __init__(self, id: int = Body(), name: str = Body()) -> None:
        self.id = id
        self.name = name

class PageableResponse(BaseModel):
    number: Optional[int]
    size: Optional[int]
    numberOfElements: Optional[int]
    totalElements: Optional[int]
    totalPages: Optional[int]
    first: bool = True
    last: bool = False
    content: list = []


class PrismaAdapter:
    def to_query_args(self, query: QueryArgs, schema: prisma.models = None):
        print(query)
        operands = {}
        query = {query}
        query = json.loads(query)
        if not query:
            return
        for key, prop in query.items():
            if prop and prop.startswith("_"):
                continue
            if len(key.split(":")) > 1:
                field, operator = key.split(":")
                if prop and len(prop.split(",")) > 1:
                    operands[field] = {operator: prop.split(",")}
                elif len(key.split(":")) > 1:
                    operands[field] = {key.split(":")[1]: prop}
            # elif:
            else:
                operands[key] = prop

        print(operands)
        return operands

    def to_pageable_response(
        self, query: QueryArgs, response, count: int
    ) -> PageableResponse:
        if not response and isinstance(query.page, int) and query.take:
            return
        response = PageableResponse(
            number=query.currentPage,
            numberOfElements=len(response),
            size=query.pageSize,
            first= query.currentPage == 0,
            last=query.currentPage == count // query.pageSize,
            totalPages=count // query.pageSize
            if count % query.pageSize > 0
            else count // query.pageSize,
            totalElements=count,
            content=response,
        )
        return response
