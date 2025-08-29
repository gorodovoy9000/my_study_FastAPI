from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from bookings_study.api.dependencies import DBDep, PaginationDep
from bookings_study.api.examples import facilities_examples
from bookings_study.api.exceptions import (
    FacilityAlreadyExistsHTTPException,
    FacilityNotFoundHTTPException
)
from bookings_study.services.facilities import FacilityService
from bookings_study.services.exceptions import (
    FacilityAlreadyExistsException,
    FacilityNotFoundException
)
from bookings_study.schemas.base import BaseResponseSchema
from bookings_study.schemas.facilities import (
    FacilitiesPatchSchema,
    FacilitiesResponseSchema,
    FacilitiesWriteSchema,
)

router = APIRouter(prefix="/facilities", tags=["facilities"])


@router.get("", description="Get all facilities")
@cache(expire=5)
async def get_facilities(
    db: DBDep, pagination: PaginationDep
) -> FacilitiesResponseSchema:
    data = await FacilityService(db).get_facilities_all(
        limit=pagination.limit,
        offset=pagination.offset,
    )
    return FacilitiesResponseSchema(data=data)


@router.get("/{facility_id}")
async def get_facility(db: DBDep, facility_id: int) -> FacilitiesResponseSchema:
    try:
        data = await FacilityService(db).get_facility(facility_id=facility_id)
    except FacilityNotFoundException:
        raise FacilityNotFoundHTTPException
    return FacilitiesResponseSchema(data=[data])


@router.post("")
async def create_facility(db: DBDep, data_create: FacilitiesWriteSchema = Body(openapi_examples=facilities_examples)) -> FacilitiesResponseSchema:
    try:
        data = await FacilityService(db).add_facility(data_create)
    except FacilityAlreadyExistsException:
        raise FacilityAlreadyExistsHTTPException
    return FacilitiesResponseSchema(data=[data])


@router.delete("/{facility_id}")
async def delete_facility(db: DBDep, facility_id: int) -> BaseResponseSchema:
    try:
        await FacilityService(db).delete_facility(facility_id=facility_id)
    except FacilityNotFoundException:
        raise FacilityNotFoundHTTPException
    return BaseResponseSchema()


@router.put("/{facility_id}")
async def update_facility(
    db: DBDep, facility_id: int, data_update: FacilitiesWriteSchema = Body(openapi_examples=facilities_examples)
) -> BaseResponseSchema:
    try:
        await FacilityService(db).edit_facility(
            facility_id=facility_id, data_update=data_update
        )
    except FacilityNotFoundException:
        raise FacilityNotFoundHTTPException
    except FacilityAlreadyExistsException:
        raise FacilityAlreadyExistsHTTPException
    return BaseResponseSchema()


@router.patch("/{facility_id}")
async def partial_update_facility(
    db: DBDep, facility_id: int, data_update: FacilitiesPatchSchema = Body(openapi_examples=facilities_examples)
) -> BaseResponseSchema:
    try:
        await FacilityService(db).edit_facility_partially(
            facility_id=facility_id, data_update=data_update
        )
    except FacilityNotFoundException:
        raise FacilityNotFoundHTTPException
    except FacilityAlreadyExistsException:
        raise FacilityAlreadyExistsHTTPException
    return BaseResponseSchema()
