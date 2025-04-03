from datetime import datetime, timezone

from app.dependencies.enums import UpdateField, UpdateType
from app.dependencies.exceptions import (
    ProductAlreadyExists,
    ProductNotFound,
    ProductsNotFound,
)
from app.models import ProductHistory, Product
from app.schemas import ProductCreate, ProductUpdate
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
    # TODO: If soft deleted product with matching id exists, replace
    try:
        new_product = Product(**product.model_dump(exclude_unset=True))
        db_session.add(new_product)

        await db_session.flush()

        history_entries = [
            ProductHistory(
                product_id=new_product.id,
                update_field=field,
                old_value=None,
                new_value=str(value),
                update_type=UpdateType.CREATE,
            )
            for value, field in zip(
                [
                    new_product.name,
                    new_product.description,
                    new_product.quantity,
                ],
                [UpdateField.NAME, UpdateField.DESCRIPTION, UpdateField.QUANTITY],
            )
        ]
        db_session.add_all(history_entries)

        await db_session.commit()
        await db_session.refresh(new_product)

        return new_product
    except IntegrityError:
        await db_session.rollback()
        raise ProductAlreadyExists(product.id)
    except Exception as e:
        await db_session.rollback()
        raise RuntimeError(f"Database error {type(e)}: {e}")


async def update_product(
    db_session: AsyncSession, product_id: int, update_data: ProductUpdate
):
    get_field: dict[str, UpdateField] = {
        "name": UpdateField.NAME,
        "description": UpdateField.DESCRIPTION,
        "quantity": UpdateField.QUANTITY,
    }

    product = (
        await db_session.execute(select(Product).where(Product.id == product_id))
    ).scalar_one_or_none()

    if not product:
        raise ProductNotFound(product_id)

    update_dict = update_data.model_dump(exclude_unset=True)

    history_entries = []

    for key, value in update_dict.items():
        if (old_val := getattr(product, key)) != value:
            setattr(product, key, value)
            history_entries.append(
                ProductHistory(
                    product_id=product_id,
                    update_field=get_field[key],
                    old_value=str(old_val),
                    new_value=str(value),
                    update_type=UpdateType.UPDATE,
                )
            )

    product.updated_at = datetime.now(timezone.utc)
    db_session.add_all(history_entries)

    try:
        await db_session.commit()
        await db_session.refresh(product)

        return product
    except Exception as e:
        await db_session.rollback()
        raise RuntimeError(f"Database error {type(e)}: {e}")


async def delete_product(db_session: AsyncSession, product_id: int):
    # TODO: Disable products instead of deleting
    product = (
        await db_session.execute(select(Product).where(Product.id == product_id))
    ).scalar_one_or_none()

    if not product:
        raise ProductNotFound(product_id)

    try:
        await db_session.delete(product)
        await db_session.commit()

        return {"message": f"Product with ID {product_id} deleted successfully"}
    except Exception as e:
        await db_session.rollback()
        raise RuntimeError(f"Database error {type(e)}: {e}")
