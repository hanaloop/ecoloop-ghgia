import logging
from fastapi import APIRouter, HTTPException, Request, UploadFile
import prisma
from app.emission_data.service import IEmissionDataService
from app.foundation.adapter_prisma import PrismaAdapter
from app.foundation.field_type_match import (
    cast_dict_to_types,
    model_fields_into_type_map,
)


service = IEmissionDataService()
router = APIRouter(
    prefix="/api",
    tags=["iemissiondata"],
)
adapter = PrismaAdapter()
logger = logging.getLogger("api.iorgsites")


@router.get("/iemissiondata/iemissiondata/count")
async def count():
    return await service.fetch_count()


@router.get("/iemissiondata/group")
async def group(count=None, by=None, sum=None, order=None, having=None):
    return await service.group_by(
        count=count, by=by, sum=sum, order=order, having=having
    )


@router.get("/iemissiondata/")
async def search(request: Request):
    query_params = request.query_params._dict
    query_args = adapter.to_query_args(query=query_params)
    include = (
        adapter.to_include_exclude_args(query_params["_include"])
        if "_include" in query_params
        else None
    )
    response = await service.fetch_many(where=query_args, include=include) ##TODO: Put default take num so that results are limited
    return response


@router.get("/iemissiondata/{uid}")
async def get_by_id(uid: str):
    return await service.fetch_many(where={"uid": uid})

@router.get("/iemissiondata/compare/")
async def fetch_grouped_by_region(request: Request):
    query_params = request.query_params._dict
    year_start = query_params["_year_from"] if "_year_from" in query_params else None
    year_end = query_params["_year_to"] if "_year_to" in query_params else None
    if year_start is None or year_end is None:
        raise HTTPException(status_code=400, detail="year_start and year_end are required")
    response = await service.fetch_grouped_by_region( year_start=year_start, year_end=year_end)
    return response

@router.get("/iemissiondata.paged/")
async def get_paged(request: Request):
    query_params = request.query_params._dict
    query_args = adapter.to_query_args(query=query_params)
    page_size = int(query_params["_pageSize"])
    page_num = int(query_params["_pageNum"])
    include = (
        adapter.to_include_exclude_args(query_params["_include"])
        if "_include" in query_params
        else None
    )
    content = await service.fetch_paged(
        where=query_args,
        take=page_size,
        skip=page_size * page_num,
        include=include,
    )  ##TODO: Group these to a single query
    if content is None:
        content = []
    count = await service.fetch_count()
    response = adapter.to_pageable_response(
        query=query_params, response=content, count=count
    )
    return response


@router.post("/iemissiondata/")
async def create(request: Request):
    body = await request.json()
    field_types = model_fields_into_type_map(prisma.models.IEmissionData.model_fields)
    body = cast_dict_to_types(body, field_types)
    try:
        return await service.create(data=body)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="Site already exists")


@router.put("/iemissiondata/{uid}")
async def update(request: Request, uid: str):
    body = await request.json()
    field_types = model_fields_into_type_map(prisma.models.IEmissionData.model_fields)
    body = cast_dict_to_types(body, field_types)
    return await service.update(where={"uid": uid}, data=body)


@router.delete("/iemissiondata/{uid}")
async def delete(uid):
    return await service.delete(where={"uid": uid})


@router.post("/iemissiondata/upload")
async def upload(file: UploadFile):
    data_source = file.filename
    return await service.upload_data(data_source=data_source, buffer=file.file)


@router.get("/iemissiondata-dateboundaries")
async def date_boundaries(request: Request):
    return await service.get_date_boundaries()
