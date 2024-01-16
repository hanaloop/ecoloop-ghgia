from typing import Optional
from fastapi import Request
from pydantic import BaseModel


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
    def to_query_args(self, query: dict):
        operands = {}

        if not query:
            return
        for key, prop in query.items():
            if key and key.startswith("_"):
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

        return operands

    def to_pageable_response(
        self, query: Request, response, count: int
    ) -> PageableResponse:
        if not response and isinstance(query["_pageNum"], int) and query["_pageSize"]:
            return
        response = PageableResponse(
            number=int(query["_pageNum"]),
            numberOfElements=len(response),
            size=int(query["_pageSize"]),
            first=int(query["_pageNum"]) == 0,
            last=int(query["_pageNum"]) == (count // int(query["_pageSize"]) ) if count > int(query["_pageSize"]) else True,
            totalPages=count // int(query["_pageSize"]) + 1
            if count % int(query["_pageSize"]) > 0
            else count // int(query["_pageSize"]),
            totalElements=count,
            content=response,
        )
        return response

    def to_include_exclude_args(self, arg: list):
        """
        Generate a dictionary with each element in the input list as a key and set its value to True.

        Args:
            arg (list): The input list.

        Returns:
            dict: A dictionary with each element in the input list as a key and True as its value.
        """
        if not arg:
            return
        if not isinstance(arg, list):
            try:
                arg = [arg]
            except:
                raise ValueError(f"Cannot convert {arg} to list")
        return {key: True for key in arg}
