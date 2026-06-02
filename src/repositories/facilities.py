from sqlalchemy import select, delete, insert

from src.repositories.mappers.mappers import FacilityDataMapper
from src.schemas.facilities import Facility, RoomFacility
from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.repositories.base import BaseRepository


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    mapper = FacilityDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesORM
    schema = RoomFacility

    async def set_room_facilities(self, room_id: int, facility_ids: list[int]):
        query = (
            select(RoomsFacilitiesORM.facility_id)
            .filter_by(room_id=room_id)
        )
        res = await self.session.execute(query)
        current_facilities_ids = res.scalars().all()

        ids_to_delete = list(set(current_facilities_ids) - set(facility_ids))
        ids_to_insert = list(set(facility_ids) - set(current_facilities_ids))

        if ids_to_insert:
            insert_m2m_facilities_stmt = (
                insert(RoomsFacilitiesORM)
                .values([{"room_id": room_id, "facility_id": facility_id} for facility_id in ids_to_insert])
            )
            await self.session.execute(insert_m2m_facilities_stmt)

        if ids_to_delete:
            delete_m2m_facilities_stmt = (
                delete(RoomsFacilitiesORM)
                .filter(
                    RoomsFacilitiesORM.room_id == room_id,
                    RoomsFacilitiesORM.facility_id.in_(ids_to_delete),
                )
            )
            await self.session.execute(delete_m2m_facilities_stmt)
