from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel

class PaginationParams(BaseModel):
    page: Annotated[
        int,
        Query(
            description="Pagination page number",
            ge=1,
        )
    ] = 1
    per_page: Annotated[
        int,
        Query(
            description="Pagination items per page",
            ge=1,
            le=100,
        )
    ] = 3

PaginationDep = Annotated[PaginationParams, Depends()]
