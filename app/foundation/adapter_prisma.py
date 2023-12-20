from enum import Enum
import json
from typing import Optional
from typing_extensions import Any
from fastapi import Query
import prisma
from pydantic import BaseModel, Field


class QueryArgs:
    def __init__(
        self,
        query=Query(
            default={},
            title="Query",
            required=False,
        ),
        pageSize: Optional[int] = Query(default=10, title="Take", required=False),
        currentPage: Optional[int] = Query(default=1, title="Page", required=False),
    ) -> None:
        self.query = query
        self.take = pageSize
        self.page = currentPage


class PageableResponse(BaseModel):
    number: Optional[int]
    size: Optional[int]
    numberOfElements: Optional[int]
    totalElements: Optional[int]
    totalPages: Optional[int]
    first: bool = True
    last: bool = True
    content: list = []


class PrismaAdapter:
    def to_query_args(self, query: QueryArgs, schema: prisma.models = None):
        print(query)
        operands = {}
        query = json.loads(query) if query and isinstance(query, str) else query
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
            number=query.page + 1,
            numberOfElements=len(response),
            size=query.take,
            first= query.page == 0,
            last=query.page == count // query.take,
            totalPages=count // query.take + 1
            if count % query.take > 0
            else count // query.take,
            totalElements=count,
            content=response,
        )
        return response
