from typing import List, Dict, Optional

from fastapi import FastAPI
import uvicorn

from pydantic import BaseModel



app = FastAPI()



@app.get("/api/info")
async def info():
    return "Hello World"




if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9090)

"""
run for development (auto-reload)
    uvicorn main:app --reload --port 9090
"""
