from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, PaginationDep
from src.api.exceptions import only_one_error_handler
from src.schemas.facilities import (
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
    data = await db.facilities.get_many_filtered(
        limit=pagination.limit,
        offset=pagination.offset,
    )
    return data


@router.get("/{facility_id}")
@only_one_error_handler
async def get_facility(db: DBDep, facility_id: int) -> FacilitiesSchema:
    data = await db.facilities.get_one(id=facility_id)
    return data


@router.post("", status_code=201)
async def create_facility(db: DBDep, schema_create: FacilitiesWriteSchema):
    data = await db.facilities.add(schema_create)
    # transaction commit MUST stay here!
    await db.commit()
    return {"status": "Ok", "data": data}


@router.delete("/{facility_id}", status_code=204)
@only_one_error_handler
async def delete_facility(db: DBDep, facility_id: int):
    await db.facilities.delete(id=facility_id)
    await db.commit()
    return {"status": "Ok"}


@router.put("/{facility_id}", status_code=204)
@only_one_error_handler
async def update_facility(
    db: DBDep, facility_id: int, schema_update: FacilitiesWriteSchema
):
    await db.facilities.edit(schema_update, id=facility_id)
    await db.commit()
    return {"status": "Ok"}


@router.patch("/{facility_id}", status_code=204)
@only_one_error_handler
async def partial_update_facility(
    db: DBDep, facility_id: int, schema_patch: FacilitiesPatchSchema
):
    await db.facilities.edit(schema_patch, partial_update=True, id=facility_id)
    await db.commit()
    return {"status": "Ok"}
