import asyncio
import os
import sys

import aioconsole
from dotenv import load_dotenv

from api.markets.binance import Binance
from api.markets.kucoin import KuCoin
from api.metrics.coinmarketcap import CoinMarketCap


def setup():
    load_dotenv()
    validation_directories = [
        ("data", "for caching of API info and other information"),
        ("data/binance", "for caching binance news posts that have not been evaluated"),
        ("data/coinmarketcap", "for caching SYMBOL -> coinmarketcap_id information etc")
    ]

    for directory_info in validation_directories:
        directory, purpose = directory_info

        if not os.path.isdir(os.path.join(os.path.dirname(__file__), directory)):
            print(f"INFO: creating '{directory}' directory {purpose}.")
            os.makedirs(directory)

    if not os.path.isfile(os.path.join(os.path.dirname(__file__), ".env")):
        print("ERROR: no .env file, please see example.env and modify accordingly and rename to .env")
        sys.exit()

    print("INFO: setup successfully")
    print("INFO: type exit to quit")


async def binance_scrape():
    timeout = int(os.getenv("BINANCE_SCRAPER_COOLDOWN"))
    print(f"Starting binance coroutine with timeout of {timeout} seconds..")
    while True:
        symbols = binance_scraper.is_new_listing_announcement()

        if symbols:
            pass

        await asyncio.sleep(timeout)


async def input_loop():
    while True:
        usr_input = await aioconsole.ainput()
        if usr_input == "exit":
            for task in asyncio.all_tasks():
                task.cancel()


async def main():
    try:
        await asyncio.gather(
            asyncio.create_task(binance_scrape()),
            asyncio.create_task(input_loop())
        )
    except asyncio.exceptions.CancelledError:
        print("Coroutines cancelled, closing.")


if __name__ == '__main__':
    setup()

    binance_scraper = Binance(
        root_dir=os.path.dirname(__file__)
    )
    kucoin = KuCoin(
        api_key=os.getenv("KUCOIN_API_KEY"),
        api_passphrase=os.getenv("KUCOIN_API_PASSPHRASE"),
        api_secret=os.getenv("KUCOIN_API_SECRET")
    )
    coinmarketcap_api = CoinMarketCap(
        api_key=os.getenv("COIN_MARKET_CAP_API_KEY")
    )
    asyncio.run(main())






