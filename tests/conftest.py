import json
from typing import AsyncGenerator

from httpx import AsyncClient, ASGITransport
import pytest

from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models import *
from src.support_tables import *
from src.schemas.hotels import HotelsWriteSchema
from src.schemas.rooms import RoomsWriteSchema
from src.utils.db_manager import DBManager


# DO NOT RUN TESTS IF APP MODE IS NOT "TEST"
@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


# callable fixtures
@pytest.fixture()
async def db() -> AsyncGenerator[DBManager, None]:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(base_url="http://test", transport=ASGITransport(app=app)) as ac:
        yield ac


# auto start fixtures
@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    # clean db and create tables
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # get mock data
    with open("tests/mock_hotels.json", encoding="utf-8") as file:
        hotels_data = json.load(file)
    with open("tests/mock_rooms.json", encoding="utf-8") as file:
        rooms_data = json.load(file)

    # set schemas
    hotels_schema = [HotelsWriteSchema.model_validate(obj) for obj in hotels_data]
    rooms_schema = [RoomsWriteSchema.model_validate(obj) for obj in rooms_data]

    # fill db
    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels_schema)
        await db_.rooms.add_bulk(rooms_schema)
        await db_.commit()


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database, ac):
    with open("tests/mock_users.json") as fo:
        data = json.load(fo)
    for obj in data:
        await ac.post("/auth/register", json=obj)
