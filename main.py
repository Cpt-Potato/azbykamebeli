from fastapi import FastAPI

import api
from db.base import database

app = FastAPI()

app.include_router(api.router, prefix="/api", tags=["API"])


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
