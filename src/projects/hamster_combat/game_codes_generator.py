import asyncio
import random
import time
import uuid

import aiohttp

from src.config import logger


class Game:
    def __init__(self, name: str, app_token: str, promo_id: str):
        self.name = name
        self.app_token = app_token
        self.promo_id = promo_id


class GameRepository:
    games = {
        # 1: Game('Riding Extreme 3D', 'd28721be-fd2d-4b45-869e-9f253b554e50', '43e35910-c168-4634-ad4f-52fd764a843f'),
        2: Game('Chain Cube 2048', 'd1690a07-3780-4068-810f-9b5bbf2931b2', 'b4170868-cef0-424f-8eb9-be0622e8e8e3'),
        # 3: Game('My Clone Army', '74ee0b5b-775e-4bee-974f-63e7f4d5bacb', 'fe693b26-b342-4159-8808-15e3ff7f8767'),
        4: Game('Train Miner', '82647f43-3f87-402d-88dd-09a90025313f', 'c4480ac7-e178-4973-8061-9ed5b2e17954'),
        5: Game('Merge Away', '8d1cc2ad-e097-4b86-90ef-7a27e19fb833', 'dc128d28-c45b-411c-98ff-ac7726fbaea4'),
        6: Game('Twerk Race', '61308365-9d16-4040-8bb0-2f4a4c69074c', '61308365-9d16-4040-8bb0-2f4a4c69074c'),
        7: Game('Polysphere', '2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71', '2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71'),
        8: Game('Mow And Trim', 'ef319a80-949a-492e-8ee0-424fb5fc20a6', 'ef319a80-949a-492e-8ee0-424fb5fc20a6'),
        # 9: Game('Mud Racing', '8814a785-97fb-4177-9193-ca4180ff9da8', '8814a785-97fb-4177-9193-ca4180ff9da8'),
        # 10: Game('Cafe Dash', 'bc0971b8-04df-4e72-8a3e-ec4dc663cd11', 'bc0971b8-04df-4e72-8a3e-ec4dc663cd11'),
        # 11: Game('Gangs Wars', 'b6de60a0-e030-48bb-a551-548372493523', 'c7821fa7-6632-482c-9635-2bd5798585f9'),
        12: Game('Zoopolis', 'b2436c89-e0aa-4aed-8046-9b0515e1c46b', 'b2436c89-e0aa-4aed-8046-9b0515e1c46b'),
        13: Game('Tile Trio', 'e68b39d2-4880-4a31-b3aa-0393e7df10c7', 'e68b39d2-4880-4a31-b3aa-0393e7df10c7'),
        14: Game('Fluff Crusade', '112887b0-a8af-4eb2-ac63-d82df78283d9', '112887b0-a8af-4eb2-ac63-d82df78283d9'),
        15: Game('Stone Age', '04ebd6de-69b7-43d1-9c4b-04a6ca3305af', '04ebd6de-69b7-43d1-9c4b-04a6ca3305af'),
        16: Game('Bouncemasters', 'bc72d3b9-8e91-4884-9c33-f72482f0db37', 'bc72d3b9-8e91-4884-9c33-f72482f0db37')
    }

    def __init__(self):
        ...

    def get_game(self, game_id: int) -> Game:
        return self.games.get(game_id)


class ClientManager:
    BASE_URL = 'https://api.gamepromo.io/promo/'

    @staticmethod
    def generate_client_id() -> str:
        timestamp = int(time.time() * 1000)
        random_numbers = ''.join(str(random.randint(0, 9)) for _ in range(19))
        return f'{timestamp}-{random_numbers}'

    @staticmethod
    def generate_random_uuid() -> str:
        return str(uuid.uuid4())

    async def login_client(self, session: aiohttp.ClientSession, game: Game) -> str:
        client_id = self.generate_client_id()
        data = {
            'appToken': game.app_token,
            'clientId': client_id,
            'clientOrigin': 'deviceid'
        }
        headers = {'Content-Type': 'application/json; charset=utf-8'}

        while True:
            try:
                async with session.post(self.BASE_URL + 'login-client', json=data, headers=headers) as response:
                    response.raise_for_status()
                    result = await response.json()
                    return result.get('clientToken')
            except aiohttp.ClientError:
                # logger.error(f'Error logging in client')
                await asyncio.sleep(10)

    async def register_event(self, session: aiohttp.ClientSession, game: Game, token: str) -> bool:
        event_id = self.generate_random_uuid()
        data = {
            'promoId': game.promo_id,
            'eventId': event_id,
            'eventOrigin': 'undefined'
        }
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json; charset=utf-8'
        }

        while True:
            try:
                async with session.post(self.BASE_URL + 'register-event', json=data, headers=headers) as response:
                    response.raise_for_status()
                    result = await response.json()
                    if not result.get('hasCode'):
                        await asyncio.sleep(10)
                    else:
                        return True
            except aiohttp.ClientError:
                await asyncio.sleep(10)

    async def create_code(self, session: aiohttp.ClientSession, game: Game, token: str) -> str:
        data = {'promoId': game.promo_id}
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json; charset=utf-8'
        }

        while True:
            try:
                async with session.post(self.BASE_URL + 'create-code', json=data, headers=headers) as response:
                    response.raise_for_status()
                    result = await response.json()
                    if 'promoCode' in result:
                        return result['promoCode']
            except aiohttp.ClientError:
                await asyncio.sleep(5)


class PromoCodeGenerator:
    def __init__(self, game_id: int):
        self.game_id = game_id
        self.game_repo = GameRepository()
        self.client_manager = ClientManager()
        self.game = self.game_repo.get_game(game_id)

    async def generate_promo_codes(self, key_count: int):
        codes = []
        async with aiohttp.ClientSession() as session:
            tasks = [self._generate_code_task(session) for _ in range(key_count)]
            codes = await asyncio.gather(*tasks)

        logger.info(f"Generated Promo Codes | Total:{len(codes)} | {codes[:3]}...")
        return codes

    async def _generate_code_task(self, session: aiohttp.ClientSession):
        token = await self.client_manager.login_client(session, self.game)
        if await self.client_manager.register_event(session, self.game, token):
            promo_code = await self.client_manager.create_code(session, self.game, token)
            return promo_code


async def generate(game_id, key_count):
    generator = PromoCodeGenerator(game_id)
    promo_codes = await generator.generate_promo_codes(key_count)
    return promo_codes
