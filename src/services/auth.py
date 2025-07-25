from datetime import datetime, timezone, timedelta

import jwt
from jwt.exceptions import DecodeError, InvalidSignatureError, ExpiredSignatureError
from passlib.context import CryptContext

from src.config import settings
from src.services.exceptions import InvalidPasswordException, InvalidTokenException
from src.services.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
