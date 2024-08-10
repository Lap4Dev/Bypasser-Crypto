from src.config import settings
from src.utils.text import text_progress_bar

BOT_NAME = 'Bypasser'
START_COMMAND_DESCRIPTION = 'Почати взаємодію із ботом'
GUARD_SUBSCRIPTION_NEEDED_MESSAGE = '<b>👁 Для доступу до функціоналу бота необхідно підписатися на канали:</b>\n\n' \
                                    'Після підписки натисни на кнопку перевірити 🔄'
GUARD_CHECK_SUB = 'Ноу дружище, так не проканає. Жду підписки 🥷'
HANDLER_NOT_FOUND = 'Агоов, заблукав ? 👀'

FIRST_MESSAGE_START = f'Привіт! Я <b>{BOT_NAME}</b>, твій БРО у світі крипто автоматизації! 👁\n\n' \
                      f'Радий вітати тебе у нашому просторі, де технології та креативність поєднуються, створюючи безмежні можливості. 🚀\n\n' \
                      f'Тут ти зможеш в майбутьному отримати скрипти для автоматизації різних крипто проектів, таких як <b><a href="{settings.HAMSTER_REF_LINK}">Hamster Combat</a>, <a href="{settings.GRASS_REF_LINK}">Grass</a>, <a href="{settings.MEMEFI_REF_LINK}">MemeFi</a>, <a href="{settings.BLUM_REF_LINK}">Blum</a> </b> та багато інших. 🔥\n\n' \
                      f'<b>🎮 Що на тебе чекає?</b>\n' \
                      f'-- Інструменти для оптимізації твоєї роботи у світі криптовалют.\n' \
                      f'-- Ексклюзивні скрипти для автоматизації та покращення взаємодії з популярними проектами.\n\n' \
                      f'<b>А вже зараз</b> у тебе є можливість згенерувати секретні ключі для участі в іграх на платформі <b>Hamster Combat</b>! 🔐\n\n' \
                      f'Натискай кнопку нижче, щоб отримати свої ключі та приєднатися до гри. Разом ми досягнемо нових висот у світі крипто! 🌐\n\n' \
                      f'Завжди на зв\'язку,\n' \
                      f'<b>{BOT_NAME}</b> 👁'

MESSAGE_START = f'Знову на зв\'язку, друже! 👋\n\n' \
                f'Що будемо робити цього разу? Скрипти, ключі, автоматизація — обирай! 🚀\n\n' \
                f'Твій крипто БРО 🥷,\n' \
                f'<b>{BOT_NAME}</b> 👁'

CHOOSE_HAMSTER_GAME = '<b>Вибери гру, яку хочеш 🦆кнуть в хомячелі: ⚡</b>️'
CODE_NOT_FOUND = 'Сорі дружище, коди закінчилися 🤯 Але незабаром вони з\'являться. Спробуй трішки пізніше 🥷'


def code_generated_msg(code: str, game_name: str, hamster_combat_link, keys_used: int, keys_limit) -> str:
    return f'🤝 Тримай код для: <a href="{hamster_combat_link}">{game_name}</a>\n' \
           f'🔋 <b>Ключів залишилося:</b> {keys_limit-keys_used}/{keys_limit}\n\n' \
           f'📊 <b>Прогрес використання:</b>\n' \
           f'{text_progress_bar(capacity=keys_limit, used=keys_used)}\n\n' \
           f'🔑 Ключ: <code>{code}</code>'


def referral_info_msg(ref_link: str, total_ref_count: int = 0, active_ref_count: int = 0) -> str:
    return f'<b>Пригласи друга, будь другом</b> 🫣\n' \
           f'<i>та отримай повний доступ до бота</i> 💠\n\n' \
           f'👨‍👨‍👦‍👦 <b>Всього запрошено:</b> <code>{total_ref_count}</code>\n' \
           f'🔋 <b>Активні реферали: <code>{active_ref_count}</code></b>\n' \
           f'♻️ <b>Конверсія:</b> <code>{(active_ref_count / total_ref_count)%.2}%</code>\n\n' \
           f'📎 <b>Лінк:</b> {ref_link}'


def keys_limit_msg(ref_link: str, keys_used: int = 0, keys_limit: int = 0) -> str:
    limit_msg = "Друже, на сьогодні ти досяг ліміту генерації ключів для цієї гри.\n\n" \
        if keys_used >= keys_limit else ""

    return f'{limit_msg}' \
           f'🪫 <b>Ключів залишилося:</b> {keys_limit-keys_used}/{keys_limit}\n\n' \
           f'<b>Для того, щоб отримати більше ключів - запроси друга. Кожен друг = +2 ключа</b>\n\n' \
           f'📎<b>Посилання для друга:</b>\n{ref_link}'

