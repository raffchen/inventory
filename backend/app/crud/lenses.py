from datetime import datetime, timezone

from app.dependencies.exceptions import (
    MalformedInput,
    ProductAlreadyExists,
    ProductNotFound,
)
from app.models import Lenses, LensesHistory, UpdateField, UpdateType
from app.schemas import LensCreate, LensUpdate
from sqlalchemy import desc, func, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


async def get_lenses(
    db_session: AsyncSession,
    sort: list[str, str] = None,
    range: list[int, int] = None,
    filter: dict = None,
    show_deleted: bool = False,
):
    stmt = select(Lenses)

    if not show_deleted:
        stmt = stmt.where(Lenses.deleted_at.is_(None))

    if sort:
        field, direction = sort
        sort_column = getattr(Lenses, field, None)
        if not sort_column:
            raise MalformedInput(
                f"Requested sort on field {field} but field doesn't exist"
            )

        if direction == "ASC":
            stmt = stmt.order_by(field)
        elif direction == "DESC":
            stmt = stmt.order_by(desc(field))
        else:
            raise MalformedInput(f"Requested sort direction {direction} doesn't exist")
    else:
        stmt = stmt.order_by(Lenses.id)

    if filter:
        for field, value in filter.items():
            if field == "id":
                if isinstance(value, int):
                    stmt = stmt.where(Lenses.id == value)
                elif isinstance(value, list) and all(isinstance(i, int) for i in value):
                    stmt = stmt.where(Lenses.id.in_(value))
                else:
                    raise MalformedInput(f"Id filter must be int or list of ints")
            else:
                # TODO: handle custom filters e.g. {"show_deleted": true}
                # TODO: handle if value type doesn't match field e.g. {"name": 2}
                # TODO: handle fuzzy matching e.g. {"name": "cha"} searches for *cha*
                # TODO: once table fields are finalized, can turn this into a match statement
                filter_column = getattr(Lenses, field, None)
                if not filter_column:
                    raise MalformedInput(
                        f"Requested filter on field {field} but field doesn't exist"
                    )
                if isinstance(value, str):
                    stmt = stmt.where(filter_column.ilike(f"%{value}%"))
                else:
                    stmt = stmt.where(filter_column == value)

    total = 0

    if range:
        # calculate total before range is applied
        total = await db_session.scalar(select(func.count()).select_from(stmt))

        start, end = range
        if end < start:
            raise MalformedInput(f"Range end cannot be less than range start")
        stmt = stmt.offset(start).limit(end - start)

    lenses = (await db_session.scalars(stmt)).all()

    if not lenses:
        # if range is out of bounds, we need to set total back to 0
        total = 0

    return lenses, total


async def get_lens(db_session: AsyncSession, lens_id: int):
    lens = (
        await db_session.scalars(
            select(Lenses)
            .where(Lenses.id == lens_id)
            .where(Lenses.deleted_at.is_(None))
        )
    ).first()

    if not lens:
        raise ProductNotFound(lens_id)

    return lens


async def create_lens(db_session: AsyncSession, lens: LensCreate):
    # TODO: allow update_source
    try:
        new_lens = Lenses(**lens.model_dump(exclude_unset=True))
        db_session.add(new_lens)

        await db_session.flush()

        history_entries = [
            LensesHistory(
                lens_id=new_lens.id,
                update_field=field,
                old_value=None,
                new_value=str(value),
                update_type=UpdateType.CREATE,
            )
            for value, field in zip(
                [
                    new_lens.lens_type,
                    new_lens.sphere,
                    new_lens.cylinder,
                    new_lens.unit_price,
                    new_lens.quantity,
                    new_lens.storage_limit,
                    new_lens.comment,
                ],
                [
                    UpdateField.LENS_TYPE,
                    UpdateField.SPHERE,
                    UpdateField.CYLINDER,
                    UpdateField.UNIT_PRICE,
                    UpdateField.QUANTITY,
                    UpdateField.STORAGE_LIMIT,
                    UpdateField.COMMENT,
                ],
            )
        ]
        db_session.add_all(history_entries)

        await db_session.commit()
        await db_session.refresh(new_lens)

        return new_lens
    except IntegrityError as e:
        await db_session.rollback()
        raise ProductAlreadyExists(f"Lens with id {lens.id} already exists")
    except Exception as e:
        await db_session.rollback()
        raise RuntimeError(f"Database error {type(e)}: {e}")


async def replace_lens(db_session: AsyncSession, lens: Lenses, update_data: LensCreate):
    get_field: dict[str, UpdateField] = {
        "lens_type": UpdateField.LENS_TYPE,
        "sphere": UpdateField.SPHERE,
        "cylinder": UpdateField.CYLINDER,
        "unit_price": UpdateField.UNIT_PRICE,
        "quantity": UpdateField.QUANTITY,
        "storage_limit": UpdateField.STORAGE_LIMIT,
        "comment": UpdateField.COMMENT,
    }

    update_dict = update_data.model_dump(exclude_unset=True)
    del update_dict["id"]

    history_entries = []

    for key, value in update_dict.items():
        if (old_val := getattr(lens, key)) != value:
            setattr(lens, key, value)
        history_entries.append(
            LensesHistory(
                lens_id=lens.id,
                update_field=get_field[key],
                old_value=str(old_val),
                new_value=str(value),
                update_type=UpdateType.CREATE,
            )
        )

    history_entries.append(
        LensesHistory(
            lens_id=lens.id,
            update_field=UpdateField.DELETED_AT,
            old_value=str(lens.deleted_at),
            new_value=None,
            update_type=UpdateType.CREATE,
        )
    )

    lens.updated_at = datetime.now(timezone.utc)
    lens.deleted_at = None

    db_session.add_all(history_entries)

    try:
        await db_session.commit()
        await db_session.refresh(lens)

        return lens
    except Exception as e:
        await db_session.rollback()
        raise RuntimeError(f"Database error {type(e)}: {e}")


async def create_or_replace_lens(db_session: AsyncSession, lens: LensCreate):
    check = (
        await db_session.execute(select(Lenses).where(Lenses.id == lens.id))
    ).scalar_one_or_none()

    if check:
        if check.deleted_at is None:
            raise ProductAlreadyExists(lens.id)
        else:
            return await replace_lens(db_session, check, lens)

    return await create_lens(db_session, lens)


async def update_lens(db_session: AsyncSession, lens_id: int, update_data: LensUpdate):
    get_field: dict[str, UpdateField] = {
        "lens_type": UpdateField.LENS_TYPE,
        "sphere": UpdateField.SPHERE,
        "cylinder": UpdateField.CYLINDER,
        "unit_price": UpdateField.UNIT_PRICE,
        "quantity": UpdateField.QUANTITY,
        "storage_limit": UpdateField.STORAGE_LIMIT,
        "comment": UpdateField.COMMENT,
    }

    lens = (
        await db_session.execute(
            select(Lenses)
            .where(Lenses.id == lens_id)
            .where(Lenses.deleted_at.is_(None))
        )
    ).scalar_one_or_none()

    if not lens:
        raise ProductNotFound(lens_id)

    update_dict = update_data.model_dump(exclude_unset=True)

    update_notes = update_dict.get("update_notes")
    update_source = update_dict.get("update_source")

    history_entries = []

    for key, value in update_dict.items():
        if key in ["update_notes", "update_source"]:
            # TODO: handle these values
            continue

        if (old_val := getattr(lens, key)) != value:
            setattr(lens, key, value)
            history_entries.append(
                LensesHistory(
                    lens_id=lens_id,
                    update_field=get_field[key],
                    old_value=str(old_val),
                    new_value=str(value),
                    update_type=UpdateType.UPDATE,
                    update_notes=update_notes,
                    update_source=update_source,
                )
            )

    lens.updated_at = datetime.now(timezone.utc)
    db_session.add_all(history_entries)

    try:
        await db_session.commit()
        await db_session.refresh(lens)

        return lens
    except Exception as e:
        await db_session.rollback()
        raise RuntimeError(f"Database error {type(e)}: {e}")


async def delete_lens(db_session: AsyncSession, lens_id: int):
    lens = (
        await db_session.execute(
            select(Lenses)
            .where(Lenses.id == lens_id)
            .where(Lenses.deleted_at.is_(None))
        )
    ).scalar_one_or_none()

    if not lens:
        raise ProductNotFound(lens_id)

    try:
        utc_now = datetime.now(timezone.utc)

        stmt = update(Lenses).where(Lenses.id == lens_id).values(deleted_at=utc_now)
        await db_session.execute(stmt)

        db_session.add(
            LensesHistory(
                lens_id=lens_id,
                update_field=UpdateField.DELETED_AT,
                old_value=None,
                new_value=str(utc_now),
                update_type=UpdateType.DELETE,
            )
        )

        await db_session.commit()

        return {"message": f"Lens with ID {lens_id} deleted successfully"}
    except Exception as e:
        await db_session.rollback()
        raise RuntimeError(f"Database error {type(e)}: {e}")
