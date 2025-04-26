import asyncio
from httpx import AsyncClient


test_data = [
    {
        "id": 1,
        "lens_type": "CR39",
        "sphere": -2.0,
        "cylinder": -0.75,
        "unit_price": 45.0,
        "storage_limit": 100,
        "quantity": 42,
    },
    {
        "id": 2,
        "lens_type": "Polycarbonate",
        "sphere": -1.25,
        "cylinder": 0.0,
        "unit_price": 55.0,
        "storage_limit": 80,
        "quantity": 15,
    },
    {
        "id": 3,
        "lens_type": "Trivex",
        "sphere": 0.0,
        "cylinder": -1.25,
        "unit_price": 60.0,
        "storage_limit": 60,
        "quantity": 10,
    },
    {
        "id": 4,
        "lens_type": "High Index 1.67",
        "sphere": -5.0,
        "cylinder": -0.5,
        "unit_price": 95.0,
        "storage_limit": 50,
        "quantity": 25,
    },
    {
        "id": 5,
        "lens_type": "High Index 1.74",
        "sphere": -6.5,
        "cylinder": -2.0,
        "unit_price": 120.0,
        "storage_limit": 30,
        "quantity": 5,
    },
    {
        "id": 6,
        "lens_type": "Trivex",
        "sphere": +1.75,
        "cylinder": -1.00,
        "unit_price": 75.00,
        "storage_limit": 100,
        "quantity": 15,
    },
    {
        "id": 7,
        "lens_type": "CR39",
        "sphere": 0.00,
        "cylinder": 0.00,
        "unit_price": 40.00,
        "storage_limit": 100,
        "quantity": 25,
    },
    {
        "id": 8,
        "lens_type": "Polycarbonate",
        "sphere": -6.00,
        "cylinder": -2.00,
        "unit_price": 70.00,
        "storage_limit": 100,
        "quantity": 27,
    },
    {
        "id": 9,
        "lens_type": "Trivex",
        "sphere": -3.50,
        "cylinder": -1.75,
        "unit_price": 80.00,
        "storage_limit": 25,
        "quantity": 10,
        "comment": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
    },
    {
        "id": 10,
        "lens_type": "Trivex",
        "sphere": +1.75,
        "cylinder": 2.00,
        "unit_price": 75.00,
        "storage_limit": 25,
        "quantity": 10,
    },
]


async def send_requests():
    async with AsyncClient() as client:
        for lens_data in test_data:
            await client.post(
                "http://localhost:8000/api/inventory/lenses", json=lens_data
            )


if __name__ == "__main__":
    asyncio.run(send_requests())
