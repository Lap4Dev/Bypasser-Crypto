from typing import Any, Tuple

from sqlalchemy import select, update, func, case
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import TelegramUser
from .base import IUserRepository


class SqlAlchemyUserRepository(IUserRepository):
    model = TelegramUser

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get_or_create(self, user_id: int, username: str, first_name: str, last_name: str, referrer_id: int = None) \
            -> Tuple[TelegramUser, bool]:
        user_data = dict(
            user_id=user_id,
        )

        try:
            result = await self.session.execute(select(self.model).filter_by(**user_data))

            instance = result.scalars().first()

            if not instance:
                raise NoResultFound()

            was_created = False

            if (instance.username != username or
                    instance.first_name != first_name or
                    instance.last_name != last_name):
                instance.username = username
                instance.first_name = first_name
                instance.last_name = last_name

                await self.session.commit()

        except NoResultFound:
            user_data = dict(
                user_id=user_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                referrer_id=referrer_id
            )
            instance = self.model(**user_data)
            self.session.add(instance)
            await self.session.commit()
            was_created = True

        return instance, was_created

    async def get_field_value(self, user_id: int, field_name: str) -> Any:
        """
        Get the value of a specific field for a user with the given user_id.

        :param user_id: The ID of the user to retrieve the field value for.
        :param field_name: The name of the field to retrieve the value for (e.g., 'is_admin', 'is_banned').
        :return: The value of the specified field for the user.
        """
        user = await self.session.execute(
            select(getattr(self.model, field_name)).filter_by(chat_id=user_id)
        )
        return user.scalar_one_or_none()

    async def set_field_value(self, user_id: int, field_name: str, value: Any) -> None:
        """
        Set the value of a specific field for a user with the given user_id.

        :param user_id: The ID of the user to set the field value for.
        :param field_name: The name of the field to set the value for (e.g., 'is_admin', 'is_banned').
        :param value: The value to set for the specified field.
        """
        await self.session.execute(
            update(self.model).
            where(TelegramUser.user_id == user_id).
            values({field_name: value})
        )
        await self.session.commit()

    async def is_admin(self, user_id: int) -> bool:
        result = await self.get_field_value(user_id, 'is_admin')
        return result if result is not None else False

    async def is_banned(self, user_id: int) -> bool:
        result = await self.get_field_value(user_id, 'is_banned')
        return result if result is not None else False

    async def get_by_id(self, user_id: int) -> TelegramUser | None:
        result = await self.session.execute(select(self.model).filter_by(user_id=user_id))
        return result.scalar_one_or_none()

    async def get_referral_counts(self, user_id: int) -> Tuple[int, int]:
        result = await self.session.execute(
            select(
                func.count(self.model.user_id),
                func.sum(
                    case(
                        (self.model.is_verified.is_(True), 1),
                        else_=0
                    )
                )
            )
            .where(self.model.referrer_id == user_id)
        )

        total_referrals_count, active_referrals_count = result.first()

        return total_referrals_count, active_referrals_count

    async def verify_user(self, user_id: int) -> bool:

        result = await self.session.execute(
            select(self.model)
            .where(self.model.user_id == user_id)
        )
        user = result.scalar_one_or_none()

        if user is None:
            return False

        if not user.is_verified:
            user.is_verified = True
            await self.session.commit()
            return True
        else:
            return False

    async def get_all_verified(self) -> list[TelegramUser]:
        result = await self.session.execute(
            select(self.model)
            .where(self.model.is_verified.is_(True))
        )
        return list(result.scalars().all())
