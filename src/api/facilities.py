import json

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.init import redis_manager
from src.schemas.facilities import FacilityAdd
from src.api.dependencies import DBDep

router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    print("Иду в БД")
    return await db.facilities.get_all()


@router.post("")
async def create_facility(db: DBDep, facility_data: FacilityAdd):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    return {"status": "OK", "facility": facility}
