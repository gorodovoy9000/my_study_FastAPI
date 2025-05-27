from pydantic import BaseModel, EmailStr

from src.schemas.base import BasePatchSchema


class UserBaseSchema(BaseModel):
    username: str
    email: EmailStr


class UserWriteSchema(UserBaseSchema):
    pass


class UserPlainPasswordSchema(UserBaseSchema):
    password: str


class UserHashedPasswordSchema(UserBaseSchema):
    hashed_password: str


class UserPatchSchema(BasePatchSchema):
    username: str = None
    email: EmailStr = None


class UserSchema(UserBaseSchema):
    id: int
