from pydantic import EmailStr

from bookings_study.models.users import UsersOrm
from bookings_study.repositories.base import BaseRepository
from bookings_study.repositories.mappers.mappers import UsersDataMapper
from bookings_study.schemas.users import UserWithHashedPasswordSchema


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UsersDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        # override return mapper
        model_object = await self.get_one(orm_output=True, email=email)
        return UserWithHashedPasswordSchema.model_validate(
            model_object, from_attributes=True
        )
