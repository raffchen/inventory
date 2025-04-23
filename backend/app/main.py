import logging
import sys
from contextlib import asynccontextmanager

import uvicorn
from app.config import settings
from app.database import sessionmanager
from app.models import Lenses
from app.routers.inventory import router as inventory_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette_admin.contrib.sqla import Admin, ModelView

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

admin = Admin(sessionmanager._engine, title="Test")
admin.add_view(ModelView(Lenses))
admin.mount_to(app)


@app.get("/")
async def root():
    return {"message": "Hello World"}
