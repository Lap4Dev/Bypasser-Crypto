from aiocryptopay.const import Assets, PaidButtons
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, FSInputFile

from src.config import constants as c, settings, logger
from src.config import templates as t
from src.keyboards import inline
from src.loader import crypto_bot, security
from src.projects.hamster_combat.auto_claim import get_hamster_token
from src.repositories import SqlAlchemyProductRepository, SqlAlchemyHamsterClaimerRepository, \
    SqlAlchemyConfidentialRepository
from src.services.subscription_service import SubscriptionService
from src.utils.bot import create_media, send_error_media, create_invite_link

router = Router()


class ClaimerSettings(StatesGroup):
    waiting_token = State()


@router.callback_query(F.data == c.CD_AUTO_HMSTR_CLAIMER)
async def hamster_claimer_menu(query: CallbackQuery):
    media = create_media(settings.IMAGES_PATH / c.AUTO_CLAIMER_HAMSTER_IMAGE_NAME, t.HAMSTER_CLAIMER_DESCRIPTION)
    await query.message.edit_media(
        media=media,
        reply_markup=inline.get_hamster_auto_claimer_menu(c.HAMSTER_KOMBAT)
    )


async def payment_need(query: CallbackQuery, product_name: str, session):
    product_repo = SqlAlchemyProductRepository(session)

    product = await product_repo.get_by_name(product_name)
    if not product:
        return await send_error_media(query, caption=t.PRODUCT_NOT_FOUND)

    media = create_media(
        settings.IMAGES_PATH / c.PAYMENT_IMAGE_NAME,
        t.auto_claimer_payment_explanation(product.price_in_usd)
    )

    payment_payload = t.generate_payload(
        user_id=query.from_user.id,
        amount=product.price_in_usd,
        product_name=product.name,
    )
    try:
        invoice = await crypto_bot.create_invoice(
            asset=Assets.USDT,
            amount=product.price_in_usd,
            payload=payment_payload,
            expires_in=7200,
            paid_btn_name=PaidButtons.OPEN_BOT,
            paid_btn_url=settings.BOT_LINK,
        )

        if not (invoice.invoice_id and invoice.bot_invoice_url):
            raise Exception("invoice_id or bot_invoice_url not found")

    except Exception as ex:
        logger.warning(f'Error while creating invoice: {ex}')
        return await send_error_media(query, caption=t.PAYMENT_CREATION_ERROR)

    await query.message.edit_media(
        media=media,
        reply_markup=inline.get_purchase_subscription(
            subscription_price=product.price_in_usd,
            payment_url=invoice.bot_invoice_url,
            go_back=c.CD_AUTO_HMSTR_CLAIMER
        )
    )


@router.callback_query(F.data == c.CD_CLAIMER_MENU)
async def hamster_kombat_claimer_bot_menu(tg_object: CallbackQuery | Message, session, state: FSMContext = None):
    if state:
        await state.clear()

    user_id = tg_object.from_user.id
    sub_service = SubscriptionService(session)
    claimer_repo = SqlAlchemyHamsterClaimerRepository(session)

    subscription = await sub_service.get_subscription(user_id, c.PRODUCT_HAMSTER_KOMBAT_CLAIMER)
    if not subscription:
        return await send_error_media(tg_object, caption=t.SUBSCRIPTION_NOT_FOUND)

    caption = t.claimer_bot_menu(subscription)
    media = create_media(settings.IMAGES_PATH / c.HAMSTER_MENU_IMAGE_NAME, caption)
    hamster_claimer, _ = await claimer_repo.get_or_create(user_id)
    markup = inline.get_claimer_menu(
        is_claimer_run=hamster_claimer.is_active,
        is_empty_token=hamster_claimer.token_id is None,
        go_to=c.CD_AUTO_HMSTR_CLAIMER
    )

    if isinstance(tg_object, CallbackQuery):
        await tg_object.message.edit_media(
            media=media,
            reply_markup=markup
        )
    else:
        photo_file = FSInputFile(settings.IMAGES_PATH / c.HAMSTER_MENU_IMAGE_NAME)
        await tg_object.answer_photo(
            photo=photo_file,
            caption=caption,
            reply_markup=markup
        )


@router.callback_query(F.data == c.CD_RUN_CLAIMER)
@router.callback_query(F.data == c.CD_STOP_CLAIMER)
async def toggle_run(query: CallbackQuery, session):
    claimer_repo = SqlAlchemyHamsterClaimerRepository(session)

    need_run = True if query.data == c.CD_RUN_CLAIMER else False
    is_ok = await claimer_repo.set_active(query.from_user.id, is_active=need_run)

    if is_ok:
        await query.message.edit_reply_markup(
            reply_markup=inline.get_claimer_menu(
                is_claimer_run=need_run,
                is_empty_token=False,
                go_to=c.CD_AUTO_HMSTR_CLAIMER
            )
        )
    else:
        return await send_error_media(query, caption=t.TOGGLE_RUN_ERROR)


@router.callback_query(F.data == c.CD_CHANGE_TOKEN)
@router.callback_query(F.data == c.CD_SET_TOKEN)
async def set_hamster_token(query: CallbackQuery, state: FSMContext, bot):
    await state.set_state(ClaimerSettings.waiting_token)
    invite_link = await create_invite_link(bot, settings.INSTRUCTION_CHANNEL_ID)

    message = await query.message.edit_caption(
        caption=t.enter_token_from_instruction(invite_link),
        reply_markup=inline.cancel(c.CD_CLAIMER_MENU)
    )
    await state.update_data(previous_message_id=message.message_id)
    await query.answer()


@router.message(ClaimerSettings.waiting_token)
async def handle_token(message: Message, state: FSMContext, session, bot: Bot):
    user_id = message.from_user.id
    hashed_token = message.text
    decoded_token = security.decode_string(hashed_token)

    invite_link = await create_invite_link(bot, settings.INSTRUCTION_CHANNEL_ID)

    if 'hash' not in decoded_token:
        return await message.answer(t.seems_you_enter_invalid_token(invite_link))

    confidential_repo = SqlAlchemyConfidentialRepository(session)

    _ = await confidential_repo.find_or_create(
        user_id,
        c.NAME_HASHED_TOKEN,
        value=hashed_token
    )

    hamster_token = await get_hamster_token(decoded_token)

    if not hamster_token:
        return await message.answer(t.seems_you_enter_invalid_token(invite_link))

    confidential_data = await confidential_repo.create_or_update(
        user_id,
        c.NAME_HAMSTER_TOKEN,
        value=hamster_token
    )
    if not confidential_data:
        return await send_error_media(message, caption=t.SETTING_TOKEN_ERROR)

    claimer_repo = SqlAlchemyHamsterClaimerRepository(session)
    is_set = await claimer_repo.set_token_id(user_id=user_id, token_id=confidential_data.id)
    if not is_set:
        return await send_error_media(message, caption=t.SETTING_TOKEN_ERROR)

    data = await state.get_data()

    try:
        await bot.delete_message(chat_id=user_id, message_id=data.get('previous_message_id'))
    except:
        ...

    await hamster_kombat_claimer_bot_menu(message, session, state)
    return


@router.callback_query(F.data == c.CD_RUN_AUTO_BOT)
async def run_auto_bot(query: CallbackQuery, session):
    sub_service = SubscriptionService(session)
    is_subscribed = await sub_service.is_subscribe(query.from_user.id, product_name=c.PRODUCT_HAMSTER_KOMBAT_CLAIMER)
    if is_subscribed:
        await hamster_kombat_claimer_bot_menu(query, session)
        return
    # return await query.answer('На стадії розробки. Незабаром буде доступно!', show_alert=True)
    await payment_need(
        query,
        session=session,
        product_name=c.PRODUCT_HAMSTER_KOMBAT_CLAIMER
    )
