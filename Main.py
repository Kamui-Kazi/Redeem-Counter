from dotenv import load_dotenv
import logging
import asyncio
import asqlite
import threading

from webserver import run_flask
import bot_boy

import twitchio

def main() -> None:
    load_dotenv()
    twitchio.utils.setup_logging(level=logging.INFO)

    flaskThread = threading.Thread(target=run_flask, daemon=True)
    flaskThread.start()
    
    async def runner() -> None:
        async with asqlite.create_pool("tokens.db") as tdb, bot_boy.Bot(token_database=tdb) as bot:
            await bot.setup_database()
            await bot.start()
                
    try:
        asyncio.run(runner())
    except KeyboardInterrupt:
        bot_boy.LOGGER.warning("Shutting down due to KeyboardInterrupt...")


if __name__ == "__main__":
    main()