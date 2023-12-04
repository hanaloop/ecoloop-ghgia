from fastapi import APIRouter, UploadFile
import prisma
from iorgsites.service import FactoryOnSiteService


service = FactoryOnSiteService()
router = APIRouter(
    prefix="/api/iorgsites",
    tags=["iorgsites"],
)

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

@router.get("/{id}")
async def get_by_id(id):
    return await service.fetch_some(where={"id": id})

@router.delete("/") ##TODO: Need auth
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
    return await service.upload_iorgsites(data_source=data_source, buffer=file.file)