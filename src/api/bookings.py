from fastapi import APIRouter

from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.api.dependencies import DBDep, UserIdDep

router = APIRouter(prefix="/bookings", tags=['Бронирования'])


@router.get("")
async def get_all_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me")
async def get_my_bookings(
        user_id: UserIdDep,
        db: DBDep,
):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("")
async def create_booking(
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingAddRequest
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price = room.price
    _booking_data = BookingAdd(
        user_id=user_id,
        price= room_price,
        **booking_data.model_dump()
    )

    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}