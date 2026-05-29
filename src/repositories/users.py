from src.schemas.users import User
from src.models.users import UsersORM
from src.repositories.base import BaseRepository


class UsersRepository(BaseRepository):
    model = UsersORM
    schema = User