from domain.service.user import UserService
from fastapi import APIRouter

user_router = APIRouter()


@user_router.post(path="")
async def create_user():
    await UserService().create_user()
