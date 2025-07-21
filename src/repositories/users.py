from pydantic import EmailStr

from src.models.users import UsersOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import UsersDataMapper
from src.schemas.users import UserWithHashedPasswordSchema


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UsersDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        # override return mapper
        model_object = await self.get_one(orm_output=True, email=email)
        return UserWithHashedPasswordSchema.model_validate(
            model_object, from_attributes=True
        )
