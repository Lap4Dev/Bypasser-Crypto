import asyncio
import hashlib
import random
import string

import aiohttp
from datetime import datetime
from fake_useragent import UserAgent

from src.config import logger

user_agent = UserAgent()


class TokenGenerator:
    def __init__(self, init_data_raw: str):
        self.init_data_raw = init_data_raw

    @staticmethod
    def generate_random_fonts():
        fonts = [
            'Agency FB', 'Calibri', 'Century', 'Century Gothic', 'Franklin Gothic',
            'Haettenschweiler', 'Leelawadee', 'Lucida Bright', 'Lucida Sans',
            'MS Outlook', 'MS Reference Specialty', 'MS UI Gothic', 'MT Extra',
            'Marlett', 'Microsoft Uighur', 'Monotype Corsiva', 'Pristina', 'Segoe UI Light'
        ]
        random.shuffle(fonts)
        return fonts[:random.randint(5, len(fonts))]

    @staticmethod
    def generate_random_string(length=32):
        letters = string.ascii_lowercase + string.digits
        return ''.join(random.choice(letters) for i in range(length))

    @staticmethod
    def generate_random_duration(max_value=1000):
        return random.randint(0, max_value)

    @staticmethod
    def generate_random_value(min_value=0, max_value: float = 1):
        return random.uniform(min_value, max_value)

    @staticmethod
    def generate_random_priority():
        return f"u={random.randint(0, 1)}, i"

    @staticmethod
    def generate_random_sec_ch_ua_platform():
        platforms = ['"Windows"', '"macOS"', '"Linux"', '"Android"', '"iOS"']
        return random.choice(platforms)

    @classmethod
    def generate_fingerprint(cls):
        return {
            'version': '4.2.1',
            'visitorId': hashlib.md5(cls.generate_random_string().encode()).hexdigest(),
            'components': {
                'fonts': {
                    'value': cls.generate_random_fonts(),
                    'duration': cls.generate_random_duration(1000),
                },
                'domBlockers': {
                    'duration': cls.generate_random_duration(100),
                },
                'fontPreferences': {
                    'value': {
                        'default': cls.generate_random_value(100, 200),
                        'apple': cls.generate_random_value(100, 200),
                        'serif': cls.generate_random_value(100, 200),
                        'sans': cls.generate_random_value(100, 200),
                        'mono': cls.generate_random_value(100, 200),
                        'min': cls.generate_random_value(0, 50),
                        'system': cls.generate_random_value(100, 200),
                    },
                    'duration': cls.generate_random_duration(100),
                },
                'audio': {
                    'value': cls.generate_random_value(0, 0.001),
                    'duration': cls.generate_random_duration(100),
                },
                'screenFrame': {
                    'value': [0, 0, cls.generate_random_duration(50), 0],
                    'duration': cls.generate_random_duration(10),
                },
                'canvas': None,
                'osCpu': {
                    'duration': cls.generate_random_duration(100),
                },
                'languages': {
                    'value': [['en-US']],
                    'duration': cls.generate_random_duration(10),
                },
                'colorDepth': {
                    'value': 24,
                    'duration': cls.generate_random_duration(10),
                },
                'deviceMemory': {
                    'value': random.choice([4, 8, 16, 32]),
                    'duration': cls.generate_random_duration(10),
                },
                'screenResolution': {
                    'value': [1920, 1080],
                    'duration': cls.generate_random_duration(10),
                },
                'hardwareConcurrency': {
                    'value': random.choice([4, 8, 16]),
                    'duration': cls.generate_random_duration(10),
                },
                'timezone': {
                    'value': random.choice(['Europe/Kiev', 'Europe/Moscow', 'America/New_York']),
                    'duration': cls.generate_random_duration(20),
                },
                'sessionStorage': {
                    'value': random.choice([True, False]),
                    'duration': cls.generate_random_duration(10),
                },
                'localStorage': {
                    'value': random.choice([True, False]),
                    'duration': cls.generate_random_duration(10),
                },
                'indexedDB': {
                    'value': random.choice([True, False]),
                    'duration': cls.generate_random_duration(10),
                },
                'openDatabase': {
                    'value': random.choice([True, False]),
                    'duration': cls.generate_random_duration(10),
                },
                'cpuClass': {
                    'duration': cls.generate_random_duration(100),
                },
                'platform': {
                    'value': random.choice(['Win32', 'Linux x86_64']),
                    'duration': cls.generate_random_duration(10),
                },
                'plugins': {
                    'value': [
                        {
                            'name': random.choice(['PDF Viewer', 'Chrome PDF Viewer', 'WebKit built-in PDF']),
                            'description': 'Portable Document Format',
                            'mimeTypes': [
                                {
                                    'type': 'application/pdf',
                                    'suffixes': 'pdf',
                                },
                            ],
                        },
                    ],
                    'duration': cls.generate_random_duration(50),
                },
                'touchSupport': {
                    'value': {
                        'maxTouchPoints': random.choice([0, 1, 2, 5]),
                        'touchEvent': random.choice([True, False]),
                        'touchStart': random.choice([True, False]),
                    },
                    'duration': cls.generate_random_duration(10),
                },
                'vendor': {
                    'value': random.choice(['Google Inc.', 'Mozilla Foundation', 'Apple Inc.']),
                    'duration': cls.generate_random_duration(10),
                },
                'vendorFlavors': {
                    'value': ['chrome'],
                    'duration': cls.generate_random_duration(10),
                },
                'cookiesEnabled': {
                    'value': random.choice([True, False]),
                    'duration': cls.generate_random_duration(10),
                },
                'colorGamut': {
                    'value': random.choice(['srgb', 'p3', 'rec2020']),
                    'duration': cls.generate_random_duration(10),
                },
                'invertedColors': {
                    'duration': cls.generate_random_duration(10),
                },
                'forcedColors': {
                    'value': random.choice([True, False]),
                    'duration': cls.generate_random_duration(10),
                },
                'monochrome': {
                    'value': random.choice([0, 8]),
                    'duration': cls.generate_random_duration(10),
                },
                'contrast': {
                    'value': random.choice([0, 1]),
                    'duration': cls.generate_random_duration(10),
                },
                'reducedMotion': {
                    'value': random.choice([True, False]),
                    'duration': cls.generate_random_duration(10),
                },
                'reducedTransparency': {
                    'value': random.choice([True, False]),
                    'duration': cls.generate_random_duration(10),
                },
                'hdr': {
                    'value': random.choice([True, False]),
                    'duration': cls.generate_random_duration(10),
                },
                'math': {
                    'value': {
                        'acos': cls.generate_random_value(0, 2),
                        'acosh': cls.generate_random_value(0, 1000),
                        'asin': cls.generate_random_value(0, 1),
                        'asinh': cls.generate_random_value(0, 10),
                        'atanh': cls.generate_random_value(0, 1),
                        'atan': cls.generate_random_value(0, 1),
                        'sin': cls.generate_random_value(-1, 1),
                        'sinh': cls.generate_random_value(0, 10),
                        'cos': cls.generate_random_value(-1, 1),
                        'cosh': cls.generate_random_value(1, 2),
                        'tan': cls.generate_random_value(-2, 2),
                        'tanh': cls.generate_random_value(0, 1),
                        'exp': cls.generate_random_value(0, 10),
                        'expm1': cls.generate_random_value(0, 10),
                        'log1p': cls.generate_random_value(0, 10),
                        'powPI': cls.generate_random_value(0, 1e-50),
                    },
                    'duration': cls.generate_random_duration(10),
                },
                'pdfViewerEnabled': {
                    'value': random.choice([True, False]),
                    'duration': cls.generate_random_duration(10),
                },
                'architecture': {
                    'value': random.choice([255, 64, 128]),
                    'duration': cls.generate_random_duration(10),
                },
                'applePay': {
                    'value': random.choice([-1, 0, 1]),
                    'duration': cls.generate_random_duration(10),
                },
                'privateClickMeasurement': {
                    'duration': cls.generate_random_duration(10),
                },
                'webGlBasics': {
                    'value': {
                        'version': 'WebGL 1.0 (OpenGL ES 2.0 Chromium)',
                        'vendor': 'WebKit',
                        'vendorUnmasked': 'Google Inc. (Intel)',
                        'renderer': 'WebKit WebGL',
                        'rendererUnmasked': 'ANGLE (Intel, Intel(R) HD Graphics 630 (0x0000591B) Direct3D11 vs_5_0 ps_5_0, D3D11)',
                        'shadingLanguageVersion': 'WebGL GLSL ES 1.0 (OpenGL ES GLSL ES 1.0 Chromium)',
                    },
                    'duration': cls.generate_random_duration(20),
                },
                'webGlExtensions': None,
            },
        }

    @classmethod
    def generate_headers(cls) -> dict:
        headers = {
            'Accept': 'application/json',
            'Origin': "https://hamsterkombat.io",
            'Accept-Language': random.choice(['en-US,en;q=0.9', 'en-GB,en;q=0.8', 'en-CA,en;q=0.7']),
            'Content-Type': 'application/json',
            'Priority': cls.generate_random_priority(),
            'Sec-Ch-Ua-Mobile': random.choice(['?0', '?1']),
            'Sec-Ch-Ua-Platform': cls.generate_random_sec_ch_ua_platform(),
            'Sec-Fetch-Dest': random.choice(['empty', 'document', 'script']),
            'Sec-Fetch-Mode': random.choice(['cors', 'navigate', 'no-cors']),
            'Sec-Fetch-Site': random.choice(['same-site', 'cross-site', 'none']),
            'Sec-Gpc': str(random.randint(0, 1)),
            'User-Agent': user_agent.random,
        }
        return headers

    def generate_payload(self) -> dict:
        return {
            'initDataRaw': self.init_data_raw,
            'fingerprint': self.generate_fingerprint()
        }


async def get_hamster_token(init_data_raw: str) -> str | None:
    generator = TokenGenerator(init_data_raw)
    async with aiohttp.ClientSession() as session:
        headers = generator.generate_headers()
        json_data = generator.generate_payload()
        for i in range(5):
            try:
                response = await session.post(
                    'https://api.hamsterkombatgame.io/auth/auth-by-telegram-webapp',
                    headers=headers,
                    json=json_data
                )
                if response.ok:
                    result = await response.json()
                    return result.get('authToken', None)
            except Exception as ex:
                logger.error(f'Error while getting token [Attempt: {i + 1}]: {ex}')

            await asyncio.sleep(1)

    return None


class HamsterAccount:
    def __init__(self, token: str, session: aiohttp.ClientSession):
        self.token = token
        self.session = session
        self.url = "https://api.hamsterkombat.io/clicker/sync"
        self.headers = {
            "Host": "api.hamsterkombat.io",
            "Authorization": f"Bearer {self.token}",
            "Sec-Fetch-Site": "same-site",
            "Accept-Language": "ru",
            "Sec-Fetch-Mode": "cors",
            "Accept": "/",
            "Origin": "https://hamsterkombat.io",
            "Content-Length": "0",
            "User-Agent": user_agent.random,
            "Referer": "https://hamsterkombat.io/",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty"
        }

    async def claim(self):
        for i in range(5):
            try:
                async with self.session.post(self.url, headers=self.headers) as response:
                    response.raise_for_status()
                    data = await response.json()
                    balance_coins = data["clickerUser"]["balanceCoins"]
                    last_passive_earn = data["clickerUser"]["lastPassiveEarn"]
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    logger.debug(
                        f"{current_time}: Token: {self.token}, balanceCoins: {balance_coins}, lastPassiveEarn: {last_passive_earn}")
                    break
            except aiohttp.ClientError as e:
                logger.error(f"Error for token {self.token}: {e}")
                await asyncio.sleep(10)

    async def apply_promo(self, promo_code: str):
        headers = {
            'accept': 'application/json',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': f'Bearer {self.token}',
            'content-type': 'application/json',
            'origin': 'https://hamsterkombatgame.io',
            'priority': 'u=1, i',
            'referer': 'https://hamsterkombatgame.io/',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': f'{user_agent.random}',
        }
        try:
            async with self.session.post(
                    "https://api.hamsterkombatgame.io/clicker/apply-promo",
                    headers=headers,
                    json={
                        'promoCode': promo_code,
                    }
            ) as response:
                # print(await response.json())
                response.raise_for_status()
                return True

        except Exception as e:
            logger.error(f"Error while apply_promo: {promo_code}: {e}")
            return False


async def process_accounts(tokens: list[str], batch_size: int = 50):
    async with aiohttp.ClientSession() as session:
        tasks = []

        for i in range(0, len(tokens), batch_size):
            batch = tokens[i:i + batch_size]

            for token in batch:
                account = HamsterAccount(token, session)
                tasks.append(account.claim())

            await asyncio.gather(*tasks)


async def process_promos(token: str, promos: list):
    async with aiohttp.ClientSession() as session:
        for promo in promos:
            account = HamsterAccount(token, session)
            await account.apply_promo(promo)

if __name__ == "__main__":
    access_tokens = ""
    asyncio.run(process_promos(access_tokens, []))
