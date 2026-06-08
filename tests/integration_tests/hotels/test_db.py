import os

from config import settings
from database import async_session_maker
from schemas.hotels import HotelAdd
from utils.db_manager import DBManager


async def test_add_hotel():
    hotel_data = HotelAdd(title="Hotel 5 stars", location="New York")
    async with DBManager(session_factory=async_session_maker) as db:
        await db.hotels.add(hotel_data)
        await db.commit()
