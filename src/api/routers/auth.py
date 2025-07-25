from fastapi import APIRouter, HTTPException, Response
from passlib.context import CryptContext
from starlette import status

from src.repositories.exceptions import (
    NotFoundException,
    UniqueValueException,
)
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.users import UsersAddSchema, UsersLoginSchema, UsersRegisterSchema
from src.services.auth import AuthService
from src.services.exceptions import InvalidPasswordException

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login")
async def login_user(db: DBDep, schema_received: UsersLoginSchema, response: Response):
    # authorize user
    try:
        # check user exists
        user = await db.users.get_user_with_hashed_password(email=schema_received.email)
        # verify password
        AuthService().verify_password(schema_received.password, user.hashed_password)
    # unauthorized error
    except (NotFoundException, InvalidPasswordException):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email or password invalid!",
        )
    # set access token
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(user_id: UserIdDep, response: Response):
    response.delete_cookie("access_token")
    return {"status": "Ok"}


@router.post("/register", status_code=201)
async def register_user(db: DBDep, schema_received: UsersRegisterSchema):
    # build user to add schema
    schema_create = UsersAddSchema(
        username=schema_received.username,
        email=schema_received.email,
        hashed_password=AuthService().hash_password(schema_received.password),
    )
    # create user and do not return created user data
    try:
        await db.users.add(schema_create)
        await db.commit()
    # user already exist error
    except UniqueValueException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )
    return {"status": "Ok"}


@router.get("/me")
async def current_user(db: DBDep, user_id: UserIdDep):
    user = await db.users.get_one(id=user_id)
    return user
