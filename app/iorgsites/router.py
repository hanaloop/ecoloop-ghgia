import logging
from typing import Annotated, Any
from fastapi import APIRouter, Body, Form, UploadFile, Depends, Request
from prisma.partials import PostIorgSiteObject
from app.iorgsites.service import IOrgSiteService
from app.foundation.adapter_prisma import PageableResponse, PrismaAdapter, QueryArgs, TestObj

service = IOrgSiteService()
adapter = PrismaAdapter()
router = APIRouter(
    prefix="/api/iorgsites",
    tags=["iorgsites"],
)
logger = logging.getLogger("api.iorgsites")

@router.get("/count")
async def count():
    return await service.fetch_count()

@router.get("/paged")
async def paged(skip: int = 0, limit: int = 10):
    return await service.fetch_paged(skip=skip, take=limit)

@router.get("/group")
async def group(count=None, by = None, sum = None, order = None, having = None):
    return await service.group_by(count = count, by = by, sum = sum, order = order, having = having)

@router.get("/{uid}")
async def get_by_id(uid):
    return await service.fetch_one(where={"uid": uid})

@router.delete("/") ##TODO: Need auth TODO:Unify functions
async def delete(where = None):
    return await service.delete(where=where)

@router.delete("/{uid}")
async def search():
    return await service.delete(where={"uid": uid})

@router.put("/")
async def update(where = None, data = None):
    return await service.update(where=where, data=data)

@router.post("/")
async def create(data):
    return await service.create(data=data)

@router.post("/upload")
async def upload(file: UploadFile):
    data_source = file.filename
    return await service.upload_iorgsites(data_source=data_source, buffer=file.file)

@router.put("/addresses/update")
async def update_addresses():
    return await service.populate_addresses()

@router.put("/{uid}/address")
async def update_single_address(uid: str):
    return await service.populate_single_address(uid=uid)

@router.get("/search/")
async def search(query: QueryArgs = Depends()):
    logger.debug("query: %s", query)
    query_args = adapter.to_query_args(query=query.query)
    logger.debug("query_args: %s", query_args)
    return await service.fetch_paged(where=query_args, take=query.pageSize, skip=query.pageSize*query.currentPage)

@router.get("/search.paged/")
async def search(query: QueryArgs = Depends()):
    logger.debug("query: %s", query)
    query_args = adapter.to_query_args(query=query.query)
    logger.debug("query_args: %s", query_args)
    content =  await service.fetch_paged(where=query_args, take=query.pageSize, skip=query.pageSize*query.currentPage, order=query.sort) ##TODO: Group these to a single query
    count = await service.fetch_count()
    response = adapter.to_pageable_response(query=query, response=content, count=count)
    return response

@router.post("/add/")
async def search(body: Request):
    body = await body.json()
    logger.debug("body: %s", body)
    return await service.add_site(site=body)

@router.put("/edit/")
async def search(query: QueryArgs = Depends(), request_data = None):
    logger.debug("query: %s", query)
    query_args = adapter.to_query_args(query=query.query)
    logger.debug("query_args: %s", query_args)
    return await service.upsert(where=query_args, data=request_data)
