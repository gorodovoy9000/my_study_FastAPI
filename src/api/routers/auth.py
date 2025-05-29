from fastapi import APIRouter, HTTPException, Response
from passlib.context import CryptContext
from starlette import status

from src.database import async_session_maker
from src.exceptions import NotFoundException, UniqueValueException, InvalidPasswordException
from src.api.dependencies import UserIdDep
from src.repositories.users import UsersRepository
from src.schemas.users import UserAddSchema, UserLoginSchema, UserRegisterSchema
from src.service.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login")
async def login_user(schema_received: UserLoginSchema, response: Response):
    async with async_session_maker() as session:
        # authorize user
        try:
            # check user exists
            user = await UsersRepository(session).get_user_with_hashed_password(email=schema_received.email)
            # verify password
            AuthService().verify_password(schema_received.password, user.hashed_password)
        # unauthorized error
        except (NotFoundException, InvalidPasswordException):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email or password invalid!")
        # set access token
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}


@router.post("/register", status_code=201)
async def register_user(schema_received: UserRegisterSchema):
    # build user to add schema
    schema_create = UserAddSchema(
        username=schema_received.username,
        email=schema_received.email,
        hashed_password=AuthService().hash_password(schema_received.password),
    )
    # create user and do not return created user data
    try:
        async with async_session_maker() as session:
            await UsersRepository(session).add(schema_create)
            await session.commit()
    # user already exist error
    except UniqueValueException:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User with this email already exists",
        )
    return {"status": "Ok"}


@router.get("/me")
async def current_user(user_id: UserIdDep):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one(id=user_id)
    return user
