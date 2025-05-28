from pydantic import BaseModel, EmailStr


class UserBaseSchema(BaseModel):
    username: str
    email: EmailStr


class UserRegisterSchema(UserBaseSchema):
    password: str


class UserAddSchema(UserBaseSchema):
    hashed_password: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserSchema(UserBaseSchema):
    id: int


class UserWithHashedPasswordSchema(UserSchema):
    hashed_password: str
