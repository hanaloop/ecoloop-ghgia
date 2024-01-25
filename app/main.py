
from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import uvicorn
from app.iorganizations import router as iorganizations
from app.iorgsites import router as iorgsites
from app.region import router as region
from app.emission_data import router as emission_data
from app.database import  get_connection
from app.code import router as code

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


client = get_connection()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Connecting to database...")
    
    get_connection()
    await client.connect()
    yield
    await client.disconnect()

app = FastAPI(lifespan=lifespan, default_response_class=ORJSONResponse)
app.include_router(iorgsites.router, default_response_class=ORJSONResponse)
app.include_router(iorganizations.router)
app.include_router(emission_data.router)
app.include_router(region.router)
app.include_router(code.router)

api_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)



@app.get("/api")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9091)

"""
run for development (auto-reload)
    uvicorn main:app --reload --port 9091
"""
