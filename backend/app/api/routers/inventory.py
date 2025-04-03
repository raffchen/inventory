from app.api.dependencies.core import DBSessionDep
from app.crud.inventory import get_products
from app.schemas.inventory import Product
from fastapi import APIRouter

router = APIRouter(
    prefix="/api/inventory",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[Product])
async def read_products(db_session: DBSessionDep):
    user = await get_products(db_session)
    return user
