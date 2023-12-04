
from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from iorgsites import router as iorgsites
from database import  get_connection

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

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9090,)

"""
run for development (auto-reload)
    uvicorn main:app --reload --port 9090
"""
