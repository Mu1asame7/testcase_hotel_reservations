from datetime import date

from sqlalchemy import select, func

from src.models.bookings import BookingsORM
from src.schemas.rooms import Room
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsORM


class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = Room

    async def get_filtered_by_time(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date,
    ):
        """
        WITH rooms_cnt AS
        (SELECT bookings.room_id AS room_id, count('*') AS rooms_booked
        FROM bookings
        WHERE bookings.date_from <= '2024-08-10' AND bookings.date_to >= '2024-08-01' GROUP BY bookings.room_id),
        rooms_left_table AS
        (SELECT rooms.id AS room_id, rooms.quantity - coalesce(rooms_cnt.rooms_booked, 0) AS rooms_left
        FROM rooms LEFT OUTER JOIN rooms_cnt ON rooms.id = rooms_cnt.room_id)
        SELECT rooms_left_table.room_id, rooms_left_table.rooms_left
        FROM rooms_left_table
        WHERE rooms_left_table.rooms_left > 0 and room_id in (select id from rooms where hotel_id = 8);
        """

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
            .filter_by(hotel_id=hotel_id)
            .subquery()
        )

        rooms_ids_get = (
            select(rooms_left_table.c.room_id)
            .select_from(rooms_left_table)
            .filter(
                rooms_left_table.c.rooms_left > 0,
                rooms_left_table.c.room_id.in_(get_rooms_ids_for_hotel)
                # select id from rooms where hotel_id = 8
            )
        )

        return await self.get_filtered(RoomsORM.id.in_(rooms_ids_get))
