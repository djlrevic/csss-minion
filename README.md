# csss-minion

# Information: #

The csss-minion bot is maintained by Henry Zhou (henrymzhou) using Python 3 and discord.py for SFU's Computing Science Student Society. The bot accepts user input from Discord chat channels and runs a script to execute the command. Commands available include WolframAlpha math functions, Google Translate functionality, and administrative commands. Valid inputs are processed by the bot and the specific command is executed. The bot then displays the command output to the user. When an invalid input is detected, the bot sends feedback to the user indicating the command does not exist.

This bot supports ranks by giving users EXP every time they participate in chat. There are also custom ranks that users can place themselves in to add themselves to classes, allowing a user to find other students in their classes. 

The bot also supports audio playback of music, which can be added from any YouTube video. 

A user can add a "cog", which is a additional file that has custom implementation to expand the use of the bot. The bot has built-in load and unloading of cogs available through its commands.

[A complete list of commands](COMMANDS.md)
A list can also be found using the `.help` command.

This bot is covered under the GPL-2.0 License.

# Bot Setup: #

Duplicate `botMain.settings.sample` as `botMain.settings` and add your own discord bot token. Afterwards, run the bot using `python3 csss-minion.py test`. The `test` argument skips
loading all cogs and allows anyone to use commands usually restricted to Henry.

Loading any cog is possible with `.load <cog>`, and listing available cogs can be done with `.cogs`.

The bot's `.help` command will list all the currently implemented commands, listed in greater detail below.

Source Code
https://github.com/henrymzhao/csss-minion/
