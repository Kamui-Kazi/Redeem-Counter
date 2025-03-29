import os
from dotenv import load_dotenv
import logging
import asyncio
import asqlite

import twitchio
from twitchio import eventsub
from twitchio.ext import commands

LOGGER: logging.Logger = logging.getLogger("Bot")

# creating the class that is used to keep track of the number of meows
class Counter():
    def __init__(self):
        self.count = 0
    def add(self, count: int):
        self.count += count
    def set(self, count: int):
        self.count = count
    def reset(self):
        self.count = 0
    def pp(self) -> str:
        return f"Meow has been redeemed {self.count} times"



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
        target = self.create_partialuser(user_id=self.target_id, user_login=self.target_name)
        await target.send_message(sender=self.bot_id, message='Bot has landed')

    #oauth token portion
    async def setup_hook(self) -> None:
        # Add our component which contains our commands...
        await self.add_component(MyComponent(self))
    
        # Subscribe to chat (event_message)
        subscription = eventsub.ChatMessageSubscription(broadcaster_user_id=self.target_id, user_id=self.bot_id)
        await self.subscribe_websocket(payload=subscription)

        # Subscribe to reward redeems (event_custom_redemption_add)
        # subscription = eventsub.ChannelPointsRedeemAddSubscription(broadcaster_user_id=self.target_id)
        # await self.subscribe_websocket(payload=subscription)

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
        async with self.token_database.acquire() as connection:
            await connection.execute(query)



#This is where all the commands and "reactions" for the bot are setup
class MyComponent(commands.Component):
    def __init__(self, bot: Bot):
        self.bot = bot
    
    async def event_command_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, commands.CheckFailure):
            # Prevent traceback, optionally send a message
            await ctx.send("You don't have permission to use this command.")
        else:
            # Print unexpected errors
            print(f"Unexpected error: {error}")

    # We use this listener to increment the count every time a Meow is redeemed
    @commands.Component.listener()
    async def event_custom_redemption_add(self, payload: twitchio.ChannelPointsRedemptionAdd):
        self.bot.counter.add(1)
        #prints out the info assosiated with the redeem
        #print(f"[{payload.broadcaster.display_name}] - user:{payload.user.display_name}: redeemed - {payload.reward.title}, {payload.reward.id} | id: {payload.id}")

    # # We use a listener in our Component to display the messages received.
    # @commands.Component.listener()
    # async def event_message(self, payload: twitchio.ChatMessage) -> None:
    #     pass

    # we use @commands.command() to initiate the setup of a command
    @commands.command()
    async def meows(self, ctx: commands.Context) -> None:
        #mod only command that displays the number of meows 
        await ctx.reply(content=self.bot.counter.pp())

    @commands.command()
    async def meow_rewards(self, ctx: commands.Context) -> None:
        #public command that explains the meow cost of diffrent rewards
        #reward_costs_1 = "Key| Aries says: cost in Meows "
        #await ctx.send(content=reward_costs_1)
        reward_costs_2 = "Meow: 1 | Ara Ara: 10 | Senpai daisuki: 50 | Nya for 10 minutes: 100 | X3 nuzzles song: 500"
        await ctx.send(content=reward_costs_2)
    
    @commands.command()
    async def meow_commands(self, ctx: commands.Context) -> None:
        reply = "PUBLIC: !meows, !meow_rewards"
        if ctx.chatter.moderator or ctx.chatter.broadcaster:
            reply +=" | MOD ONLY: !add_meows, !set_meows, !reset_meows"
        await ctx.reply(content=reply)
    
    @commands.command()
    @commands.is_moderator()
    async def add_meows(self, ctx: commands.Context, *, value: int=0) -> None:
        #mod only command that adds to the number of meows
        self.bot.counter.add(value)
        await ctx.reply(content=f"{value} Meows added, current count is {self.bot.counter.count}")

    @commands.command()
    @commands.is_moderator()
    async def set_meows(self, ctx: commands.Context, *, value: int=0) -> None:
        #mod only command that sets the number of meows
        self.bot.counter.set(value)
        await ctx.reply(content=f"Meows set to {value}")

    @commands.command()
    @commands.is_moderator()
    async def reset_meows(self, ctx: commands.Context) -> None:
        #mod only command that resets the number of meows
        self.bot.counter.reset() 
        await ctx.reply(content="Meows Reset")
        
    
    
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