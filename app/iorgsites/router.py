import logging
from fastapi import APIRouter, HTTPException, Request, UploadFile
import pandas as pd
import prisma
from app.iorgsites.service import IOrgSiteService
from app.foundation.adapter_prisma import PrismaAdapter
from app.foundation.field_type_match import cast_dict_to_types, model_fields_into_type_map

service = IOrgSiteService()
adapter = PrismaAdapter()
router = APIRouter(
    prefix="/api",
    tags=["iorgsites"],
)
logger = logging.getLogger("api.iorgsites")


@router.get("/iorgsites/count")
async def count():
    return await service.fetch_count()



@router.get("/iorgsites/group")
async def group(count=None, by=None, sum=None, order=None, having=None):
    return await service.group_by(
        count=count, by=by, sum=sum, order=order, having=having
    )

@router.post("/iorgsites/upload")
async def upload(file: UploadFile):
    data_source = file.filename
    return await service.upload_iorgsites(data_source=data_source, buffer=file.file)


@router.put("/iorgsites/addresses/update")
async def update_addresses():
    return await service.populate_addresses()


@router.put("/iorgsites/{uid}/address")
async def update_single_address(uid: str):
    return await service.populate_single_address(uid=uid)

@router.get("/iorgsites/")
async def search(request: Request):
    query_params = request.query_params._dict
    query_args = adapter.to_query_args(query=query_params)
    return await service.fetch_paged(
        where=query_args, take=query_args.take, skip=query_args.take * query_args.page
    )

@router.get("/iorgsites/{uid}")
async def search(uid: str):
    return await service.fetch_some(where={"uid": uid})

@router.get("/iorgsites.paged/")
async def search(request: Request):
    query_params = request.query_params._dict
    query_args = adapter.to_query_args(query=query_params)
    page_size = int(query_params["_pageSize"])
    page_num = int(query_params["_pageNum"])
    include = query_params['include'] if 'include' in query_params else None
    content = await service.fetch_paged(
        where=query_args,
        take=page_size,
        skip=page_size * page_num,
        include=include
    )  ##TODO: Group these to a single query
    count = await service.fetch_count()
    response = adapter.to_pageable_response(
        query=query_params, response=content, count=count
    )
    return response


@router.post("/iorgsites/")
async def search(request: Request):
    body = await request.json()
    field_types = model_fields_into_type_map(prisma.models.IOrgSite.model_fields)
    body = cast_dict_to_types(body, field_types)
    body_as_pd = pd.DataFrame(body, index=[0])
    body_as_series = body_as_pd.iloc[0]
    body_as_series["keyHash"] = service.hash_row(row=body_as_series)
    try:
        return await service.create(data=body_as_series.to_dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail="Site already exists")
        
       


@router.put("/iorgsites/{uid}")
async def search(request: Request, uid: str):
    body = await request.json()
    field_types = model_fields_into_type_map(prisma.models.IOrgSite.model_fields)
    body = cast_dict_to_types(body, field_types)
    return await service.update(where={"uid": uid}, data=body)

@router.delete("/iorgsites/{uid}")
async def delete(uid):
    return await service.delete(where={"uid": uid})
