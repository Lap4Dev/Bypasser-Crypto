from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.enums import ChatType
from aiogram.types import Message, CallbackQuery

from src.config import logger


class LoggingMiddleware(BaseMiddleware):
    @staticmethod
    async def log_event(user_id, user_name, message, state_name: str, state: dict = None, log_name='msg'):
        text = f"{user_id} - {user_name} - {log_name}({message})"
        if state:
            text += f' - {state_name}({state})'
        logger.info(text)

    async def __call__(
            self,
            handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:

        chat_type = event.message.chat.type if isinstance(event, CallbackQuery) else event.chat.type
        if chat_type != ChatType.PRIVATE:
            return

        user = event.from_user
        state = data.get('state')
        state_data = await state.get_data() if state else None

        if isinstance(event, Message):
            await self.log_event(
                user.id, user.username, event.text,
                state_name=await state.get_state(),
                state=state_data, log_name='msg'
            )

        if isinstance(event, CallbackQuery):
            await self.log_event(user.id, user.username, event.data,
                                 state_name=await state.get_state(),
                                 state=state_data, log_name='callback')

        return await handler(event, data)
