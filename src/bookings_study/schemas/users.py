from pydantic import BaseModel, EmailStr


class UsersBaseSchema(BaseModel):
    username: str
    email: EmailStr


class UsersRegisterSchema(UsersBaseSchema):
    password: str


class UsersAddSchema(UsersBaseSchema):
    hashed_password: str


class UsersLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UsersSchema(UsersBaseSchema):
    id: int


class UserWithHashedPasswordSchema(UsersSchema):
    hashed_password: str
