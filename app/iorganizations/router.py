import logging
from fastapi import APIRouter, HTTPException, Request, UploadFile
import prisma
from app.foundation.adapter_prisma import PrismaAdapter
from app.foundation.field_type_match import cast_dict_to_types, model_fields_into_type_map
from app.iorganizations.service import IOrganizationService

service = IOrganizationService()
router = APIRouter(
    prefix="/api",
    tags=["iorganizations"],
)
adapter = PrismaAdapter()

logger = logging.getLogger(__name__)


@router.get("/iorganizations-count/")
async def count():
    return await service.fetch_count()

@router.get("/iorganizations/{uid}/")
async def get_by_id(uid: str):
    return await service.fetch_many(where={"uid": uid})

@router.get("/iorganizations-group/")
async def group(count=None, by=None, sum=None, order=None, having=None):
    return await service.group_by(
        count=count, by=by, sum=sum, order=order, having=having
    )

@router.get("/iorganizations/")
async def get_orgs(request: Request):
    query_params = request.query_params._dict
    query_args = adapter.to_query_args(query=query_params)
    return await service.fetch_paged(
        where=query_args, take=query_args.take, skip=query_args.take * query_args.page
    )

@router.get("/iorganizations.paged/")
async def get_paged(request: Request):
    query_params = request.query_params._dict
    query_args = adapter.to_query_args(query=query_params)
    page_size = int(query_params["_pageSize"])
    page_num = int(query_params["_pageNum"])
    include = query_params.get("_include", None)
    _sort = query_params.get("_sort", None)
    sort = adapter.to_sort_object(_sort)

    content = await service.fetch_paged(
        where=query_args,
        take=page_size,
        skip=page_size * page_num,
        include=include,
        order=sort
    )  ##TODO: Group these to a single query
    if content is None:
        content = []
    count = await service.fetch_count(where=query_args)
    response = adapter.to_pageable_response(
        query=query_params, response=content, count=count
    )
    return response

@router.post("/iorganizations/")
async def create(request: Request):
    body = await request.json()
    field_types = model_fields_into_type_map(prisma.models.IOrganization.model_fields)
    body = cast_dict_to_types(body, field_types)
    try:
        return await service.create(data=body)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="Bad request")
       

@router.put("/iorganizations/{uid}/")
async def update(request: Request, uid: str):
    body = await request.json()
    field_types = model_fields_into_type_map(prisma.models.IOrganization.model_fields)
    body = cast_dict_to_types(body, field_types)
    return await service.update(where={"uid": uid}, data=body)

@router.delete("/iorganizations/{uid}/")
async def delete(uid):
    return await service.delete(where={"uid": uid})


@router.post("/iorganizations-upload/")
async def upload(file: UploadFile):
    data_source = file.filename
    return await service.upload_organizations(data_source=data_source, buffer=file.file)

@router.get("/iorganization/find-related-sites/")
async def find_related_sites(request: Request):
    companyName = request.query_params.get("companyName")
    logger.debug(companyName)
    if not companyName:
        raise HTTPException(status_code=400, detail="Bad request")
    companyName = companyName.strip()
    return await service.find_related_sites(company_name=companyName)
