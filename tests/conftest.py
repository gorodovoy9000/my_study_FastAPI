from httpx import AsyncClient, ASGITransport
import pytest

from src.config import settings
from src.database import Base, engine_null_pool
from src.main import app
from src.models import *
from src.support_tables import *


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database):
    async with AsyncClient(base_url="http://test", transport=ASGITransport(app=app)) as ac:
        await ac.post(
            "/auth/register",
            json={
                "email": "test1@test.com",
                "password": "password"
            }
        )
