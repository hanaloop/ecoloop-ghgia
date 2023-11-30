from typing import List, Dict, Optional

from fastapi import FastAPI
import uvicorn

from pydantic import BaseModel
from iorgSites import router as iOrgSites
from database import  get_connection

app = FastAPI()
client = get_connection()

app.include_router(iOrgSites.router)

@app.on_event("startup")
async def startup_event():
    await client.connect()

@app.on_event("shutdown")
async def shutdown_event():
    await client.disconnect()

@app.get("/api/info")
async def info():
    return "api is running"




if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9090)

"""
run for development (auto-reload)
    uvicorn main:app --reload --port 9090
"""
