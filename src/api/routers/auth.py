from fastapi import APIRouter, HTTPException, Response
from starlette import status

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.users import UsersLoginSchema, UsersRegisterSchema
from src.services.auth import AuthService
from src.services.exceptions import (
    UserAlreadyExistsException,
    UserLoginFailedException,
    UserNotFoundException,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login_user(db: DBDep, data_login: UsersLoginSchema, response: Response):
    try:
        access_token = await AuthService(db).login_user(data_login)
    except UserLoginFailedException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login failed! Email or password invalid.",
        )
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(user_id: UserIdDep, response: Response):
    response.delete_cookie("access_token")
    return {"status": "Ok"}


@router.post("/register", status_code=201)
async def register_user(db: DBDep, data_register: UsersRegisterSchema):
    try:
        await AuthService(db).register_user(data_register)
    except UserAlreadyExistsException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )
    return {"status": "Ok"}


@router.get("/me")
async def current_user(db: DBDep, user_id: UserIdDep):
    try:
        user = await AuthService(db).get_user(user_id)
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user
