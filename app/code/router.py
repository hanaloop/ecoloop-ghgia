import logging
from fastapi import APIRouter, HTTPException, Request, UploadFile
import prisma
from app.code.service import CodeService
from app.foundation.adapter_prisma import PrismaAdapter
from app.foundation.field_type_match import cast_dict_to_types, model_fields_into_type_map

adapter = PrismaAdapter()
service = CodeService()
logger = logging.getLogger("api.code")
router = APIRouter(
    prefix="/api",
    tags=["code"],
)

@router.get("/code-count")
async def count():
    return await service.fetch_count()

@router.get("/code.paged/")
async def get_paged(request: Request):
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

@router.get("/code/")
async def search(request: Request):
    query_params = request.query_params._dict
    query_args = adapter.to_query_args(query=query_params)
    include = query_params.get("_include", None)
    return await service.fetch_some(
        where=query_args, include=include
    )


@router.get("/code-group")
async def group(count=None, by = None, sum = None, order = None, having = None):
    return await service.group_by(count = count, by = by, sum = sum, order = order, having = having)

@router.get("/code/{uid}")
async def get_by_id(uid):
    return await service.fetch_some(where={"uid": uid})

@router.delete("/code/{uid}")
async def delete(where = None):
    return await service.delete(where=where)

@router.put("/code/{uid}")
async def update(where = None, data = None):
    return await service.update(where=where, data=data)

@router.post("/code/")
async def create(request: Request):
    body = await request.json()
    field_types = model_fields_into_type_map(prisma.models.Code.model_fields)
    body = cast_dict_to_types(body, field_types)
    try:
        return await service.create(data=body)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail="Site already exists") from e

@router.post("/upload")
async def upload(file: UploadFile):
    data_source = file.filename
    return await service.upload_data(data_source=data_source, buffer=file.file)
