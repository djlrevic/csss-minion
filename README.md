# csss-minion

# Information: #

The csss-minion bot is maintained by Henry Zhou (henrymzhou) using Python 3 and discord.py for SFU's Computing Science Student Society. The bot accepts user input from Discord chat channels and runs a script to execute the command. Commands available include WolframAlpha math functions, Google Translate functionality, and administrative commands. Valid inputs are processed by the bot and the specific command is executed. The bot then displays the command output to the user. When an invalid input is detected, the bot sends feedback to the user indicating the command does not exist.

This bot supports ranks by giving users EXP every time they participate in chat. There are also custom ranks that users can place themselves in to add themselves to classes, allowing a user to find other students in their classes. 

The bot also supports audio playback of music, which can be added from any YouTube video. 

A user can add a "cog", which is a additional file that has custom implementation to expand the use of the bot. The bot has built-in load and unloading of cogs available through its commands.

A complete list of commands in listed below, and can also be found using the `.help` command.

This bot is covered under the GPL-2.0 License.

# Bot Setup: #

Duplicate `botMain.settings.sample` as `botMain.settings` and add your own discord bot token. Afterwards, run the bot using `python3 csss-minion.py test`. The `test` argument skips
loading all cogs and allows anyone to use commands usually restricted to Henry.

Loading any cog is possible with `.load <cog>`, and listing available cogs can be done with `.cogs`.

The bot's `.help` command will list all the currently implemented commands, listed in greater detail below.

Source Code
https://github.com/henrymzhao/csss-minion/


# Commands: #

## Administrative Commands: ##

These commands are available to moderation and administrative users. Often these are back end commands that allow for the deletion of messages, the locking and unlocking of channels, and the loading and unloading of cogs for the bot.

**.announce <title> <desc>**

Makes an announcement.

Usage: .announce <title> <body>

**.clear <amount>**

Clears set amount of messages above current messages.

Usage: .clear 50

**.clearspam**

Clears the spam.

Usage: .clearspam

**.cogs**

Lists the currently loaded cogs.

Usage: .cogs

**.em [desc...]**

Make an embedded message.

Usage: .em <message>

**.exc [args...]**

Execute a bash command

Usage: .exc ls -a

**.load <name>**

Loads a cog.

Usage: .load Announce

**.lock**

Locks current channel.

Usage: .lock

**.modsay [msg...]**

Give a stern message (Heavily inspired by brenfan's .em code <3).

Usage: .modsay "This is a stern message."

**.propagateMute**

Adds the Muted role to every channel, maintaining universal control and ruleset for muted role

Usage: .propagateMute

**.refreshCache**

Refresh the server wordart cache. 

Usage: .refreshCache

**.reload <name>**

Reloads the cogs.

Usage: .reload Announce
 
**.restrict <user> (not yet implemented)**

Restricts a user from posting in a channel

Usage: .restrict <John Doe>

**.unload <name>**

Unloads a cog.

Usage: .unload Announce

**.unlock**

Unlocks the current channel.

**.unrestrict [msg...] (not yet implemented)**

Undo any restrictions on a user for all channels. 

Usage: !unrestrict [users..]

## Miscellaneous Commands: ##

These are miscellaneous commands that add more character to the bot. These commands range from queries to DuckDuckGo and WolframAlpha, to posting cute cat pictures and wordart clouds.

**.allreminders**

Lists all the active reminders. Does not list reminders from remindmein.

Usage: .allreminders

**.antonym <word>**

Returns a few antonyms of a given word.

Usage: .antonym clever

**.avatart [args...]**

Makes a wordcloud in the shape of your avatar.

Usage: .avatart <invert> <bgcolor>

**.beep**

Returns the message "boop". Useful when seeing if the bot is alive. Similar to .ding and .ping.

Usage: .beep

**.ding**

Returns the message "dong". Useful when seeing if the bot is alive. Similar to .beep and .ping.

Usage: .ding

**.doraemon**

Shows a cute cat picture.

Usage: .doraemon

**.eggplant**

Prints "My eggplant brings all the boys to the yard."

Usage: .eggplant

*And they're like, it's better than yours*

**.eggwrite [msg...]**

Use the bot to write with eggplant emojis.

Usage: .eggwrite "This is a message."

*Only works with letters*

**.gameR**

Starts the roulette game.

Usage: .gameR

**.goodluck**

Shows a photo of an eggplant in the shape of a thumbs up, wishing someone good luck

Usage: .goodluck

**.help**

The help command will display the information menu in the chat. This menu contains brief descriptions of all possible commands, and provides a link to the source code.

Usage: .help

**.help mc**

This can only be used within the #minecraft channel. When the command is used in correct channel, it will display commands specific to MineCraft. Outside of the correct channel, it will display a message alerting the user to move to that channel.

Usage: .help mc

**.henry**

Posts a photo of people bowing to Henry, the bot creator.

Usage: .henry

**.howoldami**

Displays when you joined the server in days.

Usage: .howoldami

**.imgur [word...]**

Search for a picture on imgur MISC

Usage: .imgur cat

**.impeach**

Posts a photo of Henry coming out of a giant peach.

Usage: .impeach

**.info**

Displays the old MineCraft server information

Usage: .info

**.joke**

Displays a photo of a joke flying over Henry's head

Usage: .joke

**.kms**

Currently broken.

Usage: .kms

**.meaning <word>**

Returns the definition of the given word.

Usage: .meaning life

**.myreminders**

Lists only user's own reminders

Usage: .myreminders

**.mytop10**

Displays your top 10 words on the server.

Usage: .mytop10

**.outline [args...]**

Display an SFU course's outline

Usage: outline <department> <number> (section) (year) (semester)

**.ping**

Returns the message "pong". Useful when seeing if the bot is alive. Similar to .beep and .ding.

Usage: .ping

**.poem [args...]**

Searches for a poem and private messages it to the user.

Usage: !poem <title> <author> <length>

**.poll [args...]**

Create an instant poll. Defaults to yes/no if no choices supplied.

Usage: .poll <subject> [option 1]...[option N]

**.prettygood**

Photo of a man saying "Heyyyy, that's pretty good"

Usage: .prettygood

**.remindme [words] [time]**

Reminds the user to do some thing at the given time. Format: YYYY MM DD [HH] [mm] [ss]

Usage: .remindme "hang the cat to dry" 2017 8 5

**.remindmein [time] [words]**

Reminds the user to do some thing at the given time.

Usage: .remindmein 2 days "do that thing"

**.roads [campus]**

Display road conditions for SFU. Campus must be an SFU campus.

Usage: .roads <campus>

**.search [query...]**

Search the Internet using DuckDuckGo.

Usage: .search "cute cats"

**.servart**

Make a wordcloud out of the server's most common words.

Usage: .servart

**.sfu [words...]**

Lookup an SFU class' information. Includes class calendar page.

Usage: .sfu <cmpt120> or .sfu <cmpt> <120>

**.status**

Display the number of players on the MineCraft server

Usage: .status

*Dead Command*

**.stealthegg**

Puts an eggplant emoji in chat.

Usage: .stealthegg

**.spell <word>**

Check your spelling of the given word.

Usage: .spell wierd

**.synonym <word>**

Returns the synonym of a word

Usage: .synonym clever

**.top10**

Displays the top 10 words on the server.

Usage: .top10

**.translate "message" <target> (source)**

Translate a string into a specified language. To specify source language, include a third arg.

Usage: 

.translate "message" <target> (source)

Example of a translation into Spanish: <!translate "I like cheese" es>

!translate "Je suis formé à la guerre de Nerf et j'ai le plus d'étoiles d'or dans toute la classe maternelle." en fr

*Supported languages and language codes listed on this webpage
https://cloud.google.com/translate/docs/languages*

**.triggered**

Posts a GIF of an angry face in chat.

Usage: .triggered

**.urban [msg...]**

Queries urban dictionary for the entry you provide.

Usage: .urban hip

**.wiki [msg...]**

Looks up the given input on Wikipedia.

Usage: .wiki "wolf"

**.wolf [args...]**

Queries WolframAlpha with given input

Usage: .wolf "How many cups are there in a quart?"

**.wordart**

Makes a wordcloud out of your most common words on the server.

Usage: .wordart

**.youtube [query...]**

Search for a youtube video

Usage: .youtube "Never Gonna Give You Up"

## Music Commands: ##

These commands are to control the bot's behaviour when playing music. This includes adding songs to the queue, pausing and resuming music, and moving which channel the bot is in.

**.bump <index>**

Vote to bump the indexed song to the front.

Usage: .bump 2

**.join <channel>**

Makes the bot join a voice channel to play music.

Usage: .join General

**.pause**

Pauses the currently played song.

Usage: .pause

**.play <song>**

Plays a song. If there is a song currently in the queue, then it is
queued until the next song is done playing.
This command automatically searches as well from YouTube.

Usage: .play "The Sun Roars Into View"

*The list of supported sites can be found here:
https://rg3.github.io/youtube-dl/supportedsites.html*

**.playmsg <msg>**

Changes the bot's playing message

Usage: .playing <msg>

**.playing**

Shows information about the currently played song.

Usage: .playing

**.queue**

Shows songs in the current queue.

Usage: .queue

**.resume**

Resumes the currently playing song.

Usage: .resume

**.skip**

Vote to skip the current song. The song requester can automatically skip.
3 skip votes are needed for the song to be skipped.

Usage: .skip

**.stop**

Stops playing audio and leaves the voice channel. This also clears the queue.

Usage: .stop

**.summon**

Make the bot join your current voice channel. Plays music if there is music in the queue.

Usage: .summon

**.volume <value>**

Sets the volume of the currently playing song.

Usage: .volume 50

## Rank Commands: ##

These commands are to control the custom user ranks. These commands include giving EXP to users, adding and removing users from ranks, and the creation of a custom ranks.

**.gexp <user> <amount>**

Gives input amount of EXP to given user.

Usage: .gexp Henry 100

**.iam \<course\>**

You can use this command to give yourself any roles that already exist, and consists of entirely lowercase letters or numbers. The \<class\> format follows the same rules as the .newclass command shown above. If the role you attempted to join does not exist, it will be created and you will be given it.

Usage: .iam "cmpt376"

**.iamn <course>**

Remove yourself from a discord class/role assigned by the **.iam** command

Usage: .iamn <cmpt376>

**.levels**

Shows the list of users sorted by rank

Usage: .levels

**.newclass \<class\>**

This command will create a new class role, and give you that role. The name of the role will either be the first word typed after the .newclass command, or will be the entire string between the first quotation marks. An example is shown below. It is also worth noting that all roles created using this command will be converted to lowercase for security reasons.

Usage: 

.newclass cmpt376 = a new role with the name "cmpt376"

.newclass one two three = a new role with the name "one."

.newclass "one two three" = a new role with the name "one two three."

**.rank**

Displays your current rank on the server

Usage: .rank

**.stats**

Shows EXP changes in the past amount of time. 

Usage: .stats

*Currently broken*

**.whois <course>**

Lists people in the discord role/class provided.

Usage: whois <cmpt376>