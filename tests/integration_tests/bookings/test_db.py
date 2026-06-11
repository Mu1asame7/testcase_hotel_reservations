from datetime import date

from schemas.bookings import BookingAdd, BookingPatch


async def test_booking_crud(db):
    # create
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2026, month=6, day=10),
        date_to=date(year=2026, month=6, day=20),
        price=100,
    )
    new_booking = await db.bookings.add(booking_data)

    # read
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking is not None
    assert booking.user_id == user_id
    assert booking.room_id == room_id
    assert booking.date_from == date(year=2026, month=6, day=10)
    assert booking.date_to == date(year=2026, month=6, day=20)
    assert booking.price == 100

    # update
    booking_data_edit = BookingPatch(
        date_from=date(year=2026, month=6, day=11),
        date_to=date(year=2026, month=6, day=21)
    )
    await db.bookings.edit(
        booking_data_edit,
        is_patch=True,
        room_id=room_id,
        user_id=user_id,
    )
    updated_booking = await db.bookings.get_one_or_none(user_id=user_id, room_id=room_id)
    assert updated_booking is not None
    assert updated_booking.user_id == user_id
    assert updated_booking.room_id == room_id
    assert updated_booking.date_from == date(year=2026, month=6, day=11)
    assert updated_booking.date_to == date(year=2026, month=6, day=21)
    assert updated_booking.price == 100

    # delete
    await db.bookings.delete(user_id=user_id, room_id=room_id)
    await db.commit()