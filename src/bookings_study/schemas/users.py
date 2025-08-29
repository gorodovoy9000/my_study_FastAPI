from typing import Annotated

from pydantic import AfterValidator, BaseModel, EmailStr


def is_password_correct(value: str) -> str:
    if len(value) < 8:
        raise ValueError("Password must be at least 8 characters long")
    return value


class UsersBaseSchema(BaseModel):
    email: EmailStr


class UsersRegisterSchema(UsersBaseSchema):
    password: Annotated[str, AfterValidator(is_password_correct)]


class UsersAddSchema(UsersBaseSchema):
    hashed_password: str


class UsersLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UsersSchema(UsersBaseSchema):
    id: int


class UserWithHashedPasswordSchema(UsersSchema):
    hashed_password: str
