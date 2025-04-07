import datetime

import pytest
import pytest_asyncio
from app.database import Base, DatabaseSessionManager, get_db_session
from app.main import app as main_app
from httpx import ASGITransport, AsyncClient
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor

test_db = factories.postgresql_proc(port=None, dbname="test_db")


@pytest_asyncio.fixture(scope="session")
async def test_sessionmanager(test_db):
    with DatabaseJanitor(
        user=test_db.user,
        host=test_db.host,
        port=test_db.port,
        dbname=test_db.dbname,
        version=test_db.version,
        password=test_db.password,
    ):
        connection_str = "postgresql+asyncpg://{}@{}:{}/{}".format(
            test_db.user, test_db.host, test_db.port, test_db.dbname
        )
        sessionmanager = DatabaseSessionManager(connection_str)
        async with sessionmanager.connect() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield sessionmanager


@pytest_asyncio.fixture(scope="session")
async def test_db_session(test_sessionmanager):
    async with test_sessionmanager.session() as session:
        yield session


@pytest.fixture(scope="session", autouse=True)
def override_get_db_session(test_db_session):
    async def _override():
        yield test_db_session

    main_app.dependency_overrides[get_db_session] = _override


@pytest.fixture(autouse=True)
async def cleanup_db(test_db_session):
    for table in reversed(Base.metadata.sorted_tables):
        await test_db_session.execute(table.delete())
    await test_db_session.commit()


def compare_returned_json(
    resp_dict: dict,
    source_dict: dict,
    ignored: list[str] = ["created_at", "updated_at"],
) -> bool:
    # remove ignored fields
    d1 = {k: v for k, v in resp_dict.items() if k not in ignored}
    d2 = {k: v for k, v in source_dict.items() if k not in ignored}
    return d1 == d2


@pytest.mark.asyncio(loop_scope="session")
async def test_get_products_empty():
    async with AsyncClient(
        transport=ASGITransport(app=main_app), base_url="http://test"
    ) as client:
        resp = await client.get("/api/inventory/")

        assert resp.status_code == 200
        assert len(resp.json()) == 0


@pytest.mark.asyncio(loop_scope="session")
async def test_get_product_not_exist():
    async with AsyncClient(
        transport=ASGITransport(app=main_app), base_url="http://test"
    ) as client:
        resp = await client.get("/api/inventory/1")

        assert resp.status_code == 404


@pytest.mark.asyncio(loop_scope="session")
async def test_create_one_product():
    product_data = {
        "id": 1,
        "name": "Table",
        "description": "A table",
        "quantity": 5,
    }

    async with AsyncClient(
        transport=ASGITransport(app=main_app), base_url="http://test"
    ) as client:
        assert (
            await client.post(
                "/api/inventory/",
                json=product_data,
            )
        ).status_code == 200

        # test that product shows up in list of all products
        get_resp = await client.get("/api/inventory/")

        assert get_resp.status_code == 200

        ret = get_resp.json()

        assert len(ret) == 1
        assert compare_returned_json(ret[0], product_data)

        # test that product gets its own endpoint
        get_resp = await client.get("/api/inventory/1")

        assert get_resp.status_code == 200
        assert compare_returned_json(get_resp.json(), product_data)


@pytest.mark.asyncio(loop_scope="session")
async def test_create_multiple_products():
    product_data1 = {
        "id": 1,
        "name": "Table",
        "description": "A table",
        "quantity": 5,
    }
    product_data2 = {
        "id": 2,
        "name": "Chair",
        "description": "A chair",
        "quantity": 7,
    }

    async with AsyncClient(
        transport=ASGITransport(app=main_app), base_url="http://test"
    ) as client:
        post_resp1 = await client.post("/api/inventory/", json=product_data1)
        post_resp2 = await client.post("/api/inventory/", json=product_data2)

        assert post_resp1.status_code == 200
        assert post_resp2.status_code == 200

        # test that all products show up
        get_resp = await client.get("/api/inventory/")
        ret = get_resp.json()

        assert len(ret) == 2

        # products are ordered by id
        assert compare_returned_json(ret[0], product_data1)
        assert compare_returned_json(ret[1], product_data2)

        # test that each product gets its own endpoint
        get_resp = await client.get("/api/inventory/1")

        assert get_resp.status_code == 200
        assert compare_returned_json(get_resp.json(), product_data1)

        get_resp = await client.get("/api/inventory/2")

        assert get_resp.status_code == 200
        assert compare_returned_json(get_resp.json(), product_data2)


@pytest.mark.asyncio(loop_scope="session")
async def test_create_products_with_same_id():
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
        post_resp = await client.post("/api/inventory/", json=product_data2)

        assert post_resp.status_code == 400

        # make sure original data is still there
        get_resp = await client.get("/api/inventory/")
        ret = get_resp.json()

        assert len(ret) == 1
        assert compare_returned_json(ret[0], product_data1)

        get_resp = await client.get("/api/inventory/1")

        assert get_resp.status_code == 200
        assert compare_returned_json(get_resp.json(), product_data1)


@pytest.mark.asyncio(loop_scope="session")
async def test_update_product():
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

        put_resp = await client.put("/api/inventory/1", json=update_data)

        assert put_resp.status_code == 200

        get_resp = await client.get("/api/inventory/1")
        ret = get_resp.json()

        # check that updated_at is newer
        assert datetime.datetime.strptime(
            ret["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z"
        ) > datetime.datetime.strptime(ret["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
        assert compare_returned_json(
            ret,
            update_data,
            ["id", "update_notes", "update_source", "created_at", "updated_at"],
        )


@pytest.mark.asyncio(loop_scope="session")
async def test_update_product_not_exist():
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
        put_resp = await client.put("/api/inventory/1", json=update_data)

        assert put_resp.status_code == 400


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_product():
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

        # product shows up in list of all products
        get_resp = await client.get("/api/inventory/")

        assert len(get_resp.json()) == 1

        # product endpoint exists
        get_resp = await client.get("/api/inventory/1")

        assert get_resp.status_code == 200

        # delete
        delete_resp = await client.delete("/api/inventory/1")

        assert delete_resp.status_code == 200

        # product doesn't show up in list of all products
        get_resp = await client.get("/api/inventory/")

        assert len(get_resp.json()) == 0

        # product endpoint doesn't exist
        get_resp = await client.get("/api/inventory/1")

        assert get_resp.status_code == 404


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_product_not_exists():
    async with AsyncClient(
        transport=ASGITransport(app=main_app), base_url="http://test"
    ) as client:
        delete_resp = await client.delete("/api/inventory/1")

        assert delete_resp.status_code == 404


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_product_then_create_product_with_same_id():
    async with AsyncClient(
        transport=ASGITransport(app=main_app), base_url="http://test"
    ) as client:
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
            "quantity": 6,
        }

        await client.post("/api/inventory/", json=product_data1)
        await client.delete("/api/inventory/1")

        post_resp = await client.post("/api/inventory/", json=product_data2)

        assert post_resp.status_code == 200

        get_resp = await client.get("/api/inventory/")
        ret = get_resp.json()

        assert len(ret) == 1
        assert compare_returned_json(ret[0], product_data2)

        # test that product gets its own endpoint
        get_resp = await client.get("/api/inventory/1")

        assert get_resp.status_code == 200
        assert compare_returned_json(get_resp.json(), product_data2)
