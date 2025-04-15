import datetime

import pytest
from app.main import app as main_app
from httpx import ASGITransport, AsyncClient

# TODO: add tests for sort, range, and filter query parameters


def compare_returned_json(
    resp_dict: dict,
    source_dict: dict,
    ignored: list[str] = ["created_at", "updated_at", "deleted_at"],
) -> bool:
    # remove ignored fields
    d1 = {k: v for k, v in resp_dict.items() if k not in ignored}
    d2 = {k: v for k, v in source_dict.items() if k not in ignored}
    return d1 == d2


@pytest.mark.asyncio(loop_scope="session")
async def test_get_lenses_empty():
    async with AsyncClient(
        transport=ASGITransport(app=main_app), base_url="http://test"
    ) as client:
        resp = await client.get("/api/inventory/lenses")

        assert resp.status_code == 200
        assert len(resp.json()) == 0


@pytest.mark.asyncio(loop_scope="session")
async def test_get_lens_not_exist():
    async with AsyncClient(
        transport=ASGITransport(app=main_app), base_url="http://test"
    ) as client:
        resp = await client.get("/api/inventory/lenses/1")

        assert resp.status_code == 404


@pytest.mark.asyncio(loop_scope="session")
async def test_create_one_lens():
    product_data = {
        "id": 1,
        "lens_type": "CR39",
        "sphere": -2.00,
        "cylinder": -0.75,
        "unit_price": 45.00,
        "quantity": 5,
        "storage_limit": 100,
        "comment": "Test comment",
    }

    async with AsyncClient(
        transport=ASGITransport(app=main_app), base_url="http://test"
    ) as client:
        post_resp = await client.post("/api/inventory/lenses", json=product_data)

        assert post_resp.status_code == 200

        # test that lens shows up in list of all lenses
        get_resp = await client.get("/api/inventory/lenses")

        assert get_resp.status_code == 200

        ret = get_resp.json()

        assert len(ret) == 1
        assert compare_returned_json(ret[0], product_data)

        # test that lens gets its own endpoint
        get_resp = await client.get("/api/inventory/lenses/1")

        assert get_resp.status_code == 200
        assert compare_returned_json(
            get_resp.json(),
            product_data,
            ["created_at", "updated_at", "deleted_at"],
        )


@pytest.mark.asyncio(loop_scope="session")
async def test_create_multiple_lenses():
    product_data1 = {
        "id": 1,
        "lens_type": "CR39",
        "sphere": -2.00,
        "cylinder": -0.75,
        "unit_price": 45.00,
        "quantity": 5,
        "storage_limit": 100,
        "comment": "Test comment",
    }
    product_data2 = {
        "id": 2,
        "lens_type": "Polycarbonate",
        "sphere": -1.50,
        "cylinder": -1.25,
        "unit_price": 60.00,
        "quantity": 7,
        "storage_limit": 100,
        "comment": "Test comment",
    }

    async with AsyncClient(
        transport=ASGITransport(app=main_app), base_url="http://test"
    ) as client:
        post_resp1 = await client.post("/api/inventory/lenses", json=product_data1)
        post_resp2 = await client.post("/api/inventory/lenses", json=product_data2)

        assert post_resp1.status_code == 200
        assert post_resp2.status_code == 200

        # test that all lenses show up
        get_resp = await client.get("/api/inventory/lenses")
        ret = get_resp.json()

        assert len(ret) == 2

        # lenses are ordered by id
        assert compare_returned_json(ret[0], product_data1)
        assert compare_returned_json(ret[1], product_data2)

        # test that each lens gets its own endpoint
        get_resp = await client.get("/api/inventory/lenses/1")

        assert get_resp.status_code == 200
        assert compare_returned_json(get_resp.json(), product_data1)

        get_resp = await client.get("/api/inventory/lenses/2")

        assert get_resp.status_code == 200
        assert compare_returned_json(get_resp.json(), product_data2)


@pytest.mark.asyncio(loop_scope="session")
async def test_create_lenses_with_same_id():
    product_data1 = {
        "id": 1,
        "lens_type": "CR39",
        "sphere": -2.00,
        "cylinder": -0.75,
        "unit_price": 45.00,
        "quantity": 5,
        "storage_limit": 100,
        "comment": "Test comment",
    }
    product_data2 = {
        "id": 1,
        "lens_type": "Polycarbonate",
        "sphere": -1.50,
        "cylinder": -1.25,
        "unit_price": 60.00,
        "quantity": 7,
        "storage_limit": 100,
        "comment": "Test comment",
    }

    async with AsyncClient(
        transport=ASGITransport(app=main_app), base_url="http://test"
    ) as client:
        await client.post("/api/inventory/lenses", json=product_data1)
        post_resp = await client.post("/api/inventory/lenses", json=product_data2)

        assert post_resp.status_code == 400

        # make sure original data is still there
        get_resp = await client.get("/api/inventory/lenses")
        ret = get_resp.json()

        assert len(ret) == 1
        assert compare_returned_json(ret[0], product_data1)

        get_resp = await client.get("/api/inventory/lenses/1")

        assert get_resp.status_code == 200
        assert compare_returned_json(get_resp.json(), product_data1)


@pytest.mark.asyncio(loop_scope="session")
async def test_update_lens():
    product_data = {
        "id": 1,
        "lens_type": "CR39",
        "sphere": -2.00,
        "cylinder": -0.75,
        "unit_price": 45.00,
        "quantity": 5,
        "storage_limit": 100,
        "comment": "Test comment",
    }
    update_data = {
        "unit_price": 50.00,
        "quantity": 10,
        "storage_limit": 101,
        "comment": "Test comment",
        "update_notes": "Update lens",
        "update_source": "admin",
    }

    async with AsyncClient(
        transport=ASGITransport(app=main_app), base_url="http://test"
    ) as client:
        await client.post("/api/inventory/lenses", json=product_data)

        put_resp = await client.put("/api/inventory/lenses/1", json=update_data)

        assert put_resp.status_code == 200

        get_resp = await client.get("/api/inventory/lenses/1")
        ret = get_resp.json()

        # check that updated_at is newer
        assert datetime.datetime.strptime(
            ret["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z"
        ) > datetime.datetime.strptime(ret["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
        assert compare_returned_json(
            ret,
            update_data,
            [
                "id",
                "lens_type",
                "sphere",
                "cylinder",
                "update_notes",
                "update_source",
                "created_at",
                "updated_at",
                "deleted_at",
            ],
        )


@pytest.mark.asyncio(loop_scope="session")
async def test_update_lens_not_exist():
    update_data = {
        "unit_price": 50.00,
        "quantity": 10,
        "storage_limit": 101,
        "comment": "Test comment",
        "update_notes": "Update lens",
        "update_source": "admin",
    }

    async with AsyncClient(
        transport=ASGITransport(app=main_app), base_url="http://test"
    ) as client:
        put_resp = await client.put("/api/inventory/lenses/1", json=update_data)

        assert put_resp.status_code == 400


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_lens():
    product_data = {
        "id": 1,
        "lens_type": "CR39",
        "sphere": -2.00,
        "cylinder": -0.75,
        "unit_price": 45.00,
        "quantity": 5,
        "storage_limit": 100,
        "comment": "Test comment",
    }

    async with AsyncClient(
        transport=ASGITransport(app=main_app), base_url="http://test"
    ) as client:
        await client.post("/api/inventory/lenses", json=product_data)

        # lens shows up in list of all lenses
        get_resp = await client.get("/api/inventory/lenses")

        assert len(get_resp.json()) == 1

        # lens endpoint exists
        get_resp = await client.get("/api/inventory/lenses/1")

        assert get_resp.status_code == 200

        # delete
        delete_resp = await client.delete("/api/inventory/lenses/1")

        assert delete_resp.status_code == 200

        # lens doesn't show up in list of all lenses
        get_resp = await client.get("/api/inventory/lenses")

        assert len(get_resp.json()) == 0

        # lens endpoint doesn't exist
        get_resp = await client.get("/api/inventory/lenses/1")

        assert get_resp.status_code == 404


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_lens_not_exists():
    async with AsyncClient(
        transport=ASGITransport(app=main_app), base_url="http://test"
    ) as client:
        delete_resp = await client.delete("/api/inventory/lenses/1")

        assert delete_resp.status_code == 404


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_lens_then_create_lens_with_same_id():
    product_data1 = {
        "id": 1,
        "lens_type": "CR39",
        "sphere": -2.00,
        "cylinder": -0.75,
        "unit_price": 45.00,
        "quantity": 5,
        "storage_limit": 100,
        "comment": "Test comment",
    }
    product_data2 = {
        "id": 1,
        "lens_type": "Polycarbonate",
        "sphere": -1.50,
        "cylinder": -1.25,
        "unit_price": 60.00,
        "quantity": 7,
        "storage_limit": 100,
        "comment": "Test comment",
    }

    async with AsyncClient(
        transport=ASGITransport(app=main_app), base_url="http://test"
    ) as client:
        await client.post("/api/inventory/lenses", json=product_data1)
        await client.delete("/api/inventory/lenses/1")

        post_resp = await client.post("/api/inventory/lenses", json=product_data2)

        assert post_resp.status_code == 200

        get_resp = await client.get("/api/inventory/lenses")
        ret = get_resp.json()

        assert len(ret) == 1
        assert compare_returned_json(ret[0], product_data2)

        # test that lens gets its own endpoint
        get_resp = await client.get("/api/inventory/lenses/1")

        assert get_resp.status_code == 200
        assert compare_returned_json(get_resp.json(), product_data2)


@pytest.mark.asyncio(loop_scope="session")
async def test_can_see_deleted_lenses_with_all_endpoint():
    async with AsyncClient(
        transport=ASGITransport(app=main_app), base_url="http://test"
    ) as client:
        product_data = {
            "id": 1,
            "lens_type": "CR39",
            "sphere": -2.00,
            "cylinder": -0.75,
            "unit_price": 45.00,
            "quantity": 5,
            "storage_limit": 100,
            "comment": "Test comment",
        }

        await client.post("/api/inventory/lenses", json=product_data)
        await client.delete("/api/inventory/lenses/1")

        get_resp = await client.get("/api/inventory/lenses/all")

        assert get_resp.status_code == 200

        ret = get_resp.json()

        assert len(ret) == 1
        assert compare_returned_json(ret[0], product_data)
        assert ret[0]["deleted_at"] is not None
