from datetime import date

from fastapi import Query, APIRouter

from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelAdd, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(default=None),
    location: str | None = Query(default=None),
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10"),
):
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to
    )


@router.get("/{hotel_id}")
async def get_hotel(db: DBDep, hotel_id: int):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post("")
async def create_hotel(db: DBDep, hotel_data: HotelAdd):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def put_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}")
async def patch_hotel(db: DBDep, hotel_id: int, hotel_data: HotelPATCH):
    await db.hotels.edit(hotel_data, is_patch=True, id=hotel_id)
    await db.commit()

    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}
