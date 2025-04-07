import pytest
from app.main import app as main_app
from app.models import ProductHistory
from app.dependencies.enums import UpdateField, UpdateType
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select


@pytest.mark.asyncio(loop_scope="session")
async def test_create_product_history(test_db_session):
    product_data = {
        "id": 1,
        "name": "Table",
        "description": "A table",
        "quantity": 5,
    }

    async with AsyncClient(
        transport=ASGITransport(app=main_app), base_url="http://test"
    ) as client:
        await client.post("/api/inventory/", json=product_data)

    history_list = (await test_db_session.scalars(select(ProductHistory))).all()

    for history in history_list:
        assert history.product_id == 1
        assert history.old_value == None
        assert history.update_type == UpdateType.CREATE

        match history.update_field:
            case UpdateField.NAME:
                assert history.new_value == "Table"
            case UpdateField.DESCRIPTION:
                assert history.new_value == "A table"
            case UpdateField.QUANTITY:
                assert history.new_value == "5"


@pytest.mark.asyncio(loop_scope="session")
async def test_update_product_history(test_db_session):
    product_data = {
        "id": 1,
        "name": "Table",
        "description": "A table",
        "quantity": 5,
    }
    update_data = {
        "name": "Chair",
        "description": "A chair",
        "quantity": 7,
        "update_notes": "The table became a chair",
        "update_source": "admin",
    }

    async with AsyncClient(
        transport=ASGITransport(app=main_app), base_url="http://test"
    ) as client:
        await client.post("/api/inventory/", json=product_data)
        await client.put("/api/inventory/1", json=update_data)

    history_list = (
        await test_db_session.scalars(
            select(ProductHistory).where(
                ProductHistory.update_type != UpdateType.CREATE
            )
        )
    ).all()

    for history in history_list:
        assert history.product_id == 1
        assert history.update_type == UpdateType.UPDATE
        assert history.update_notes == "The table became a chair"
        assert history.update_source == "admin"

        match history.update_field:
            case UpdateField.NAME:
                assert history.old_value == "Table"
                assert history.new_value == "Chair"
            case UpdateField.DESCRIPTION:
                assert history.old_value == "A table"
                assert history.new_value == "A chair"
            case UpdateField.QUANTITY:
                assert history.old_value == "5"
                assert history.new_value == "7"


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_product_history(test_db_session):
    product_data = {
        "id": 1,
        "name": "Table",
        "description": "A table",
        "quantity": 5,
    }

    async with AsyncClient(
        transport=ASGITransport(app=main_app), base_url="http://test"
    ) as client:
        await client.post("/api/inventory/", json=product_data)
        await client.delete("/api/inventory/1")

    history_list = (
        await test_db_session.scalars(
            select(ProductHistory).where(
                ProductHistory.update_type != UpdateType.CREATE
            )
        )
    ).all()

    for history in history_list:
        assert history.product_id == 1
        assert history.update_type == UpdateType.DELETE
        assert history.update_field == UpdateField.DELETED_AT
        assert history.old_value == None
        assert history.new_value is not None


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_then_create_product_history(test_db_session):
    product_data1 = {
        "id": 1,
        "name": "Table",
        "description": "A table",
        "quantity": 5,
    }
    product_data2 = {
        "id": 1,
        "name": "Chair",
        "description": "A chair",
        "quantity": 7,
    }

    async with AsyncClient(
        transport=ASGITransport(app=main_app), base_url="http://test"
    ) as client:
        await client.post("/api/inventory/", json=product_data1)
        await client.delete("/api/inventory/1")
        await client.post("/api/inventory/", json=product_data2)

    history_list = (
        await test_db_session.scalars(
            select(ProductHistory)
            .where(ProductHistory.update_type == UpdateType.CREATE)
            .where(ProductHistory.old_value != None)
        )
    ).all()

    for history in history_list:
        assert history.product_id == 1
        assert history.update_type == UpdateType.CREATE

        match history.update_field:
            case UpdateField.NAME:
                assert history.old_value == "Table"
                assert history.new_value == "Chair"
            case UpdateField.DESCRIPTION:
                assert history.old_value == "A table"
                assert history.new_value == "A chair"
            case UpdateField.QUANTITY:
                assert history.old_value == "5"
                assert history.new_value == "7"
            case UpdateField.DELETED_AT:
                assert history.old_value is not None
                assert history.new_value is None
