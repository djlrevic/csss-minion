import discord
from discord.ext import commands

description = 'Bot of the CSSS'

bot = commands.Bot(command_prefix='.', description=description)

token = "***REMOVED***"

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def add(left : int, right : int):
    await bot.say(left+right)


bot.run(token)