from fastapi import APIRouter
from app.region.service import RegionService


service = RegionService()
router = APIRouter(
    prefix="/api",
    tags=["region"],
)

@router.get("/region/")
async def get():
    return await service.fetch_all()

@router.get("/region/count")
async def count():
    return await service.fetch_count()

@router.get("/region/paged")
async def paged(skip: int = 0, limit: int = 10):
    return await service.fetch_paged(skip=skip, take=limit)

@router.get("/region/group")
async def group(count=None, by = None, sum = None, order = None, having = None):
    return await service.group_by(count = count, by = by, sum = sum, order = order, having = having)

@router.get("/region/{uid}")
async def get_by_id(uid):
    return await service.fetch_some(where={"uid": uid})

@router.delete("/region/") ##TODO: Need auth
async def delete(where = None):
    return await service.delete(where=where)

@router.put("/region/")
async def update(where = None, data = None):
    return await service.update(where=where, data=data)

@router.post("/region/")
async def create(data):
    return await service.create(data=data)

