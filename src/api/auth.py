from fastapi import APIRouter

from pwdlib import PasswordHash

from src.database import async_session_maker
from repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

password_hash = PasswordHash.recommended()


@router.post("/register")
async def register_user(
        data: UserRequestAdd,
):
    hashed_password = password_hash.hash(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "OK"}
