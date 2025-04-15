import os
from dotenv import load_dotenv
import logging
import asyncio
import asqlite

from counter import Counter

import twitchio
from twitchio import eventsub
from twitchio.ext import commands

load_dotenv()
LOGGER: logging.Logger = logging.getLogger("CommandBot")

# This is where the Bot, its connections, and oauth are set up
class CommandBot(commands.Bot):
    def __init__(self, *, token_database: asqlite.Pool) -> None:
        self.token_database = token_database
        self.counter = Counter
        
        self.owner_name=os.environ['OWNER_NAME']
        self.bot_name=os.environ['BOT_NAME_2']
        self.target_id=os.environ['TARGET_ID']
        self.target_name=os.environ['TARGET_NAME']
        
        super().__init__(
            client_id=os.environ['CLIENT_ID'],
            client_secret=os.environ['CLIENT_SECRET'],
            bot_id=os.environ['BOT_ID_2'],
            owner_id=os.environ['OWNER_ID'],
            prefix=os.environ['BOT_PREFIX'],
        )
    
    async def event_ready(self):
        # When the bot is ready
        LOGGER.info("Successfully logged in as: %s", self.bot_id)

    async def setup_hook(self) -> None:
        # Add our component which contains our commands...
        await self.add_component(CommandComponent(self))

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
    
    async def invoke(self, ctx: commands.Context):
        try:
            await ctx.invoke()
        except commands.CommandNotFound:
            LOGGER.warning("Unknown command: %s", ctx.message.text)
        except commands.GuardFailure:
            await ctx.reply("You don't have permission to use this command.")
            LOGGER.warning("Command called without perms: %s", ctx.message.text)


class CommandComponent(commands.Component):
    def __init__(self, bot: CommandBot):
        self.bot = bot
        self.counter = bot.counter

    # we use @commands.command() to initiate the setup of a command
    @commands.command()
    # To set the minimum permission/badge level to use this command remove the '#' at the begining of the line corosponding to the user level desired
    # To allow anyone to use the command place a '#' before all of the lines immediately following every level
    #@commands.is_broadcaster() # set's command to streamer only
    #@commands.is_moderator() # set's command to moderators and streamer only
    #@commands.is_elevated() # set's command to VIPs, moderators, and the streamer only
    async def meows(self, ctx: commands.Context) -> None:
        await self._meows(ctx)
    async def _meows(self, ctx: commands.Context) -> None:
        #mod only command that displays the number of meows 
        await ctx.reply(content=self.counter.pp())
        LOGGER.info("user: %s - used \"!meows\"", ctx.chatter.display_name)

    @commands.command()
    # To set the minimum permission/badge level to use this command remove the '#' at the begining of the line corosponding to the user level desired
    # To allow anyone to use the command place a '#' before all of the lines immediately following every level
    #@commands.is_broadcaster() # set's command to streamer only
    #@commands.is_moderator() # set's command to moderators and streamer only
    #@commands.is_elevated() # set's command to VIPs, moderators, and the streamer only
    async def meow_rewards(self, ctx: commands.Context) -> None:
        await self._meow_rewards(ctx)
    async def _meow_rewards(self, ctx: commands.Context) -> None:
        #public command that explains the meow cost of diffrent rewards
        reward_costs_1 = "Meow: 1 | Ara Ara: 10 | Senpai daisuki: 50 | Onii-chan: 100 | Nya for 10 minutes: 300 | X3 nuzzles song: 500"
        await ctx.send(content=reward_costs_1)
        LOGGER.info("user: %s - used \"!meow_rewards\"", ctx.chatter.display_name)
    
    @commands.command()
    # To set the minimum permission/badge level to use this command remove the '#' at the begining of the line corosponding to the user level desired
    # To allow anyone to use the command place a '#' before all of the lines immediately following every level
    #@commands.is_broadcaster() # set's command to streamer only
    #@commands.is_moderator() # set's command to moderators and streamer only
    #@commands.is_elevated() # set's command to VIPs, moderators, and the streamer only
    async def meow_commands(self, ctx: commands.Context) -> None:
        await self._meow_commands(ctx)
    async def _meow_commands(self, ctx: commands.Context) -> None:
        reply = "PUBLIC: !meows, !meow_rewards"
        if ctx.chatter.moderator or ctx.chatter.broadcaster:
            reply +=" | MOD ONLY: !add_meows, !sub_meows !set_meows, !reset_meows"
        await ctx.reply(content=reply)
        LOGGER.info("user: %s - used \"!meow_commands\"", ctx.chatter.display_name)
    
    @commands.command()
    # To set the minimum permission/badge level to use this command remove the '#' at the begining of the line corosponding to the user level desired
    # To allow anyone to use the command place a '#' before all of the lines immediately following every level
    #@commands.is_broadcaster() # set's command to streamer only
    @commands.is_moderator() # set's command to moderators and streamer only
    #@commands.is_elevated() # set's command to VIPs, moderators, and the streamer only
    async def add_meows(self, ctx: commands.Context, *, value: int=0) -> None:
        await self._add_meows(ctx, value)
    async def _add_meows(self, ctx: commands.Context, *, value: int=0) -> None:
        #mod only command that adds to the number of meows
        self.bot.counter.add(value)
        await ctx.reply(content=f"{value} Meows added, current count is {self.counter.count}")
        LOGGER.info("user: %s - used \"!add_meows\" to add %s meows, the current count is %s meows.", ctx.chatter.display_name, value, self.counter.count)

    @commands.command()
    # To set the minimum permission/badge level to use this command remove the '#' at the begining of the line corosponding to the user level desired
    # To allow anyone to use the command place a '#' before all of the lines immediately following every level
    #@commands.is_broadcaster() # set's command to streamer only
    @commands.is_moderator() # set's command to moderators and streamer only
    #@commands.is_elevated() # set's command to VIPs, moderators, and the streamer only
    async def sub_meows(self, ctx: commands.Context, *, value:str = '1') -> None:
        await self._sub_meows(ctx, value)
    async def _sub_meows(self, ctx: commands.Context, *, value:str = '1') -> None:
        command_dict = {'meow':1,'ara':10,'senpai':50,'onii':100,'nya':300, 'X3': 500}
        for key in command_dict:
            if key == value:
                pair = command_dict[key]
                self.counter.subtract(pair)
                await ctx.reply(content=f"Removed {pair} meows. Current count is {self.counter.count} meows")
                LOGGER.info("user: %s - used \"!sub_meows\" to remove %s meows, the current count is %s meows.", ctx.chatter.display_name, pair, self.counter.count)
                return
        
        self.counter.subtract(int(value))
        await ctx.reply(content=f"Removed {value} meows. Current count is {self.counter.count} meows")
        LOGGER.info("user: %s - used \"!sub_meows\" to remove %s meows, the current count is %s meows.", ctx.chatter.display_name, value, self.counter.count)

    @commands.command()
    # To set the minimum permission/badge level to use this command remove the '#' at the begining of the line corosponding to the user level desired
    # To allow anyone to use the command place a '#' before all of the lines immediately following every level
    #@commands.is_broadcaster() # set's command to streamer only
    @commands.is_moderator() # set's command to moderators and streamer only
    #@commands.is_elevated() # set's command to VIPs, moderators, and the streamer only
    async def set_meows(self, ctx: commands.Context, *, value: int=0) -> None:
        await self._set_meows(ctx, value)
    async def _set_meows(self, ctx: commands.Context, *, value: int=0) -> None:
        #mod only command that sets the number of meows
        self.counter.set(value)
        await ctx.reply(content=f"Meows set to {value}")
        LOGGER.info("user: %s - used \"!set_meows\" to set the meow count to %s.", ctx.chatter.display_name, self.counter.count)

    @commands.command()
    # To set the minimum permission/badge level to use this command remove the '#' at the begining of the line corosponding to the user level desired
    # To allow anyone to use the command place a '#' before all of the lines immediately following every level
    #@commands.is_broadcaster() # set's command to streamer only
    @commands.is_moderator() # set's command to moderators and streamer only
    #@commands.is_elevated() # set's command to VIPs, moderators, and the streamer only
    async def reset_meows(self, ctx: commands.Context) -> None:
        await self._reset_meows(ctx)
    async def _reset_meows(self, ctx: commands.Context) -> None:
        #mod only command that resets the number of meows
        self.counter.reset() 
        await ctx.reply(content="Meows Reset")
        LOGGER.info("user: %s - used \"!reset_meows\" to reset the meow count to %s.", ctx.chatter.display_name, self.counter.count)

    @commands.command()
    # To set the minimum permission/badge level to use this command remove the '#' at the begining of the line corosponding to the user level desired
    # To allow anyone to use the command place a '#' before all of the lines immediately following every level
    #@commands.is_broadcaster() # set's command to streamer only
    #@commands.is_moderator() # set's command to moderators and streamer only
    #@commands.is_elevated() # set's command to VIPs, moderators, and the streamer only
    async def meow(self, ctx: commands.Context, command_type: str = 'count', value: int = 0) -> None:
        command_dict = {
            'count': self.meows,
            'rewards': self.meow_rewards,
            'commands': self.meow_commands,
            'add': self.add_meows,
            'sub': self.sub_meows,
            'set': self.set_meows,
            'reset': self.reset_meows
        }

        func = command_dict.get(command_type)

        

        if func:
            if command_type in ['add', 'sub', 'set', 'reset']:
                if (ctx.chatter._is_moderator or ctx.chatter._is_broadcaster):
                    if command_type in ['add', 'sub', 'set']:
                        await func(ctx, value)
                    else:
                        await func(ctx)
                else:
                    await ctx.reply("You don't have the perms for this silly.")
            else:
                await func(ctx)
        else:
            await ctx.send(f"Unknown meow command type: {command_type}")
