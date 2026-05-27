from fastapi import Query, APIRouter
from fastapi.params import Body

from sqlalchemy import insert, select, func

from src.models.hotels import HotelsORM
from src.database import async_session_maker
from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(default=None),
    location: str | None = Query(default=None),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsORM)
        if location:
            # query = query.filter(HotelsORM.location.ilike(f"%{location}%"))
            query = query.filter(func.lower(HotelsORM.location).like(f"%{location.lower()}%"))
        if title:
            # query = query.filter(HotelsORM.title.ilike(f"%{title}%"))
            query = query.filter(func.lower(HotelsORM.title).like(f"%{title.lower()}%"))
        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )
        result = await session.execute(query)

        hotels = result.scalars().all()

        return hotels


@router.post("")
async def create_hotel(hotel_data: Hotel):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsORM).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "OK"}


@router.put("/{hotel_id}")
def put_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name

    return {"status": "OK"}


@router.patch("/{hotel_id}")
def patch_hotel(hotel_id: int, hotel_data: HotelPATCH):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title:
                hotel["title"] = hotel_data.title
            if hotel_data.name:
                hotel["name"] = hotel_data.name

    return {"status": "OK"}


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}
