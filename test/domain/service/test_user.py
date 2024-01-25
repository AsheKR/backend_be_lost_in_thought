from typing import Any

from unittest.mock import AsyncMock, patch
from uuid import uuid4

from assertpy import assert_that
from domain.repository.user import UserModel, UserRepository
from domain.service.user import UserService


async def test_find_first_by_external_id():
    user_model = UserModel(
        id=1,
        external_id=uuid4(),
    )
    with patch(
        "domain.repository.user.UserRepository.find_first_by_external_id", return_value=user_model
    ) as find_first_by_external_id:
        user_repository = UserRepository(session=Any)
        user_service = UserService(user_repository=user_repository)

        user_result = await user_service.find_first_by_external_id(external_id=user_model.external_id)
        find_first_by_external_id.assert_awaited_once_with(external_id=user_model.external_id)
        assert_that(user_result).is_not_none()


async def test_find_first_by_external_id_return_none_when_not_exist():
    with patch(
        "domain.repository.user.UserRepository.find_first_by_external_id", return_value=None
    ) as find_first_by_external_id:
        user_repository = UserRepository(session=Any)
        user_service = UserService(user_repository=user_repository)

        external_id = str(uuid4())
        user_result = await user_service.find_first_by_external_id(external_id=external_id)
        find_first_by_external_id.assert_awaited_once_with(external_id=external_id)
        assert_that(user_result).is_none()


async def test_register():
    user_model = UserModel(
        id=1,
        external_id=uuid4(),
    )
    with patch(
            "domain.repository.user.UserRepository.register", return_value=user_model,
    ) as register:
        user_repository = UserRepository(session=Any)
        user_service = UserService(user_repository=user_repository)

        external_id = await user_service.register()

        register.assert_awaited_once()
        assert_that(external_id).is_not_none()
