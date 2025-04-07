import logging
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.routers.inventory import router as inventory_router
from app.config import settings
from app.database import sessionmanager


logging.basicConfig(stream=sys.stdout, level=settings.log_level)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan)
app.include_router(inventory_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
