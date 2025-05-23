from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel

class PaginationParams(BaseModel):
    page: Annotated[int, Query(ge=1)] = 1
    per_page: Annotated[int, Query(ge=1, le=100)] = 10

PaginationDep = Annotated[PaginationParams, Depends()]
