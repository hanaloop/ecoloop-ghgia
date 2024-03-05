from typing import Optional
from fastapi import Request
from pydantic import BaseModel

from app.utils.string import string_to_dict


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
            if key and key.startswith("_") or not prop or prop == "":
                continue
            if len(key.split(":")) == 2:
                field, operator = key.split(":")
                if prop and len(prop.split(",")) > 1 or operator == "in":
                    operands[field] = {operator: prop.split(",")}
                elif len(key.split(":")) > 1:
                    operands[field] = {key.split(":")[1]: prop}
            elif len(key.split(":")) > 2:
                new_key = ":".join([key, prop])
                joint_dict = string_to_dict(new_key, ":")
                operands.update(joint_dict)
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

    def to_include_exclude_args(self, arg: str):
        """
        Generate a dictionary with each element in the input list as a key and set its value to True.

        Args:
            arg (list): The input list.

        Returns:
            dict: A dictionary with each element in the input list as a key and True as its value.
        """
        arg_list = arg.split(",")
        if not arg_list:
            return
        if not isinstance(arg_list, list):
            try:
                arg_list = [arg_list]
            except:
                raise ValueError(f"Cannot convert {arg_list} to list")
        return {value: True for value in arg_list}

    def to_sort_object(self, sort: str):
        if not sort:
            return
        _sort_list = sort.split(",")
        return [{value.split(':')[0]: value.split(':')[1] } for value in _sort_list] 
