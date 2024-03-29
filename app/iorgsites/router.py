import logging
from fastapi import APIRouter, HTTPException, Request, UploadFile
import pandas as pd
import prisma
from app.iorgsites.service import IOrgSiteService
from app.foundation.adapter_prisma import PrismaAdapter
from app.foundation.field_type_match import cast_dict_to_types, model_fields_into_type_map

service = IOrgSiteService()
adapter = PrismaAdapter()
api_logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/api",
    tags=["iorgsites"],
)


@router.get("/iorgsites-count")
async def count():
    return await service.fetch_count()



@router.get("/iorgsites-group")
async def group(count=None, by=None, sum=None, order=None, having=None):
    return await service.group_by(
        count=count, by=by, sum=sum, order=order, having=having
    )

@router.post("/iorgsites-upload")
async def upload(file: UploadFile):
    return await service.upload_iorgsites(buffer=file.file)


@router.put("/iorgsites-address-all/")
async def update_addresses():
    return await service.populate_addresses()


@router.put("/iorgsites-address/{uid}/")
async def update_single_address(uid: str):
    return await service.populate_single_address(uid=uid)

@router.get("/iorgsite/")
async def get(request: Request):
    query_params = request.query_params._dict
    query_args = adapter.to_query_args(query=query_params)
    include = query_params.get("_include", None)
    return await service.fetch_paged(
        where=query_args, take=query_args.take, skip=query_args.take * query_args.page, include=include
    )

@router.get("/iorgsites/{uid}/")
async def get_by_id(uid: str):
    return await service.fetch_many(where={"uid": uid})

@router.get("/iorgsites.paged/")
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
    _sort = query_params.get("_sort", None)
    sort = adapter.to_sort_object(_sort)
    content = await service.fetch_paged(
        where=query_args,
        take=page_size,
        skip=page_size * page_num,
        include=include,
        order=sort
    )  ##TODO: Group these to a single query
    count = await service.fetch_count(where=query_args)
    response = adapter.to_pageable_response(
        query=query_params, response=content, count=count
    )
    return response


@router.post("/iorgsites/")
async def create(request: Request):
    body = await request.json()
    field_types = model_fields_into_type_map(prisma.models.IOrgSite.model_fields)
    body = cast_dict_to_types(body, field_types)
    body_as_pd = pd.DataFrame(body, index=[0])
    body_as_series = body_as_pd.iloc[0].copy()
    body_as_series["keyHash"] = service.hash_row(row=body_as_series)
    try:
        return await service.add_site(site=body_as_series.to_dict(),)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Site already exists")

@router.put("/iorgsites/{uid}/")
async def update(request: Request, uid: str):
    body = await request.json()
    field_types = model_fields_into_type_map(prisma.models.IOrgSite.model_fields)
    body_update = cast_dict_to_types(body, field_types)
    return await service.update(where={"uid": uid}, data=body_update)

@router.delete("/iorgsites/{uid}/")
async def delete(uid):
    return await service.delete_site(uid=uid)

@router.put("/iorgsite/{orgUid}/")
async def update_site_organization(request: Request, orgUid: str = None):
    if orgUid == "undefined" or orgUid == "null":
        orgUid = None
    body = await request.json()
    field_types = model_fields_into_type_map(prisma.models.IOrgSite.model_fields)
    body = cast_dict_to_types(body, field_types)
    return await service.update_site(orgUid=orgUid, data=body)

