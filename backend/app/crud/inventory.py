from app.models import Product as ProductDBModel
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_products(db_session: AsyncSession):
    items = (await db_session.scalars(select(ProductDBModel))).all()
    if not items:
        raise HTTPException(status_code=404, detail="No items found")
    return items
