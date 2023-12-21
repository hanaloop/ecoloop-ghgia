from fastapi import APIRouter, Depends, UploadFile
from app.foundation.adapter_prisma import PrismaAdapter, QueryArgs
from app.iorganizations.service import IOrganizationService


service = IOrganizationService()
router = APIRouter(
    prefix="/api/iorganizations",
    tags=["iorganizations"],
)
adapter = PrismaAdapter()

@router.get("/")
async def get():
    return await service.fetch_all()

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
async def get_by_id(uid: str):
    return await service.fetch_some(where={"uid": uid})

@router.delete("/")
async def delete(where = None):
    return await service.delete(where=where)

@router.put("/")
async def update(where = None, data = None):
    return await service.update(where=where, data=data)

@router.post("/")
async def create(data):
    return await service.create(data=data)

@router.post("/upload")
async def upload(file: UploadFile):
    data_source = file.filename
    return await service.upload_organizations(data_source=data_source, buffer=file.file)

@router.get("/search/")
async def search(query: QueryArgs = Depends()):
    query_args = adapter.to_query_args(query=query.query)
    return await service.fetch_paged(where=query_args, take=query.take, skip=query.take*query.page)

@router.get("/search.paged/")
async def search(query: QueryArgs = Depends()):
    query_args = adapter.to_query_args(query=query.query)
    response = await service.fetch_paged(where=query_args, take=query.take, skip=query.take*query.page)
    return {"response": response, "count": await service.fetch_count(where=query_args), }

@router.post("/add/")
async def search(query: QueryArgs = Depends(), request_data = None):
    query_args = adapter.to_query_args(query=query.query)
    return await service.create(where=query_args, data=request_data)

@router.put("/edit/")
async def search(query: QueryArgs = Depends(), request_data = None):
    query_args = adapter.to_query_args(query=query.query)
    return await service.upsert(where=query_args, data=request_data)
