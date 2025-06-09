from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.exceptions import NotFoundException
from src.models.users import UsersORM
from src.repositories.base import BaseRepository
from src.schemas.users import UsersSchema, UserWithHashedPasswordSchema


class UsersRepository(BaseRepository):
    model = UsersORM
    schema = UsersSchema

    async def get_user_with_hashed_password(self, email: EmailStr):
        # todo refactor - too much duplicate code with the base method get_one
        query = select(self.model).filter_by(email=email)
        try:
            result = await self.session.execute(query)
            model_object = result.scalars().one()
        except NoResultFound as err:
            raise NotFoundException(err)
        # todo this is the only difference with the base method get_one
        return UserWithHashedPasswordSchema.model_validate(model_object, from_attributes=True)
