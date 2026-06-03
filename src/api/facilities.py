import json

from fastapi import APIRouter

from src.init import redis_manager
from src.schemas.facilities import FacilityAdd
from src.api.dependencies import DBDep

router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("")
async def get_facilities(db: DBDep):
    facilities_from_cache = await redis_manager.get("facilities")
    if not facilities_from_cache:
        facilities =  await db.facilities.get_all()
        facilities_schemas = [f.model_dump() for f in facilities]
        facilities_json = json.dumps(facilities_schemas)
        await redis_manager.set("facilities", facilities_json)

        return facilities
    else:
        facilities_dicts = json.loads(facilities_from_cache)
        return facilities_dicts


@router.post("")
async def create_facility(db: DBDep, facility_data: FacilityAdd):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    return {"status": "OK", "facility": facility}
