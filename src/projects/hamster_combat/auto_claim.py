import asyncio
import aiohttp
from datetime import datetime


class HamsterAccount:
    def __init__(self, token: str, session: aiohttp.ClientSession):
        self.token = token
        self.session = session
        self.url = "https://url..."
        self.headers = {
            "Host": "api.hamsterkombat.io",
            "Authorization": f"Bearer {self.token}",
            "Sec-Fetch-Site": "same-site",
            "Accept-Language": "ru",
            "Sec-Fetch-Mode": "cors",
            "Accept": "/",
            "Origin": "https://hamsterkombat.io",
            "Content-Length": "0",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko)",
            "Referer": "https://hamsterkombat.io/",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty"
        }

    async def claim(self):
        while True:
            try:
                async with self.session.post(self.url, headers=self.headers) as response:
                    response.raise_for_status()
                    data = await response.json()
                    balance_coins = data["clickerUser"]["balanceCoins"]
                    last_passive_earn = data["clickerUser"]["lastPassiveEarn"]
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(
                        f"{current_time}: Token: {self.token}, balanceCoins: {balance_coins}, lastPassiveEarn: {last_passive_earn}")
                    break
            except aiohttp.ClientError as e:
                print(f"Error for token {self.token}: {e}")
                await asyncio.sleep(10)


async def process_accounts(tokens: list[str], batch_size: int = 50):
    async with aiohttp.ClientSession() as session:
        tasks = []

        for i in range(0, len(tokens), batch_size):
            batch = tokens[i:i + batch_size]

            for token in batch:
                account = HamsterAccount(token, session)
                tasks.append(account.claim())

            await asyncio.gather(*tasks)


if __name__ == "__main__":
    access_tokens = ["token1", "token2", "token3", ...]
    asyncio.run(process_accounts(access_tokens))
