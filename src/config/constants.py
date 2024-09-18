# Основные команды
CMD_START = 'start'
CMD_SEND_ALL = 'send_all'

# Кнопки меню
CHECK_SUBSCRIPTION = 'Перевірити підписку 🔄'
HAMSTER_KOMBAT = 'Hamster Kombat 🐹'
HAMSTER_KEY = 'Отримати Hamster ключі 🐹🔑'
AUTO_HAMSTER_CLAIMER = 'АВТО БОТ Hamster Kombat 💰'
MENU = 'Меню 🎮'
INFO = 'Інфо 📚'
SUPPORT = '☎️ Підтримка'
OFFICIAL_CHANNEL = '✅ Офіційний канал'
OFFICIAL_CHAT = '💬 Офіційний чат'
RUN_AUTO_BOT = 'Запустить авто бот 🤖'
GO_BACK = '🔙 Назад'
REFERRAL_PROGRAM = 'Реферальна програма 🫂'
RUN_CLAIMER = '🚀 Запустити авто збір'
STOP_CLAIMER = '💢 Зупинити авто збір '
CLAIMER_SETTINGS = '⛓ Налаштування'
SET_TOKEN = '💻 Встановити токен'
CHANGE_TOKEN = '♻️ Змінити токен'
CANCEL = '💢 Скасувати'
CLOSE = '💢 Закрити'
CONFIRM_SENDING = '✅ Відправити розсилку'
AGENT301_PROJECT = 'Новий проект від Дурова 💰🔥'

# Коды действий
CD_AUTO_HMSTR_CLAIMER = 'hmstr-claimer'
CD_RUN_AUTO_BOT = 'run-auto-bot'
CD_HAMSTER_KEY = 'hmstr-keys'
CD_MAIN_MENU = 'main-menu'
CD_REFF_PROG = 'ref-prog'
CD_RUN_CLAIMER = 'run-claimer'
CD_STOP_CLAIMER = 'stop-claimer'
CD_CLAIMER_SETTINGS = 'settings-claimer'
CD_SET_TOKEN = 'set-hamster-token'
CD_CHANGE_TOKEN = 'change-hamster-token'
CD_CLAIMER_MENU = 'claimer-menu'
CD_CONFIRM_SENDING = 'confirm-sending'
CD_CANCEL = 'cancel'
CD_CLOSE = 'close'

# Изображения
HAMSTER_IMAGE_NAME = 'hamster.webp'
WELCOME_IMAGE_NAME = 'welcome.webp'
START_IMAGE_NAME = 'hello.webp'
GUARD_IMAGE_NAME = 'guard.webp'
CLONE_ARMY_IMAGE_NAME = 'clone_army.webp'
CUBE_IMAGE_NAME = '2048.jpg'
PAYMENT_IMAGE_NAME = 'payment.jpg'
RIDING_EXTREME_IMAGE_NAME = 'riding_extreme.webp'
MINER_IMAGE_NAME = 'miner.webp'
INFO_IMAGE_NAME = 'info.webp'
REFERRAL_PROGRAM_IMAGE_NAME = 'referral_program.webp'
ACCESS_CARD_IMAGE_NAME = 'access_card.webp'
AUTO_CLAIMER_HAMSTER_IMAGE_NAME = 'hamster_auto_claimer.webp'
HAMSTER_MENU_IMAGE_NAME = 'menu_hamster.webp'
ERROR_IMAGE_NAME = 'something_error.webp'

# Игры Hamster
HAMSTER_GAMES = [
    # (1, 'Riding Extreme 3D', RIDING_EXTREME_IMAGE_NAME),
    (2, 'Chain Cube 2048', CUBE_IMAGE_NAME),
    # (3, 'My Clone Army', CLONE_ARMY_IMAGE_NAME),
    (4, 'Train Miner', MINER_IMAGE_NAME),
    (5, 'Merge Away', HAMSTER_IMAGE_NAME),
    (6, 'Twerk Race', HAMSTER_IMAGE_NAME),
    (7, 'Polysphere', HAMSTER_IMAGE_NAME),
    (8, 'Mow And Trim', HAMSTER_IMAGE_NAME),
    # (9, 'Mud Racing', HAMSTER_IMAGE_NAME),
    # (10, 'Cafe Dash', HAMSTER_IMAGE_NAME),
    # (11, 'Gangs Wars', HAMSTER_IMAGE_NAME),
    (12, 'Zoopolis', HAMSTER_IMAGE_NAME),
    (13, 'Tile Trio', HAMSTER_IMAGE_NAME),
    (14, 'Fluff Crusade', HAMSTER_IMAGE_NAME),
    (15, 'Stone Age', HAMSTER_IMAGE_NAME),
    (16, 'Bouncemasters', HAMSTER_IMAGE_NAME),
    (17, 'Hide Ball', HAMSTER_IMAGE_NAME),
    (18, 'Pin Out Master', HAMSTER_IMAGE_NAME),
    (19, 'Count Masters', HAMSTER_IMAGE_NAME),
]

# Статистика использования ключей (Key Usage Statistics)
# HAMSTER_RIDING_KEYS_USED = 'hamster_riding_keys_used'
HAMSTER_CUBE_KEYS_USED = 'hamster_cube_keys_used'
# HAMSTER_CLONE_KEYS_USED = 'hamster_clone_keys_used'
HAMSTER_MINER_KEYS_USED = 'hamster_miner_keys_used'
HAMSTER_MERGE_AWAY_KEYS_USED = 'hamster_merge_away_keys_used'
HAMSTER_TWERK_RACE_KEYS_USED = 'hamster_twerk_race_keys_used'
HAMSTER_POLYSPHERE_KEYS_USED = 'hamster_polysphere_keys_used'
HAMSTER_MOW_AND_TRIM_KEYS_USED = 'hamster_mow_and_trim_keys_used'
# HAMSTER_MUD_RACING_KEYS_USED = 'hamster_mud_racing_keys_used'
# HAMSTER_CAFE_DASH_KEYS_USED = 'hamster_cafe_dash_keys_used'
# HAMSTER_GANGS_WARS_KEYS_USED = 'hamster_gangs_wars_keys_used'
HAMSTER_ZOOPOLIS_KEYS_USED = 'hamster_zoopolis_keys_used'
HAMSTER_TILE_TRIO_KEYS_USED = 'hamster_tile_trio_keys_used'
HAMSTER_FLUFF_CRUSADE_KEYS_USED = 'hamster_fluff_crusade_keys_used'
HAMSTER_STONE_AGE_KEYS_USED = 'hamster_stone_age_keys_used'
HAMSTER_BOUNCEMASTER_KEYS_USED = 'hamster_bouncemaster_keys_used'
HAMSTER_HIDE_BALL_KEYS_USED = 'hamster_hide_ball_keys_used'
HAMSTER_PIN_OUT_MASTER_KEYS_USED = 'hamster_pin_out_keys_used'
HAMSTER_COUNT_MASTERS_KEYS_USED = 'hamster_count_masters_keys_used'

# Статистика использования игр
DB_STATISTIC_HAMSTER_GAMES = {
    # 1: HAMSTER_RIDING_KEYS_USED,
    2: HAMSTER_CUBE_KEYS_USED,
    # 3: HAMSTER_CLONE_KEYS_USED,
    4: HAMSTER_MINER_KEYS_USED,
    5: HAMSTER_MERGE_AWAY_KEYS_USED,
    6: HAMSTER_TWERK_RACE_KEYS_USED,
    7: HAMSTER_POLYSPHERE_KEYS_USED,
    8: HAMSTER_MOW_AND_TRIM_KEYS_USED,
    # 9: HAMSTER_MUD_RACING_KEYS_USED,
    # 10: HAMSTER_CAFE_DASH_KEYS_USED,
    # 11: HAMSTER_GANGS_WARS_KEYS_USED,
    12: HAMSTER_ZOOPOLIS_KEYS_USED,
    13: HAMSTER_TILE_TRIO_KEYS_USED,
    14: HAMSTER_FLUFF_CRUSADE_KEYS_USED,
    15: HAMSTER_STONE_AGE_KEYS_USED,
    16: HAMSTER_BOUNCEMASTER_KEYS_USED,
    17: HAMSTER_HIDE_BALL_KEYS_USED,
    18: HAMSTER_PIN_OUT_MASTER_KEYS_USED,
    19: HAMSTER_COUNT_MASTERS_KEYS_USED
}

# Название продуктов (Product name)
PRODUCT_HAMSTER_KOMBAT_CLAIMER = 'Авто БОТ Hamster Kombat'

# Confidential data names
NAME_HASHED_TOKEN = 'hashed_token'
NAME_HAMSTER_TOKEN = 'hamster_token'

NOTIFICATION_BTN_LINK = 'button_link='
