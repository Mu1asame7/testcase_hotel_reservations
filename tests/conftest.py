import pytest

from config import settings
from src.database import Base, engine_null_pool
from src.models import *


@pytest.fixture(scope="session", autouse=True)
async def async_main():
    assert settings.MODE == "TEST"

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all) # type: ignore
        await conn.run_sync(Base.metadata.create_all) # type: ignore