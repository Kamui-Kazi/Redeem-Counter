import sys
if (sys.version_info[0] < 3) and (sys.version_info[1] < 11):
    raise Exception("Python 3.11 or a more recent version is required.")

import os
from dotenv import load_dotenv
import logging
import asyncio
import asqlite
import threading

from RedeemBot import RedeemBot
from CommandBot import CommandBot

import twitchio


# Add it to your TwitchIO logger and root logger (or any specific ones you want)
LOGGER = logging.getLogger('Bots')



def start() -> None:
    load_dotenv()
    twitchio.utils.setup_logging(level=logging.INFO)
    LOGGER.info("Bot is starting...")

    async def runner() -> None:
        async with asqlite.create_pool("tokens.db") as tdb, RedeemBot(token_database=tdb) as rbot, CommandBot(token_database=tdb) as cbot:
            await rbot.setup_database()
            
            await asyncio.gather(
                cbot.start(),
                rbot.start()
            )

    try:
        asyncio.run(runner())
    except KeyboardInterrupt:
        LOGGER.warning("Shutting down due to KeyboardInterrupt...")

def run_bot_in_background():
    thread = threading.Thread(target=start, daemon=True)
    thread.start()


if __name__ == '__main__':
    start()