
from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import uvicorn
from app.foundation.task_tracker import TaskTracker
from app.iorganizations import router as iorganizations
from app.iorgsites import router as iorgsites
from app.region import router as region
from app.emission_data import router as emission_data
from app.database import  get_connection
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


client = get_connection()
task_tracker = TaskTracker()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Connecting to database...")
    get_connection()
    await client.connect()
    task_tracker.start_tracking()
    yield
    await client.disconnect()

app = FastAPI(lifespan=lifespan, default_response_class=ORJSONResponse)
app.include_router(iorgsites.router, default_response_class=ORJSONResponse)
app.include_router(iorganizations.router)
app.include_router(emission_data.router)
app.include_router(region.router)



@app.get("/api")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9091, log_level="info")

"""
run for development (auto-reload)
    uvicorn main:app --reload --port 9091
"""
