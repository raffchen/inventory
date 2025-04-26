from typing import Annotated, Any

from app.crud import lenses
from app.dependencies.core import DBSessionDep
from app.dependencies.exceptions import (
    MalformedInput,
    ProductAlreadyExists,
    ProductNotFound,
    ProductsNotFound,
)
from app.schemas.lenses import LensCreate, LensRead, LensUpdate
from fastapi import APIRouter, HTTPException, Query, Response
from pydantic.types import Json

router = APIRouter(
    prefix="/api/inventory",
    tags=["inventory"],
    responses={404: {"description": "Not found"}},
)


@router.get("/lenses", response_model=list[LensRead])
async def read_lenses(
    db_session: DBSessionDep,
    response: Response,
    sort: Annotated[Json[list[list[str]]] | None, Query()] = None,
    range: Annotated[Json[list[int]] | None, Query(min_length=2, max_length=2)] = None,
    filter: Annotated[Json | None, Query()] = None,
):
    try:
        products, total = await lenses.get_lenses(db_session, sort, range, filter)
    except MalformedInput as e:
        raise HTTPException(status_code=400, detail=str(e))

    if range:
        response.headers["Content-Range"] = (
            f"items {range[0]}-{range[0] + len(products) - 1}/{total}"
        )

    return products


@router.get("/lenses/all", response_model=list[LensRead])
# TODO: update to match /products
async def read_all_products(db_session: DBSessionDep):
    try:
        products, total = await lenses.get_lenses(db_session, show_deleted=True)
    except ProductsNotFound as e:
        return []

    return products


@router.get("/lenses/{product_id}", response_model=LensRead)
async def read_product(db_session: DBSessionDep, product_id: int):
    try:
        product = await lenses.get_lens(db_session, product_id)
    except ProductNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))

    return product


@router.post("/lenses", response_model=LensRead)
async def create_product(db_session: DBSessionDep, product: LensCreate):
    try:
        product = await lenses.create_or_replace_lens(db_session, product)
    except ProductAlreadyExists as e:
        raise HTTPException(status_code=400, detail=str(e))

    return product


@router.put("/lenses/{product_id}", response_model=LensRead)
async def update_product(
    db_session: DBSessionDep, product_id: int, update_data: LensUpdate
):
    try:
        product = await lenses.update_lens(db_session, product_id, update_data)
    except ProductNotFound as e:
        raise HTTPException(status_code=400, detail=str(e))

    return product


@router.delete("/lenses/{product_id}")
async def delete_product(db_session: DBSessionDep, product_id: int):
    try:
        message = await lenses.delete_lens(db_session, product_id)
    except ProductNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))

    return message
