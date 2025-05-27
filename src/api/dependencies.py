from typing import Annotated

from fastapi import Depends, Query, Path
from pydantic import BaseModel


async def id_path_param(hotel_id: int = Path(ge=1)) -> int:
    return hotel_id


IdDep = Annotated[int, Depends(id_path_param)]


class PaginationParams(BaseModel):
    page: Annotated[int, Query(ge=1)] = 1
    per_page: Annotated[int, Query(ge=1, le=100)] = 10

PaginationDep = Annotated[PaginationParams, Depends()]
