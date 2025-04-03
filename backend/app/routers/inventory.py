from app.dependencies.core import DBSessionDep
from app.crud import inventory
from app.schemas.inventory import ProductCreate, ProductRead, ProductUpdate
from app.dependencies.exceptions import (
    ProductsNotFound,
    ProductNotFound,
    ProductAlreadyExists,
)
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/api/inventory",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[ProductRead])
async def read_products(db_session: DBSessionDep):
    try:
        products = await inventory.get_products(db_session)
    except ProductsNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))

    return products


@router.get("/{product_id}", response_model=ProductRead)
async def read_product(db_session: DBSessionDep, product_id: int):
    try:
        product = await inventory.get_product(db_session, product_id)
    except ProductNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))

    return product


@router.post("/", response_model=ProductRead)
async def create_product(db_session: DBSessionDep, product: ProductCreate):
    product = ProductCreate.model_validate(product)

    try:
        product = await inventory.create_product(db_session, product)
    except ProductAlreadyExists as e:
        raise HTTPException(status_code=403, detail=str(e))

    return product


@router.put("/{product_id}", response_model=ProductRead)
async def update_product(
    db_session: DBSessionDep, product_id: int, update_data: ProductUpdate
):
    product = ProductUpdate.model_validate(update_data)

    try:
        product = await inventory.update_product(db_session, product_id, update_data)
    except ProductNotFound as e:
        raise HTTPException(status_code=403, detail=str(e))

    return product


@router.delete("/{product_id}")
async def delete_product(db_session: DBSessionDep, product_id: int):
    try:
        message = await inventory.delete_product(db_session, product_id)
    except ProductNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))

    return message
