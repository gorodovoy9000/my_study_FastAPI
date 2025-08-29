from datetime import datetime, timezone, timedelta

import jwt
from jwt.exceptions import DecodeError, InvalidSignatureError, ExpiredSignatureError
from passlib.context import CryptContext

from bookings_study.config import settings
from bookings_study.repositories.exceptions import (
    NotFoundException,
    UniqueValueException,
)
from bookings_study.schemas.users import (
    UsersAddSchema,
    UsersLoginSchema,
    UsersRegisterSchema,
)
from bookings_study.services.base import BaseService
from bookings_study.services.exceptions import (
    InvalidPasswordException,
    InvalidTokenException,
    UserAlreadyExistsException,
    UserLoginFailedException,
    UserNotFoundException,
)


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def get_user(self, user_id: int):
        try:
            user = await self.db.users.get_one(id=user_id)
        except NotFoundException as err:
            raise UserNotFoundException from err
        return user

    async def register_user(self, data_register: UsersRegisterSchema):
        # build user to add schema
        schema_create = UsersAddSchema(
            email=data_register.email,
            hashed_password=self.hash_password(data_register.password),
        )
        # create user and do not return created user data
        try:
            await self.db.users.add(schema_create)
        # user already exist error
        except UniqueValueException as err:
            raise UserAlreadyExistsException from err
        await self.db.commit()

    async def login_user(self, data_login: UsersLoginSchema):
        # authorize user
        try:
            # check user exists
            user = await self.db.users.get_user_with_hashed_password(
                email=data_login.email
            )
            # verify password
            self.verify_password(data_login.password, user.hashed_password)
        # unauthorized error
        except (NotFoundException, InvalidPasswordException) as err:
            raise UserLoginFailedException from err
        # set access token
        access_token = self.create_access_token({"user_id": user.id})
        return access_token

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def decode_access_token(self, encoded_jwt: str) -> dict:
        try:
            return jwt.decode(
                encoded_jwt,
                settings.JWT_SECRET_KEY,
                algorithms=(settings.JWT_ALGORITHM,),
            )
        except (DecodeError, InvalidSignatureError, ExpiredSignatureError):
            raise InvalidTokenException()

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str):
        if not self.pwd_context.verify(plain_password, hashed_password):
            raise InvalidPasswordException()
