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

!sub_meows *amount to subtract*
>Mod / Channel Owner only
>
>replace the *amount to subtract* with the amount of meows you would like to subtract
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

!meow x
> all of the above commands have been made callable using !meow x
> 
> x is the key word and optinal value
>
> ie. to call !add_meows 10 you can now use !meow add 10
>
> the key words are: count (default), rewards, commands, add, sub, set, reset 

## creating a Twitch application
1. Go to http://dev.twitch.tv/console and Create an Application
2. Add: http://localhost:4343/oauth/callback as the callback URL
3. Make a note of your CLIENT_ID and CLIENT_SECRET.

(these instructions are from https://twitchio.dev/en/latest/getting-started/quickstart.html) 


## setting up a python enviroment
if you already have used python on this computer you can skip this section
### installing python
1. go to this website https://www.python.org/downloads/ and download at least python 3.11, as of this moment python 3.14 is not fully compatable so stick with 3.11 - 3.13
2. run the executable you just downloaded
3. The installation window shoud shows two checkboxes: for Admin privileges and Add Python to PATH, check both
4. if you didn't don't worry we can fix it later
5. select install now
6. after it installs it should give the option to disable the path length limit, do so
### Add Python to PATH
if you didn't before this will fix that, also if pip isn't working this might fix it.
1. In the Start menu, search for Environment Variables and press Enter.
2. Click Environment Variables to open the overview screen.
3. The action opens the Environment Variable tab. In the Environment Variables window, there are two sections: User Variables (affecting only the current user) and System Variables (affecting all users on the PC). Since the system gets Python for all users, modify the System Variables section.
4. Scroll down to find the Path variable under System Variables.
5. Select the Path variable and click Edit. This opens the Edit Environment Variable window.
6. In the Edit Environment Variable window, click New to add a new entry to the path and add the following: `C:\Users\*your user*\AppData\Local\Programs\Python\Python313\`
7. add another entry to the path and and add the following: `C:\Users\*your user*\AppData\Local\Programs\Python\Python313\Scripts\`
8. Click OK to save the changes
   (these instructions are from https://phoenixnap.com/kb/how-to-install-python-3-windows)

## setup the bot
1. Create a new Twitch account. This will be the dedicated bot account.
2. Enter your CLIENT_ID and CLIENT_SECRET from the twitch application you made above into the provided .env file
3. do the same with the BOT_ID and OWNER_ID, these are not your usernames, these are numerical IDs that you can get from https://www.streamweasels.com/tools/convert-twitch-username-%20to-user-id/
4. Comment out everything in setup_hook.
5. Run the bot.
6. Open a new browser / incognito mode, log in as the bot account and visit http://localhost:4343/oauth?scopes=user:read:chat%20user:write:chat%20user:bot%20channel:read:redemptions
7. Whilst logged in as the stream channel account, visit http://localhost:4343/oauth?scopes=channel:bot
8. Stop the bot and uncomment everything in setup_hook.
9. Start the bot.

## to get the twitch ids I used this site
https://www.streamweasels.com/tools/convert-twitch-username-%20to-user-id/
