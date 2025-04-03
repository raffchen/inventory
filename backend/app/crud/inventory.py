from datetime import datetime, timezone

from app.models import Product
from app.schemas import ProductCreate, ProductUpdate
from app.dependencies.exceptions import (
    ProductsNotFound,
    ProductNotFound,
    ProductAlreadyExists,
)
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


async def get_products(db_session: AsyncSession):
    products = (await db_session.scalars(select(Product))).all()

    if not products:
        raise ProductsNotFound()

    return products


async def get_product(db_session: AsyncSession, product_id: int):
    product = (
        await db_session.scalars(select(Product).where(Product.id == product_id))
    ).first()

    if not product:
        raise ProductNotFound(product_id)

    return product


async def create_product(db_session: AsyncSession, product: ProductCreate):
    new_product = Product(**product.model_dump(exclude_unset=True))
    db_session.add(new_product)

    try:
        await db_session.commit()
        await db_session.refresh(new_product)
        return new_product
    except IntegrityError:
        await db_session.rollback()
        raise ProductAlreadyExists(product.id)


async def update_product(
    db_session: AsyncSession, product_id: int, update_data: ProductUpdate
):
    product = (
        await db_session.execute(select(Product).where(Product.id == product_id))
    ).scalar_one_or_none()

    if not product:
        raise ProductNotFound(product_id)

    update_dict = update_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(product, key, value)

    product.updated_at = datetime.now(timezone.utc)

    await db_session.commit()
    await db_session.refresh(product)

    return product


async def delete_product(db_session: AsyncSession, product_id: int):
    product = (
        await db_session.execute(select(Product).where(Product.id == product_id))
    ).scalar_one_or_none()

    if not product:
        raise ProductNotFound(product_id)

    await db_session.delete(product)
    await db_session.commit()

    return {"message": f"Product with ID {product_id} deleted successfully"}
