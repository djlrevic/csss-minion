# csss-minion

The csss-minion bot is programmed by Henry Zhou (henrymzhou) using Python 3 and discord.py for SFU's Computing Science Student Society. The bot accepts user input from Discord chat channels and runs a script to execute the command. Commands available include WolframAlpha math functions, grouping users by courses, and admin commands. Valid inputs are processed by the bot and the specific command is executed. The bot then displays the command output to the user. When an invalid input is detected, the bot sends feedback to the user indicating the command does not exist.

TODO: Explain COGS


# Commands: #

## Administrative Commands: ##

These commands are available to moderation and administrative users. Often these are back end commands that allow for the deletion of messages, the locking and unlocking of channels, and the loading and unloading of cogs for the bot.

###.announce <title> <desc>###

Makes an announcement.

Usage: .announce <title> <body>

###.clear <amount>###

Clears set amount of messages above current messages.

Usage: .clear 50

###.clearspam###

Clears the spam.

Usage: .clearspam

###.cogs ###

Lists the currently loaded cogs.

Usage: .cogs

###.exc [args...]###

Execute a bash command

Usage: .exc ls -a

###.load <name> ###

Loads a cog.

Usage: .load Announce

###.lock ###

Locks current channel.

Usage: .lock

###.modsay [msg...]###

Give a stern message (Heavily inspired by brenfan's .em code <3).

Usage: .modsay "This is a stern message."

###.propagateMute ###

Adds the Muted role to every channel, maintaining universal control and ruleset for muted role

Usage: .propagateMute

###.refreshCache ###

Refresh the server wordart cache. 

Usage: .refreshCache

###.reload <name>###

Reloads the cogs.

Usage: .reload Announce
 
###.restrict <user> (not yet implemented)###

Restricts a user from posting in a channel

Usage: .restrict <John Doe>

###.unload <name>###

Unloads a cog.

Usage: .unload Announce

###.unlock###

Unlocks the current channel.

###.unrestrict [msg...] (not yet implemented)###

Undo any restrictions on a user for all channels. 

Usage: !unrestrict [users..]

## Miscellaneous Commands: ##

.allreminders (MISC) 
list all the active reminders. Does not list reminders from remindmein.

.antonym <word> (MISC) 
Return the antonym of a word

.avatart [args...] (MISC)
Make a wordcloud in the shape of your avatar.
usage: .avatart <invert> <bgcolor>

.beep (MISC) Same as ping/pong

.ding (MISC) Same as ping/pong

.doraemon (Shows cat picture) MISC

.eggplant (MISC) Prints "My eggplant brings all the boys to the yard"
And they're like, it's better than yours

.eggwrite [msg...] (MISC) (Only working with letters)
Use the bot to write with eggplant emojis!

.em [desc...] (MISC)
Make an embedded message
Usage: em <body>
Restricted command

.gameR None (NOTHING?) Starts the roulette game

.goodluck (MISC) Shows a photo of a thumbs up eggplant
Wish someone good luck

### .help ###
The help command will display the information menu in the chat. This menu contains brief descriptions of all possible commands, and provides a link to the source code.

### .help mc ###

This can only be used within the #minecraft channel. When the command is used in correct channel, it will display commands specific to minecraft. Outside of the correct channel, it will display a message alerting the user to move to that channel.

.henry (MISC) Posts a photo of people bowing to henry.

.howoldami (MISC) Display when you joined the server

### .iam \<course\> ###
You can use this command to give yourself any roles that already exist, and consists of entirely lowercase letters or numbers. The \<class\> format follows the same rules as the .newclass command shown above. If the role you attempted to join does not exist, it will be created and you will be given it.

.iamn <course> (MISC)
Remove yourself from a discord class/role
Usage: iamn <someclass>

.imgur [word...] Search for a picture on imgur MISC

.impeach Impeach our dear leader (Shows photo of Henry) MISC

.info (MISC) Displays the old minecraft server information

.joke (MISC) Displays a photo of a joke flying over henry's head

.kms Don't (NOTHING?) (Nothing)

.meaning <word> (MISC)
Return the meaning of a word

.myreminders (MISC)
list only user's reminders

.mytop10 (MISC) Displays your top 10 words on the server.

### .newclass \<class\> ###
This command will create a new class role, and give you that role. The name of the role will either be the first word typed after the .newclass command, or will be the entire string between the first quotation marks. An example is shown below. It is also worth noting that all roles created using this command will be converted to lowercase for security reasons.

.newclass <course> (MISC)
Create a new discord class/role
Usage: newclass <someclass>
Creating a class/role places you in that class/role

.newclass one two three = a new role with the name "one."
.newclass "one two three" = a new role with the name "one two three."

.outline [args...] (MISC)
Display an SFU course's outline
Usage: outline <department> <number> (section) (year) (semester)

.ping (MISC) Replys with pong

.playmsg <msg> (MUSIC)
Change minion's playing message
Usage: playing <msg>

.poem [args...] Searches for a poem usage: !poem <title> <author> <length> (PMs you the poem) MISC

.poll [args...] (MISC)
Create an instant poll
Usage: poll <subject> [choices]...
Defaults to yes/no if no choices supplied.

.prettygood (MISC) Photo of a man saying "Heyyyy, that's pretty good"

.remindme [word...] (MISC)
remind the user to do some thing at some time.
usage: !remindme "hang the cat to dry" 2017 8 5
format: year month day [hour] [minute] [second]

.remindmein [word...] (MISC)
usage: remindmein 2 days 'do that thing'

.roads [args...] (MISC)
Display road conditions for SFU
Usage: roads <city>

.search [query...] (MISC)
Search the internet using DuckDuckGo!

.servart (MISC)
Make a wordcloud out of the server's most common words.

.sfu [words...] (MISC)
Lookup an SFU class
usage: !sfu <cmpt120> or !sfu <cmpt> <120>

.status (MISC) (DEAD COMMAND)
Display the number of players on the minecraft server

.stealthegg (MISC) (Puts an eggplant in chat)

.spell <word> Check your spelling MISC

.synonym <word> (MISC)
Return the synonym of a word

.top10 (MISC) Displays the top 10 words on the server.

.translate [args...] (MISC)
Translate a string into a specified language!
usage: !translate <target> (source)
example translate into spanish: <!translate "I like cheese" es>
To specify source language, include a third arg:
!translate "Je suis formé à la guerre de Nerf et j'ai le plus d'étoiles d'or dans toute la classe maternelle." en fr
Supported languages and language codes listed on this webpage
https://cloud.google.com/translate/docs/languages

.triggered When someone has a mildly different opinion. (Shows angry face GIF) MISC

.urban [msg...] (MISC) Queries urban dictionary for the entry you provide
Lookup some jargon from the urban dictionary.

.whois <course> (MISC)
List people in a discord class/role
Usage: whois <someclass>

.wiki [msg...] Look up a subject on wikipedia (MISC)

.wolf [args...] (MISC)
Get wolfram alpha to help with your homework
Usage: wolf <query>

.wordart (MISC)
Make a wordcloud out of your most common words

.youtube [query...] (MUSIC)
Search for a youtube video

## Music Commands: ##

.bump (MUSIC)
vote to bump the indexed song to the front.

.join <channel> (MUSIC) (SIMILAR TO SUMMON)
Joins a voice channel.

.pause (MUSIC)
Pauses the currently played song.

.play <song> (MUSIC)
Plays a song.
If there is a song currently in the queue, then it is
queued until the next song is done playing.
This command automatically searches as well from YouTube.
The list of supported sites can be found here:
https://rg3.github.io/youtube-dl/supportedsites.html

.playing Shows info about the currently played song. MUSIC

.queue (MUSIC)
shows songs in the current queue

.resume (MUSIC)
Resumes the currently played song.

.skip (MUSIC)
Vote to skip a song. The song requester can automatically skip.
3 skip votes are needed for the song to be skipped.

.stop Stops playing audio and leaves the voice channel. This also clears the queue. MUSIC

.summon Summons the bot to join your voice channel. (PLAYS MUSIC IF) MUSIC

.volume <value> Sets the volume of the currently playing song. MUSIC

## Rank Commands: ##

.gexp <user> <amount> (EXP) gives exp to user

.levels (EXP) Shows the list of users by rank

.rank (EXP) Displays your current rank on the server

.stats (EXP) (BROKEN) Shows EXP changes in the past amount of time. 



There are currently 5 commands available, and more commands will be added in future updates.

# How to set up for testing.

Duplicate `botMain.settings.sample` as `botMain.settings`, then add your own discord bot token. Then run the bot using `python3 csss-minion.py test`. The `test` argument skips
loading all cogs and allows anyone to use commands usually restricted to Henry.

You can load any cog you like with `.load <cog>` and list available cogs with `.cogs`.


Source Code
https://github.com/henrymzhao/csss-minion/