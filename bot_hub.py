import sys
if (sys.version_info[0] < 3) and (sys.version_info[1] < 11):
    raise Exception("Python 3.11 or a more recent version is required.")

import os
from dotenv import load_dotenv
import logging
import asyncio
import asqlite

from RedeemBot import RedeemBot
from CommandBot import CommandBot

import twitchio

LOGGER: logging.Logger = logging.getLogger("Bot")
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def main(auth_mode:bool = False) -> None:
    clear_console()
    load_dotenv()
    twitchio.utils.setup_logging(level=logging.INFO)

    async def runner() -> None:
        async with asqlite.create_pool("tokens.db") as tdb, RedeemBot(auth_mode=auth_mode, token_database=tdb) as rbot, CommandBot(auth_mode=auth_mode, token_database=tdb) as cbot:
            await rbot.setup_database()
            
            await asyncio.gather(
                cbot.start(),
                rbot.start()
            )

    try:
        asyncio.run(runner())
    except KeyboardInterrupt:
        LOGGER.warning("Shutting down due to KeyboardInterrupt...")


if __name__ == "__main__":
    main()