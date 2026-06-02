from src.schemas.hotels import Hotel
from src.models.hotels import HotelsORM
from src.repositories.mappers.base import DataMapper


class HotelDataMapper(DataMapper):
    db_model = HotelsORM
    schema = Hotel