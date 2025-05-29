from typing import Annotated

from fastapi import Depends, Query, HTTPException, Path, Request, status
from pydantic import BaseModel

from src.exceptions import InvalidTokenException
from src.service.auth import AuthService


async def id_path_param(hotel_id: int = Path(ge=1)) -> int:
    return hotel_id


IdDep = Annotated[int, Depends(id_path_param)]


class PaginationParams(BaseModel):
    page: Annotated[int, Query(ge=1)] = 1
    per_page: Annotated[int, Query(ge=1, le=100)] = 10

PaginationDep = Annotated[PaginationParams, Depends()]


def get_valid_token(request: Request) -> dict:
    # get access token from cookies
    encoded_token = request.cookies.get("access_token")
    # token not found
    if not encoded_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not provided")
    # verify token
    try:
        decoded_data = AuthService().decode_access_token(encoded_token)
    # token invalid
    except InvalidTokenException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalid!")
    return decoded_data


def get_user_id(token: dict = Depends(get_valid_token)) -> int:
    user_id = token["user_id"]
    return user_id


UserIdDep = Annotated[int, Depends(get_user_id)]
