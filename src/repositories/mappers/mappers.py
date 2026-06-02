from src.schemas.facilities import Facility
from src.models.facilities import FacilitiesORM
from src.models.bookings import BookingsORM
from src.models.rooms import RoomsORM
from src.models.users import UsersORM
from src.schemas.bookings import Booking
from src.schemas.rooms import Room
from src.schemas.users import User
from src.schemas.hotels import Hotel
from src.models.hotels import HotelsORM
from src.repositories.mappers.base import DataMapper


class HotelDataMapper(DataMapper):
    db_model = HotelsORM
    schema = Hotel


class RoomDataMapper(DataMapper):
    db_model = RoomsORM
    schema = Room


class UserDataMapper(DataMapper):
    db_model = UsersORM
    schema = User


class BookingDataMapper(DataMapper):
    db_model = BookingsORM
    schema = Booking


class FacilityDataMapper(DataMapper):
    db_model = FacilitiesORM
    schema = Facility
