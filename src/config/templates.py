import json

from src.config import settings
from src.database.models import Subscription
from src.utils.text import text_progress_bar

BOT_NAME = 'Bypasser'
START_COMMAND_DESCRIPTION = 'Почати взаємодію із ботом'
GUARD_SUBSCRIPTION_NEEDED_MESSAGE = '<b>👁 Для доступу до функціоналу бота необхідно підписатися на канали:</b>\n\n' \
                                    'Після підписки натисни на кнопку перевірити 🔄'
GUARD_CHECK_SUB = 'Ноу дружище, так не проканає. Жду підписки 🥷'
HANDLER_NOT_FOUND = 'Агоов, заблукав ? 👀'
INFO_MSG = '🗄 <b>Повна інформація:</b>'

PRODUCT_NOT_FOUND = '🔍 Продукт не знайдено!\n\n' \
                    'На жаль, я не зміг знайти такий продукт у нашій базі даних. 😔 Можливо, він більше не доступний або був вилучений з продажу.\n\n' \
                    'Якщо вам потрібна допомога, будь ласка, зверніться до нашої служби підтримки. Ми з радістю вам допоможемо! 🙌'

SUBSCRIPTION_NOT_FOUND = '🔍 Підписку не знайдено!\n\n' \
                         'На жаль, я не зміг знайти вашу підписку у нашій базі даних. 😔 Можливо, вона більше не доступна або якимось чином була видалена.\n\n' \
                         'Якщо вам потрібна допомога, будь ласка, зверніться до нашої служби підтримки. Ми з радістю вам допоможемо! 🙌'

PAYMENT_CREATION_ERROR = (
    '❗️ Помилка під час створення платежу\n\n'
    'На жаль, виникла проблема при генерації вашого платежу. 😔 Будь ласка, спробуйте ще раз.\n\n'
    'Якщо проблема повторюється, не вагайтесь звернутися до нашої служби підтримки. Ми з радістю допоможемо вам вирішити це питання! 🙌'
)

SETTING_TOKEN_ERROR = (
    '❗️ Помилка під час встановлення токену\n\n'
    'На жаль, виникла проблема при встановлені токену. 😔 Будь ласка, спробуйте ще раз.\n\n'
    'Якщо проблема повторюється, не вагайтесь звернутися до нашої служби підтримки. Ми з радістю допоможемо вам вирішити це питання! 🙌'
)

TOGGLE_RUN_ERROR = (
    '❗️ Помилка під час зміни стану бота\n\n'
    'На жаль, виникла проблема. Будь ласка, спробуйте ще раз.\n\n'
    'Якщо проблема повторюється, не вагайтесь звернутися до нашої служби підтримки. Ми з радістю допоможемо вам вирішити це питання! 🙌'
)

FIRST_MESSAGE_START = (
    f'Привіт! Я <b>{BOT_NAME}</b>, твій БРО у світі крипто автоматизації! 👁\n\n'
    f'Радий вітати тебе у нашому просторі, де технології та креативність поєднуються, створюючи безмежні можливості. 🚀\n\n'
    f'Тут ти зможеш в майбутьному отримати скрипти для автоматизації різних крипто проектів, таких як <b><a href="{settings.HAMSTER_REF_LINK}">Hamster Kombat</a>, <a href="{settings.GRASS_REF_LINK}">Grass</a>, <a href="{settings.MEMEFI_REF_LINK}">MemeFi</a>, <a href="{settings.BLUM_REF_LINK}">Blum</a> </b> та багато інших. 🔥\n\n' \
    f'<b>🎮 Що на тебе чекає?</b>\n'
    f'-- Інструменти для оптимізації твоєї роботи у світі криптовалют.\n'
    f'-- Ексклюзивні скрипти для автоматизації та покращення взаємодії з популярними проектами.\n\n'
    f'<b>А вже зараз</b> у тебе є можливість згенерувати секретні ключі для участі в іграх на платформі <b>Hamster Kombat</b>! 🔐\n\n'
    f'Натискай кнопку нижче, щоб отримати свої ключі та приєднатися до гри. Разом ми досягнемо нових висот у світі крипто! 🌐\n\n'
    f'Завжди на зв\'язку,\n'
    f'<b>{BOT_NAME}</b> 👁'
)

MESSAGE_START = f'Знову на зв\'язку, друже! 👋\n\n' \
                f'Що будемо робити цього разу? Скрипти, ключі, автоматизація — обирай! 🚀\n\n' \
                f'Твій крипто БРО 🥷,\n' \
                f'<b>{BOT_NAME}</b> 👁'

CHOOSE_HAMSTER_GAME = '<b>Вибери гру, яку хочеш 🦆кнуть в хомячелі: ⚡</b>️'
CODE_NOT_FOUND = 'Сорі дружище, коди закінчилися 🤯 Але незабаром вони з\'являться. Спробуй трішки пізніше 🥷'
HAMSTER_KOMBAT_MENU_MSG = (
    f'⚔️ <a href="{settings.HAMSTER_REF_LINK}">Hamster Kombat</a> ⚔️\n'
    f'🚀 <b>Візьми контроль над дропом!</b>\n'
    f'🔑 Генератор ключів та автоматизація - вижми максимум з кожної можливості! 💥'
)

HAMSTER_CLAIMER_DESCRIPTION = (
    f'🚀 <b>Авто бот</b> <a href="{settings.HAMSTER_REF_LINK}">Hamster Kombat</a>\n\n'
    f'💡 <i>Основний критерій дропу в хомяку - пасивний дохід</i>. Тому я вирішив автоматизувати цей процес, '
    f'щоб <u>вижати максимум</u> з цього проекту 💰🔥\n\n'
    f'🤖 Я, <b>{BOT_NAME}</b>, буду збирати твої монети кожні три години - 24/7, щоб ти не пропустив жодної можливості!\n\n'
    f'<b>Більше монет = більший пасивний дохід</b> 💵'
)


def enter_token_from_instruction(instruction_link: str) -> str:
    return f'<b>Відправте токен, який ви отримали згідно <a href="{instruction_link}">інструкції</a>:</b>'


def seems_you_enter_invalid_token(instruction_link: str) -> str:
    return (
        f'Здається ви ввели некоректний токен 🤷‍♂️ Дотримуйтесь <a href="{instruction_link}">інструкції</a> 📒\n\n'
        '<b>Якщо ви впевнені в коректності токену, спробуйте ще раз. Можливо це трапилося випадково 😳</b>'
    )


def auto_claimer_payment_explanation(price: float) -> str:
    return (
        f'🔒 <b>Доступ до автоматичного збору</b>\n\n'
        f'Через обмежені ресурси, автоматичний збір можливий лише за умови мінімальної оплати. '
        f'<b>Вартість доступу до бота на 3 тижні складає <u>всього {price:.1f}$</u>.</b> 💸\n\n'
        f'💻 Вам не потрібно, щоб ваш комп\'ютер був включений. Все буде працювати на моїх серверах! '
        f'Максимальна зручність та ефективність ✅\n\n'
        f'Твій, <b>{BOT_NAME}</b> 👁'
    )


def code_generated_msg(code: str, game_name: str, hamster_combat_link, keys_used: int, keys_limit) -> str:
    return f'🤝 Тримай код для: <a href="{hamster_combat_link}">{game_name}</a>\n' \
           f'🔋 <b>Ключів залишилося:</b> {keys_limit - keys_used}/{keys_limit}\n\n' \
           f'📊 <b>Прогрес використання:</b>\n' \
           f'{text_progress_bar(capacity=keys_limit, used=keys_used)}\n\n' \
           f'🔑 Ключ: <code>{code}</code>'


def referral_info_msg(ref_link: str, total_ref_count: int = 0, active_ref_count: int = 0) -> str:
    if total_ref_count == 0 or total_ref_count is None or active_ref_count is None:
        conversion = 0
    else:
        conversion = active_ref_count / total_ref_count * 100

    return f'<b>Пригласи друга, будь другом</b> 🫣\n' \
           f'<i>та отримай повний доступ до бота</i> 💠\n\n' \
           f'👨‍👨‍👦‍👦 <b>Всього запрошено:</b> <code>{total_ref_count}</code>\n' \
           f'🔋 <b>Активні реферали: <code>{active_ref_count}</code></b>\n' \
           f'♻️ <b>Конверсія:</b> <code>{conversion:.2f}%</code>\n\n' \
           f'📎 <b>Лінк:</b> {ref_link}'


def keys_limit_msg(ref_link: str, keys_used: int = 0, keys_limit: int = 0) -> str:
    limit_msg = "Друже, на сьогодні ти досяг ліміту генерації ключів для цієї гри.\n\n" \
        if keys_used >= keys_limit else ""

    return f'{limit_msg}' \
           f'🪫 <b>Ключів залишилося:</b> {keys_limit - keys_used}/{keys_limit}\n\n' \
           f'<b>Для того, щоб отримати більше ключів - запроси друга. Кожен друг = +2 ключа</b>\n\n' \
           f'📎<b>Посилання для друга:</b>\n{ref_link}'


def buy_subscription_btn_text(sub_price: int) -> str:
    return f'👉 Оформити підписку за {sub_price}$ ✅'


def generate_payload(user_id: int, amount: float, product_name: str) -> str:
    return json.dumps(dict(
        user_id=user_id,
        amount=amount,
        product_name=product_name
    ))


def subscription_successfully_activated(product_name: str, subscription: Subscription) -> str:
    return (
        f'🎉 Підписка на <b>{product_name}</b> успішно активована! ✅\n\n'
        f'📅 Дійсна до: <b>{subscription.end_date.strftime("%d.%m.%Y")}</b>\n\n'
        f'Дякуємо за довіру! 💪\n\n'
        f'👉 Натисни /start щоб продовжити взаємодію зі мною 🤖'
    )


def claimer_bot_menu(subscription: Subscription) -> str:
    return (
        f'🎉 Підписка активна! ✅\n'
        f'📅 Дійсна до: <b>{subscription.end_date.strftime("%d.%m.%Y")}</b>\n\n'
        f'👉 <b>Виберіть дію:</b>'
    )


def notification_prepear(text: str) -> str:
    return (
        f'<b>Буде виконана розсилка для всіх користувачів бота!</b>\n'
        f'<b>Текст розсилки:</b>\n\n'
        f'{text}'
    )
