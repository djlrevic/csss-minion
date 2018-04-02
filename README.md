# csss-minion


The csss-minion bot is programmed by Henry Zhou (henrymzhou) using Python 3 and discord.py for SFU's Computing Science Student Society. The bot accepts user input from Discord chat channels and runs a script to execute the command. Commands available include WolframAlpha math functions, grouping users by courses, and admin commands. Valid inputs are processed by the bot and the specific command is executed. The bot then displays the command output to the user. When an invalid input is detected, the bot sends feedback to the user indicating the command does not exist.


# Commands: #

There are currently 5 commands available, and more commands will be added in future updates.  

-## .help ##
The help command will display the information menu in the chat. This menu contains brief descriptions of all possible commands, and provides a link to the source code.

## .newclass \<class\> ##
This command will create a new class role, and give you that role. The name of the role will either be the first word typed after the .newclass command, or will be the entire string between the first quotation marks. An example is shown below. It is also worth noting that all roles created using this command will be converted to lowercase for security reasons.

.newclass one two three = a new role with the name "one."
.newclass "one two three" = a new role with the name "one two three."

## .iam \<course\> ##
You can use this command to give yourself any roles that already exist, and consists of entirely lowercase letters or numbers. The \<class\> format follows the same rules as the .newclass command shown above. If the role you attempted to join does not exist, it will be created and you will be given it.

## .voteresult ##
Voteresult is used to display the winners of the CSSS annual election. It contains information about the following elected positions: President, Vice President, Treasurer, Director of Resources, Director of Events, Director of Communications, and Director of Archives.

## .help mc ##

This can only be used within the #minecraft channel. When the command is used in correct channel, it will display commands specific to minecraft. Outside of the correct channel, it will display a message alerting the user to move to that channel.

# How to set up for testing.

Duplicate `botMain.settings.sample` as `botMain.settings`, then add your own discord bot token. Then run the bot using `python3 csss-minion.py test`. The `test` argument skips
loading all cogs and allows anyone to use commands usually restricted to Henry.

You can load any cog you like with `.load <cog>` and list available cogs with `.cogs`.


ADD:

imgur [word...] Search for a picture on imgur MISC

.propagateMute ?????

.playing Shows info about the currently played song. MUSIC

.volume <value> Sets the volume of the currently playing song. MUSIC

.doraemon (Shows cat picture) MISC

.spell <word> Check your spelling MUSIC

.reload <name> None??? (ADMIN)

.triggered When someone has a mildly different opinion. (Shows angry face GIF) MISC

.impeach Impeach our dear leader (Shows photo of Henry) MISC

.poem [args...] Searches for a poem usage: !poem <title> <author> <length> (PMs you the poem) MISC

.summon Summons the bot to join your voice channel. (PLAYS MUSIC IF) MUSIC

.stop Stops playing audio and leaves the voice channel. This also clears the queue. MUSIC

.unload <name> None ???? (ADMIN)

.gameR None (NOTHING?)

.kms Don't (NOTHING?)

.wiki [msg...] Look up a subject on wikipedia (MISC)

.restrict None (ADMIN)

.unrestrict [msg...] Undo any restrictions on a user for all channels. Usage: !unrestrict [users..] (ADMIN)

.announce <title> <desc> 
Make an announcement
Usage: announce <title> <body>
Restricted command

.mytop10 (MISC) Displays your top 10 words on the server.

.ping (MISC) Replys with pong

.queue (MUSIC)
shows songs in the current queue

.joke (MISC) Displays a photo of a joke flying over henry's head

.urban [msg...] (MISC) Queries urban dictionary for the entry you provide
Lookup some jargon from the urban dictionary.

.eggwrite [msg...] (MISC) (Only working with letters)
Use the bot to write with eggplant emojis!

.ding (MISC) Same as ping/pong

.gexp <user> <amount> (EXP) gives exp to user

.antonym <word> (MISC) 
Return the antonym of a word

.avatart [args...] (MISC)
Make a wordcloud in the shape of your avatar.
usage: .avatart <invert> <bgcolor>

.refreshCache 
Refresh the server wordart cache. Admin only.

.levels (EXP) Shows the list of users by rank

.beep (MISC) Same ass ping/pong

.goodluck (MISC) Shows a photo of a thumbs up eggplant
Wish someone good luck

.prettygood (MISC) Photo of a man saying "Heyyyy, that's pretty good"

.join <channel> (MUSIC) (SIMILAR TO SUMMON)
Joins a voice channel.

.poll [args...] (MISC)
Create an instant poll
Usage: poll <subject> [choices]...
Defaults to yes/no if no choices supplied.

.iamn <course> (MISC)
Remove yourself from a discord class/role
Usage: iamn <someclass>

.wolf [args...] (MISC)
Get wolfram alpha to help with your homework
Usage: wolf <query>

.stats (EXP) (BROKEN) Shows EXP changes in the past amount of time. ?????????????????????

.remindme [word...] (MISC)
remind the user to do some thing at some time.
usage: !remindme "hang the cat to dry" 2017 8 5
format: year month day [hour] [minute] [second]

.resume (MUSIC)
Resumes the currently played song.

.status (MISC) (DEAD COMMAND)
Display the number of players on the minecraft server

.modsay [msg...] (ADMIN)
Give a stern message.
Heavily inspired by brenfan's .em code <3

.synonym <word> (MISC)
Return the synonym of a word

.em [desc...] (MISC)
Make an embedded message
Usage: em <body>
Restricted command

.playmsg <msg> (???)
Change minion's playing message
Usage: playing <msg>

.servart (MISC)
Make a wordcloud out of the server's most common words.

.whois <course> 
List people in a discord class/role
Usage: whois <someclass>

.translate [args...]
Translate a string into a specified language!
usage: !translate <target> (source)
example translate into spanish: <!translate "I like cheese" es>
To specify source language, include a third arg:
!translate "Je suis formé à la guerre de Nerf et j'ai le plus d'étoiles d'or dans toute la classe maternelle." en fr
Supported languages and language codes listed on this webpage
https://cloud.google.com/translate/docs/languages

.allreminders (MISC) 
list all the active reminders. Does not list reminders from remindmein.

.stealthegg (MISC) (Puts an eggplant in chat)

.bump (MUSIC)
vote to bump the indexed song to the front.

.remindmein [word...] (MISC)
usage: remindmein 2 days 'do that thing'

.search [query...] (MISC)
Search the internet using DuckDuckGo!

.exc [args...] (ADMIN) ???

.outline [args...] (MISC)
Display an SFU course's outline
Usage: outline <department> <number> (section) (year) (semester)

.wordart (MISC)
Make a wordcloud out of your most common words

.load <name> (ADMIN) ???

.sfu [words...] (MISC)
Lookup an SFU class
usage: !sfu <cmpt120> or !sfu <cmpt> <120>

.rank (EXP) Displays your current rank on the server

.roads [args...] (MISC)
Display road conditions for SFU
Usage: roads <city>

.top10 (MISC) Displays the top 10 words on the server.

.skip (MUSIC)
Vote to skip a song. The song requester can automatically skip.
3 skip votes are needed for the song to be skipped.

.youtube [query...] (MUSIC)
Search for a youtube video

.unlock (ADMIN)
Unlocks the current channel.

.pause (MUSIC)
Pauses the currently played song.

.clear <amount> (ADMIN) (BROKEN)
Clear set amount of messages

.eggplant (MISC) Prints "My eggplant brings all the boys to the yard"
And they're like, it's better than yours

.henry (MISC) Posts a photo of people bowing to henry.

.info (MISC) Displays the old minecraft server information

.cogs (ADMIN)
Lists the currently loaded cogs.

.newclass <course> (MISC)
Create a new discord class/role
Usage: newclass <someclass>
Creating a class/role places you in that class/role

.meaning <word> (MISC)
Return the meaning of a word

.play <song> (MUSIC)
Plays a song.
If there is a song currently in the queue, then it is
queued until the next song is done playing.
This command automatically searches as well from YouTube.
The list of supported sites can be found here:
https://rg3.github.io/youtube-dl/supportedsites.html

.myreminders (MISC)
list only user's reminders

.clearspam (ADMIN) Clears the spam (BROKEN)?

.howoldami (MISC) Display when you joined the server

Source Code
https://github.com/henrymzhao/csss-minion/