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
