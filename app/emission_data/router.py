import logging
from fastapi import APIRouter, HTTPException, Request, UploadFile
import prisma
from app.emission_data.service import IEmissionDataService
from app.foundation.adapter_prisma import  PrismaAdapter
from app.foundation.field_type_match import cast_dict_to_types, model_fields_into_type_map


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
    return await service.fetch_paged(
        where=query_args, take=query_args.take, skip=query_args.take * query_args.page
    )

@router.get("/iemissiondata/{uid}")
async def search(uid: str):
    return await service.fetch_some(where={"uid": uid})


@router.get("/iemissiondata.paged/")
async def search(request: Request):
    query_params = request.query_params._dict
    query_args = adapter.to_query_args(query=query_params)
    page_size = int(query_params["_pageSize"])
    page_num = int(query_params["_pageNum"])
    content = await service.fetch_paged(
        where=query_args,
        take=page_size,
        skip=page_size * page_num,
    )  ##TODO: Group these to a single query
    count = len(content)
    response = adapter.to_pageable_response(
        query=query_params, response=content, count=count
    )
    return response


@router.post("/iemissiondata/")
async def search(request: Request):
    body = await request.json()
    field_types = model_fields_into_type_map(prisma.models.IEmissionData.model_fields)
    body = cast_dict_to_types(body, field_types)
    try:
        return await service.create(data=body)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="Site already exists")
       

@router.put("/iemissiondata/{uid}")
async def search(request: Request, uid: str):
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

