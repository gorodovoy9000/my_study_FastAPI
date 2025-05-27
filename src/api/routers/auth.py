from fastapi import APIRouter
from passlib.context import CryptContext

from src.api.exceptions import constrain_violation_error_handler
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserPlainPasswordSchema, UserHashedPasswordSchema

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", status_code=201)
@constrain_violation_error_handler
async def register_user(schema_received: UserPlainPasswordSchema):
    # hash password
    hashed_password = pwd_context.hash(schema_received.password)
    # build schema to write in db
    schema_create = UserHashedPasswordSchema(
        username=schema_received.username,
        email=schema_received.email,
        hashed_password=hashed_password,
    )
    # create user and do not return created user data
    async with async_session_maker() as session:
        await UsersRepository(session).add(schema_create)
        await session.commit()
    return {"status": "Ok"}
