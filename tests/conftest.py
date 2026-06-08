import pytest
from httpx import AsyncClient, ASGITransport

from config import settings
from src.main import app
from src.database import Base, engine_null_pool
from src.models import *


@pytest.fixture(scope="session", autouse=True)
def check_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all) # type: ignore
        await conn.run_sync(Base.metadata.create_all) # type: ignore


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database):
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as ac:
        await ac.post(
            "/auth/register",
            json={
                "email": "email@mail.ru",
                "password": "1234",
            }
        )
