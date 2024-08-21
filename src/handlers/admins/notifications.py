from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from src.config.constants import CMD_SEND_ALL, CD_CONFIRM_SENDING
from src.config.templates import notification_prepear
from src.keyboards.inline import mailing_confirm, get_close
from src.repositories import SqlAlchemyUserRepository

router = Router()


class Notification(StatesGroup):
    confirm = State()


@router.message(Command(CMD_SEND_ALL))
async def send_all(message: Message, state: FSMContext, session):
    user_repo = SqlAlchemyUserRepository(session)
    user_id = message.from_user.id
    if not await user_repo.is_admin(user_id):
        return

    text = message.text[len(CMD_SEND_ALL) + 1:]
    await message.answer(
        notification_prepear(text=text),
        reply_markup=mailing_confirm()
    )
    await state.set_state(Notification.confirm)
    await state.update_data(text=text)


@router.callback_query(Notification.confirm, F.data == CD_CONFIRM_SENDING)
async def confirm_sending(query: CallbackQuery, state: FSMContext, session, bot: Bot):
    user_repo = SqlAlchemyUserRepository(session)
    if not await user_repo.is_admin(query.from_user.id):
        await state.clear()
        return

    data = await state.get_data()
    text = data.get('text')
    if not text:
        return

    users = await user_repo.get_all_user_ids()
    successfully_sent = 0
    markup = get_close()

    for chat_id in users:
        try:
            await bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=markup
            )
            successfully_sent += 1
        except:
            ...

    await query.message.edit_text(
        f'Відправлено: <code>{successfully_sent}/{len(users)}!</code>'
    )
    await state.clear()
