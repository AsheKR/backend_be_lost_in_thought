from uuid import uuid4

from assertpy import assert_that
from domain.repository.user import UserModel, UserRepository
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session


async def test_find_first_by_external_id(session: async_scoped_session[AsyncSession]):
    user_repository = UserRepository(session=session)
    user_model = UserModel()
    session.add(instance=user_model)
    await session.flush()

    user_result = await user_repository.find_first_by_external_id(external_id=user_model.external_id)
    assert_that(user_result).is_not_none()


async def test_find_first_by_external_id_return_none_when_not_exist(session: async_scoped_session[AsyncSession]):
    user_repository = UserRepository(session=session)

    user_result = await user_repository.find_first_by_external_id(external_id=str(uuid4()))
    assert_that(user_result).is_none()


async def test_add(session: async_scoped_session[AsyncSession]):
    user_repository = UserRepository(session=session)
    user_model = UserModel()
    await user_repository.add(user=user_model)
    await session.flush()

    result = await session.scalar(select(UserModel).where(UserModel.external_id == user_model.external_id))

    assert_that(result).is_not_none()
