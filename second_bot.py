import sys
if (sys.version_info[0] < 3) and (sys.version_info[1] < 11):
    raise Exception("Python 3.11 or a more recent version is required.")

import os
from dotenv import load_dotenv
import logging
import asyncio
import asqlite

from counter import Counter

import twitchio
from twitchio import eventsub
from twitchio.ext import commands

LOGGER: logging.Logger = logging.getLogger("Bot")

# This is where the Bot, its connections, and oauth are set up
class Bot(commands.Bot):
    def __init__(self, *, token_database: asqlite.Pool) -> None:
        self.token_database = token_database
        self.counter = Counter()
        
        self.owner_name=os.environ['OWNER_NAME']
        self.bot_name=os.environ['BOT_NAME']
        self.target_id=os.environ['TARGET_ID']
        self.target_name=os.environ['TARGET_NAME']
        
        super().__init__(
            client_id=os.environ['CLIENT_ID'],
            client_secret=os.environ['CLIENT_SECRET'],
            bot_id=os.environ['BOT_ID'],
            owner_id=os.environ['OWNER_ID'],
            prefix=os.environ['BOT_PREFIX'],
        )
    
    async def event_ready(self):
        # When the bot is ready
        LOGGER.info("Successfully logged in as: %s", self.bot_id)
    #    target = self.create_partialuser(user_id=self.target_id, user_login=self.target_name)
    #    await target.send_message(sender=self.bot_id, message='Bot has landed')

    #oauth token portion
    async def setup_hook(self) -> None:
        # Add our component which contains our commands...
        await self.add_component(MyComponent(self))

        # Check if the EventSub setup has been completed before
        async with self.token_database.acquire() as connection:
            row = await connection.fetchone("SELECT value FROM flags WHERE key = 'eventsub_initialized'")  # type: ignore

        # If this is the second run (EventSub setup has been done before)
        if row and row["value"] == "true":
            # Subscribe to chat messages (EventSub)
            subscription = eventsub.ChatMessageSubscription(broadcaster_user_id=self.target_id, user_id=self.bot_id)
            await self.subscribe_websocket(payload=subscription)
            
        else:
            # This is the first run, so skip EventSub subscription and mark it as completed
            print("First run — skipping EventSub subscription")
            async with self.token_database.acquire() as connection:
                await connection.execute(
                    "INSERT OR REPLACE INTO flags (key, value) VALUES ('eventsub_initialized', 'true')"
                )

    async def add_token(self, token: str, refresh: str) -> twitchio.authentication.ValidateTokenPayload:
        # Make sure to call super() as it will add the tokens interally and return us some data...
        resp: twitchio.authentication.ValidateTokenPayload = await super().add_token(token, refresh)

        # Store our tokens in a simple SQLite Database when they are authorized...
        query = """
        INSERT INTO tokens (user_id, token, refresh)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id)
        DO UPDATE SET
            token = excluded.token,
            refresh = excluded.refresh;
        """

        async with self.token_database.acquire() as connection:
            await connection.execute(query, (resp.user_id, token, refresh))

        LOGGER.info("Added token to the database for user: %s", resp.user_id)
        return resp

    async def load_tokens(self, path: str | None = None) -> None:
        # We don't need to call this manually, it is called in .login() from .start() internally...

        async with self.token_database.acquire() as connection:
            rows: list[sqlite3.Row] = await connection.fetchall("""SELECT * from tokens""") # type: ignore

        for row in rows:
            await self.add_token(row["token"], row["refresh"])

    async def setup_database(self) -> None:
        # Create our token table, if it doesn't exist..
        query = """CREATE TABLE IF NOT EXISTS tokens(user_id TEXT PRIMARY KEY, token TEXT NOT NULL, refresh TEXT NOT NULL)"""
        query_flags = """CREATE TABLE IF NOT EXISTS flags(key TEXT PRIMARY KEY, value TEXT NOT NULL)"""
        
        async with self.token_database.acquire() as connection:
            await connection.execute(query)         # tokens table
            await connection.execute(query_flags)   # flags table



#This is where all the commands and "reactions" for the bot are setup
class MyComponent(commands.Component):
    def __init__(self, bot: Bot):
        self.bot = bot
    
    async def event_command_error(self, ctx: commands.Context, error: Exception) -> None:
        if isinstance(error, commands.exceptions.GuardFailure):
            # Prevent traceback, optionally send a message
            await ctx.send("You don't have permission to use this command.")
            return
        elif isinstance(error, commands.exceptions.CommandNotFound):
            await ctx.send(f"Unknown command: {ctx.message.text}")
            return
        else:
            pass

    @commands.command()
    async def reset_meows(self, ctx: commands.Context) -> None:
        #aries only command that resets the number of meows
        if ctx.chatter.id == self.bot.target_id or ctx.chatter.id == '1227296518':
            await ctx.send(content="!reset_meows")
        
    
    
def main() -> None:
    load_dotenv()
    twitchio.utils.setup_logging(level=logging.INFO)

    async def runner() -> None:
        async with asqlite.create_pool("tokens.db") as tdb, Bot(token_database=tdb) as bot:
            await bot.setup_database()
            await bot.start()

    try:
        asyncio.run(runner())
    except KeyboardInterrupt:
        LOGGER.warning("Shutting down due to KeyboardInterrupt...")


if __name__ == "__main__":
    main()