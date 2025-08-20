from fastapi import APIRouter
from fastapi_cache.decorator import cache

from bookings_study.api.dependencies import DBDep, PaginationDep
from bookings_study.api.exceptions import FacilityNotFoundHTTPException
from bookings_study.services.facilities import FacilityService
from bookings_study.services.exceptions import FacilityNotFoundException
from bookings_study.schemas.facilities import (
    FacilitiesSchema,
    FacilitiesPatchSchema,
    FacilitiesWriteSchema,
)

router = APIRouter(prefix="/facilities", tags=["facilities"])


@router.get("")
@cache(expire=5)
async def get_facilities(
    db: DBDep, pagination: PaginationDep
) -> list[FacilitiesSchema]:
    data = await FacilityService(db).get_facilities_all(
        limit=pagination.limit,
        offset=pagination.offset,
    )
    return data


@router.get("/{facility_id}")
async def get_facility(db: DBDep, facility_id: int) -> FacilitiesSchema:
    try:
        data = await FacilityService(db).get_facility(facility_id=facility_id)
    except FacilityNotFoundException:
        raise FacilityNotFoundHTTPException
    return data


@router.post("", status_code=201)
async def create_facility(db: DBDep, data_create: FacilitiesWriteSchema):
    data = await FacilityService(db).add_facility(data_create)
    return {"status": "Ok", "data": data}


@router.delete("/{facility_id}", status_code=204)
async def delete_facility(db: DBDep, facility_id: int):
    try:
        await FacilityService(db).delete_facility(facility_id=facility_id)
    except FacilityNotFoundException:
        raise FacilityNotFoundHTTPException
    return {"status": "Ok"}


@router.put("/{facility_id}", status_code=204)
async def update_facility(
    db: DBDep, facility_id: int, data_update: FacilitiesWriteSchema
):
    try:
        await FacilityService(db).edit_facility(
            facility_id=facility_id, data_update=data_update
        )
    except FacilityNotFoundException:
        raise FacilityNotFoundHTTPException
    return {"status": "Ok"}


@router.patch("/{facility_id}", status_code=204)
async def partial_update_facility(
    db: DBDep, facility_id: int, data_update: FacilitiesPatchSchema
):
    try:
        await FacilityService(db).edit_facility_partially(
            facility_id=facility_id, data_update=data_update
        )
    except FacilityNotFoundException:
        raise FacilityNotFoundHTTPException
    return {"status": "Ok"}
