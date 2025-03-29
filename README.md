# Twitch-notif (Redeem counter)

## Bot commands
!meows
>public
>
> replies with the amount of meows

!meow_rewards
>public
>
>sends a message that explaines the cost of the diffrent rewards for the ammount of meows redeemed

!meow_commands
>public
>
>replies with a list of the commands avalible to the caller

!add_meows *amount to add*
>limited to mods
>
>replace the *amount to add* with the amount of meows you would like to add
>
>replies with the amount it recived and the new total

!set_meows *amount to add*
>limited to mods
>
>replace the *amount to add* with the amount of meows you would like to have in the counter
>
>replies with the new total meows

!reset_meows
>limited to mods
>
>resets the count of meows

## setup the bot
1. Create a new Twitch account. This will be the dedicated bot account.
2. Enter your CLIENT_ID, CLIENT_SECRET, BOT_ID and OWNER_ID into a file called `.env`
3. Comment out everything in setup_hook.
4. Run the bot.
5. Open a new browser / incognito mode, log in as the bot account and visit http://localhost:4343/oauth?scopes=user:read:chat%20user:write:chat%20user:bot%20channel:read:redemptions
6. In your main browser whilst logged in as your account, visit http://localhost:4343/oauth?scopes=channel:bot
7. Stop the bot and uncomment everything in setup_hook.
8. Start the bot.
