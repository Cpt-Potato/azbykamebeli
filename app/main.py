from fastapi import FastAPI

from . import api
from db.base import database

app = FastAPI()

app.include_router(api.router, prefix="/api", tags=["API"])


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
