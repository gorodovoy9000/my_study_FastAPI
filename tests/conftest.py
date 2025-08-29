# ruff: noqa: E402
import json
from typing import AsyncGenerator
from unittest import mock

# mocks
mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

from httpx import AsyncClient, ASGITransport
import pytest

from bookings_study.api.v1.dependencies import get_db
from bookings_study.config import settings
from bookings_study.database import (
    Base,
    engine_null_pool,
    async_session_maker_null_pool,
)
from bookings_study.main import app
from bookings_study.schemas.facilities import FacilitiesWriteSchema
from bookings_study.schemas.hotels import HotelsWriteSchema
from bookings_study.schemas.rooms import RoomsWriteSchema
from bookings_study.utils.db_manager import DBManager


# DO NOT RUN TESTS IF APP MODE IS NOT "TEST"
@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


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
    with open("tests/mock_facilities.json", encoding="utf-8") as file:
        facilities_data = json.load(file)

    # set schemas
    hotels_schema = [HotelsWriteSchema.model_validate(obj) for obj in hotels_data]
    rooms_schema = [RoomsWriteSchema.model_validate(obj) for obj in rooms_data]
    facilities_schema = [
        FacilitiesWriteSchema.model_validate(obj) for obj in facilities_data
    ]

    # fill db
    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels_schema)
        await db_.rooms.add_bulk(rooms_schema)
        await db_.facilities.add_bulk(facilities_schema)
        await db_.commit()


@pytest.fixture(scope="session", autouse=True)
async def setup_users(setup_database, ac):
    with open("tests/mock_users.json") as fo:
        data = json.load(fo)
    for obj in data:
        response = await ac.post("/api/v1/auth/register", json=obj)
        assert response.is_success


# callable fixtures
@pytest.fixture()
async def db() -> AsyncGenerator[DBManager, None]:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        base_url="http://test", transport=ASGITransport(app=app)
    ) as ac:
        yield ac


@pytest.fixture(scope="session")
async def authenticated_ac(setup_users, ac):
    data = {"email": "vasya@test.com", "password": "password2"}
    response = await ac.post("/api/v1/auth/login", json=data)
    assert response.is_success
    assert ac.cookies["access_token"]
    yield ac
