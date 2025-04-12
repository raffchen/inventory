from typing import Annotated, Any

from app.crud import inventory
from app.dependencies.core import DBSessionDep
from app.dependencies.exceptions import (
    MalformedInput,
    ProductAlreadyExists,
    ProductNotFound,
    ProductsNotFound,
)
from app.schemas.inventory import (
    ProductCreate,
    ProductRead,
    ProductReadFull,
    ProductUpdate,
)
from fastapi import APIRouter, HTTPException, Query, Response
from pydantic.types import Json

router = APIRouter(
    prefix="/api/inventory",
    tags=["inventory"],
    responses={404: {"description": "Not found"}},
)


@router.get("/products", response_model=list[ProductRead])
async def read_products(
    db_session: DBSessionDep,
    response: Response,
    sort: Annotated[Json[list[str]] | None, Query(min_length=2, max_length=2)] = None,
    range: Annotated[Json[list[int]] | None, Query(min_length=2, max_length=2)] = None,
    filter: Annotated[Json[dict[str, Any]] | None, Query()] = None,
):
    try:
        products, total = await inventory.get_products(db_session, sort, range, filter)
    except ProductsNotFound as e:
        products, total = [], 0
    except MalformedInput as e:
        raise HTTPException(status_code=400, detail=str(e))

    if range:
        response.headers["Content-Range"] = (
            f"items {range[0]}-{int(total == 0) + range[0] + len(products) - 1}/{total}"
        )

    return products


@router.get("/products/all", response_model=list[ProductReadFull])
# TODO: update to match /products
async def read_all_products(db_session: DBSessionDep):
    try:
        products, total = await inventory.get_products(db_session, show_deleted=True)
    except ProductsNotFound as e:
        return []

    return products


@router.get("/products/{product_id}", response_model=ProductRead)
async def read_product(db_session: DBSessionDep, product_id: int):
    try:
        product = await inventory.get_product(db_session, product_id)
    except ProductNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))

    return product


@router.post("/products", response_model=ProductRead)
async def create_product(db_session: DBSessionDep, product: ProductCreate):
    product = ProductCreate.model_validate(product)

    try:
        product = await inventory.create_or_replace_product(db_session, product)
    except ProductAlreadyExists as e:
        raise HTTPException(status_code=400, detail=str(e))

    return product


@router.put("/products/{product_id}", response_model=ProductRead)
async def update_product(
    db_session: DBSessionDep, product_id: int, update_data: ProductUpdate
):
    product = ProductUpdate.model_validate(update_data)

    try:
        product = await inventory.update_product(db_session, product_id, update_data)
    except ProductNotFound as e:
        raise HTTPException(status_code=400, detail=str(e))

    return product


@router.delete("/products/{product_id}")
async def delete_product(db_session: DBSessionDep, product_id: int):
    try:
        message = await inventory.delete_product(db_session, product_id)
    except ProductNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))

    return message
