from sqlalchemy import select

from src.schemas.rooms import Room
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsORM


class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = Room