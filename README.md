# Redeem counter (Twitch bot)

This is a bot for a streamer who has a channel point redeem called 'meow for chat' that is rapidly redeemed at points during stream. They refund the redeems as they come in and as such they need to keep track of the count, so far they have been having their mods count the redeems but as there can be hundreds of redeems, this is a difficult position, they already tried to use Stream Elements to count the redeems but Stream Elements was unable to keep up with the several redeems per second.

required python version >= 3.11

## Bot commands
!meows
>public
>
> replies with the amount of meows

!meow_rewards
>public
>
>sends a message that explains the cost of the different rewards for the amount of meows redeemed

!meow_commands
>public
>
>replies with a list of the commands avalible to the caller

!add_meows *amount to add*
>Mod / Channel Owner only
>
>replace the *amount to add* with the amount of meows you would like to add
>
>replies with the amount it recived and the new total

!set_meows *new value*
>Mod / Channel Owner only
>
>replace the *new value* with the amount of meows you would like to have in the counter
>
>replies with the new total meows

!reset_meows
>Mod / Channel Owner only
>
>resets the count of meows

## setup the bot
1. Create a new Twitch account. This will be the dedicated bot account.
2. Enter your CLIENT_ID, CLIENT_SECRET, BOT_ID and OWNER_ID into the provided .env file
3. Comment out everything in setup_hook.
4. Run the bot.
5. Open a new browser / incognito mode, log in as the bot account and visit http://localhost:4343/oauth?scopes=user:read:chat%20user:write:chat%20user:bot%20channel:read:redemptions
6. Whilst logged in as the stream channel account, visit http://localhost:4343/oauth?scopes=channel:bot
7. Stop the bot and uncomment everything in setup_hook.
8. Start the bot.

## to get the twitch ids I used this site
https://www.streamweasels.com/tools/convert-twitch-username-%20to-user-id/
