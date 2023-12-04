
from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from app.iorganizations import router as iorganizations
from app.iorgsites import router as iorgsites
from app.database import  get_connection

client = get_connection()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Connecting to database...")
    get_connection()
    await client.connect()
    yield
    await client.disconnect()

app = FastAPI(lifespan=lifespan)
app.include_router(iorgsites.router)
app.include_router(iorganizations.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9090,)

"""
run for development (auto-reload)
    uvicorn main:app --reload --port 9090
"""
