from datetime import date

from sqlalchemy import select, func

from src.models.bookings import BookingsORM
from src.models.rooms import RoomsORM

def rooms_ids_for_booking(
        date_from: date,
        date_to: date,
        hotel_id: int | None = None,
):
    rooms_cnt = (
        select(BookingsORM.room_id, func.count("*").label("rooms_booked"))
        .select_from(BookingsORM)
        .filter(
            BookingsORM.date_from <= date_to,
            BookingsORM.date_to >= date_from
        )
        .group_by(BookingsORM.room_id)
        .cte(name="rooms_cnt")
    )

    rooms_left_table = (
        select(
            RoomsORM.id.label("room_id"),
            (RoomsORM.quantity - func.coalesce(rooms_cnt.c.rooms_booked, 0)).label("rooms_left")
        )
        .select_from(RoomsORM)
        .outerjoin(rooms_cnt, RoomsORM.id == rooms_cnt.c.room_id)
        .cte(name="rooms_left_table")
    )

    get_rooms_ids_for_hotel = (
        select(RoomsORM.id)
        .select_from(RoomsORM)
    )
    if hotel_id is not None:
        get_rooms_ids_for_hotel = get_rooms_ids_for_hotel.filter_by(hotel_id=hotel_id)

    get_rooms_ids_for_hotel = get_rooms_ids_for_hotel.subquery()

    rooms_ids_get = (
        select(rooms_left_table.c.room_id)
        .select_from(rooms_left_table)
        .filter(
            rooms_left_table.c.rooms_left > 0,
            rooms_left_table.c.room_id.in_(get_rooms_ids_for_hotel)
        )
    )

    return rooms_ids_get