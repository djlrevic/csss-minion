import discord  # py -m pip install -U __
import os  # pylint: disable=C
from discord.ext import commands
import configparser
import getpass
import psycopg2
import urllib.parse
import random
import asyncio
import codecs as codex
import math
import time
import subprocess
import sys
from io import StringIO
import logging
from pagination import Pages
configFile = 'botMain.settings'
if (not os.path.isfile(configFile)):
    DISCORD_API_ID = getpass.getpass('Discord API: ')
    token = getpass.getpass('Token: ')
    wolframid = getpass.getpass('Wolframalpha: ')
    ip = '172.93.48.238:25565'  #check if config file exists, if not, input manually
    description = 'Bot of the CSSS'
    postgrespass = getpass.getpass('Database Password: ')
    mashape_key = getpass.getpass('Mashape Key: ')
    local_postgres_pw = getpass.getpass('Database Password: ')
    imgur_id = getpass.getpass('Imgur client id: ')
else:
    config = configparser.ConfigParser()
    config.read(configFile)
    description = config.get('Discord', 'Description')
    wolframid = config.get('Wolfram', 'TokenId')
    DISCORD_API_ID = config.get('Discord', 'API_ID')
    token = config.get('Discord', 'Token')  #Load the config file
    ip = '172.93.48.238:25565'
    postgrespass = config.get('Postgres', 'Password')
    mashape_key = config.get('Mashape', 'Token')
    local_postgres_pw = config.get('LocalPG', 'Password')
    imgur_id = config.get('Imgur', 'client_id')
    bot = commands.Bot(command_prefix='.', description=description)
    bot.wolframid = wolframid
    bot.mcip = ip
    bot.remove_command('help')
    bot.mashape_key = mashape_key
    bot.imgur_id = imgur_id
    bot.lang_url = config.get('Translate', 'url')
    bot.postgrespass = postgrespass

def reloadConfig():
    pass

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print('------')
    # await bot.change_presence(activity=discord.Game(name='Yes my master'))

def levels_loaded():
    return 'Levels' in list(bot.cogs.keys())

@bot.event
async def on_message(message):
    await bot.process_commands(message)

@bot.command()
async def test(ctx):
    print(bot.loop)

@bot.command()
async def load(ctx, name):  # DATABASE OPERATIONS. DISABLE UNLESS ACTUALLY RUNNING AS SERVICE
    if Henry(ctx):  # print(message.author.name+"#"+message.author.discriminator)
        try:
            bot.load_extension(name)
        except (AttributeError, ImportError) as e:
            await ctx.send('Cog load failed: {}, {}'.format(type(e), str(e)))
            return
        await ctx.send('{} cog loaded.'.format(name))
    else:
        await ctx.send("You ain't my master! Shoo!")

@bot.command()
async def unload(ctx, name):
    if Henry(ctx):
        bot.unload_extension(name)
        await ctx.send('{} cog unloaded'.format(name))
    else:
        await ctx.send("You ain't my master! Shoo!")


@bot.command()
async def reload(ctx, name):
    if Henry(ctx):
        bot.unload_extension(name)
        try:
            bot.load_extension(name)
        except (AttributeError, ImportError) as e:
            await ctx.send('Cog load failed: {}, {}'.format(type(e), str(e)))
            return
            await ctx.send('`{} cog reloaded`'.format(name))
        else:
            await ctx.send("`You ain't my master! Shoo!``")

@bot.command()
async def exc(ctx, *args):
    if Henry(ctx):
        query = ' '.join(args)
        await ctx.send(('```' + subprocess.getoutput(query)) + '```')
    else:
        await ctx.send("You ain't my master! Shoo!")


def Henry(ctx):
    if ctx.author.id == 173702138122338305:
        return True
    else:
        return False


async def embed_this_for_me(text, ctx):
    'Standardized embeddings across cogs'
    callingframe = sys._getframe(1)
    em = discord.Embed(colour=4095)
    em.add_field(name='Results from ' + callingframe.f_code.co_name, value=text)
    await ctx.channel.send(embed=em)


def fit_msg(msg, maxlen: int = 2000):
    '''Split a long message to fit within discord's limits.\n      Uses the following order of division for natural splits:\n      newline > space > any char\n '''
    msgs = []  # pulling all members from the server. Disable unless admin using
    while len(msg) >= maxlen:  # @bot.command(pass_context = True)
        if '\n' in msg[:maxlen]:  # async def pull(ctx):
            idx = msg[:maxlen].rfind('\n')  #   members = ctx.message.server.members
            msgs.append(msg[:idx])  #   with codex.open('ids.txt', 'a', 'utf-8') as log:
            msg = msg[idx + 1:]  #       log.write('[')
        elif ' ' in msg[:maxlen]:  #   for i in members:
            idx = msg[:maxlen].rfind(' ')  #     # target.write('{"name" : "')
            msgs.append(msg[:idx])  #     # target.write(i.name)
            msg = msg[idx + 1:]  #     # target.write(', "user_id" : "')
        else:  #     # target.write(i.id)
            for x in range(maxlen, 0, (-1)):  #     # target.write('"}, ')
                msgs.append(msg[:x])  #     name = bytes(i.name, 'utf-8').decode('utf-8', 'ignore')
                msg = msg[x:]  #     with codex.open('ids.txt', 'a', 'utf-8') as log:
                break  #       log.write('{"name" : "' + name + '", "user_id" : "' + i.id + '", "id" : "' + i.discriminator + '"}, ')
    msgs.append(msg)  #   with codex.open('ids.txt', 'a', 'utf-8') as log:
    return msgs  #       log.write(']')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def cogs(ctx):
    '''Lists the currently loaded cogs.'''
    cogs = list(bot.cogs.keys())
    cogs.sort()
    await bot.embed_this_for_me('\n'.join(cogs), ctx)

async def update():
    await bot.wait_until_ready()
    print('ready')

bot.embed_this_for_me = embed_this_for_me
bot.fit_msg = fit_msg
bot.Henry = Henry
bot.loop.create_task(update())  #find last occurance of newline
bot.run(token)
#careful which side gets the newline
