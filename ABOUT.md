# About this Program
## This is a pair of twitch bots built in python mainly using the TwitchIO module

## Structure of the program
The program has 5 main components
1. The menu
2. The .env creator
3. The bot hub
4. The redeem counting bot
5. The chat command bot

## Prosses of the menu
The menu has 4 main steps to it's function
1. clear the console of text
2. print the lines of text that make up the menu
3. prompt the user for a selection
4. based on their selection preform the assosiated action
    1. launch the bots using the bot hub
    2. launch the bots in authenticating mode
    3. run the .env creator
    4. quit the program

## Prosses of the .env creator
The .env creator has 4 main steps to it's function
1. clear the console of text
2. print the lines of text that make up the menu
    > as the program is going line by line when it fetches certin line numbers it instead of printing the line issues a prompt. ie. the 4th line (index 3) says "Client ID: " this should be followed by an input. So it is used as the prompt for an input.
3. that data is then fed into a dictonary.
    > a dictonary is like a list that lets you fetch data using a key (often a string) instead of an index. ie. I can fetch the client id by calling dictonary["client_id"]
4. the data is then passed to another function that takes the data and writes it to a file called ".env".

## Prosses of the bot hub
The bot hub is a program that centrilizes the running and management of the 2 bots. Setting both bots up and running them in parallel.

## Structure of the Bots
the bots are nearly identical so I will describe the basic structure and then any nuances later

The bots are made of 2 main components
1. the bot object
2. the bot component

### The bot object
this is the main object, it is the client.
the bot object consists of 3 main parts
1. the initilization
    > this is where the bot recives all the information and connects to twitch
2. the subscription
    > this is where the bot tells twitch what notifications it wants to recive, ie. channel point redeems or chat messages
3. the oauth managment
    > this is where the bot either loads of sets up a server to get the keys that it needs to tell twitch that it has permision to do what it is doing

### The bot component
this is the support object, it hosts the logic for responding to events
the component consists of 2 main parts
1. the connection
    > this is where the component is attached to the bot making the 2 objects into 1 "super" object
2. the reactions 
    > this is where the logic for the commands/reactions are.

#### The commands
The structure of the commands is rather simple.
it conists of 2 main pieces
1. the decorators
    > this is what tells the bot what events trigger this command. ie. a channel point redeem or a chat message. this is also what tells the bot what if anything to filter out. ie. is the user a moderator or is the user a subcriber. there are 2 types of required decorators, listeners and commands, listeners are used to trigger based on events like a channel point redeem or a sub, commands are for chat text based commands like a user saying !meows.
2. the function 
    > this is where all the logic is hosted, after the decorators are met the program runs the corosponding funtion. ie. a chatter saying !meows will trigger the function meows, assuming that user fits all the decorrators, in this case there are none except the decorator "@commands.command" that tells the bot this is a command
