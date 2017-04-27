# py -m pip install -U __
# pylint: disable=C
import discord
import os
# import sympy
from discord.ext import commands
# from sympy import *
import wolframalpha
from mcstatus import MinecraftServer
import datetime
import configparser
import getpass
import psycopg2
import urllib.parse
import random
import time
import asyncio
import codecs as codex
import math

configFile = "botMain.settings"
database = "experience" #database name used for exp

#check if config file exists, if not, input manually
if not os.path.isfile(configFile):
    DISCORD_API_ID = getpass.getpass('Discord API: ')
    token = getpass.getpass('Token: ')
    wolframid = getpass.getpass('Wolframalpha: ')
    ip = "172.93.48.238:25565"
    description = "Bot of the CSSS"
    postgrespass = getpass.getpass('Database Password: ')
else:
    #Load the config file
    config = configparser.ConfigParser()
    config.read(configFile)
    description = config.get("Discord", "Description")
    wolframid = config.get("Wolfram", "TokenId")
    DISCORD_API_ID = config.get("Discord", "API_ID")
    token = config.get("Discord", "Token")
    ip = "172.93.48.238:25565"
    postgrespass = config.get("Postgres", "Password")

# SQL SETUP------------------------------------------------------------------------------
urllib.parse.uses_netloc.append("postgres")
conn = psycopg2.connect("port='5432' user='zocnciwk' host='tantor.db.elephantsql.com' password='"+postgrespass+"'")
cur = conn.cursor()
# SQL SETUP------------------------------------------------------------------------------

# conn.close()
# conn = psycopg2.connect("port='5432' user='zocnciwk' host='tantor.db.elephantsql.com' password='"+postgrespass+"'")
# cur = conn.cursor()

bot = commands.Bot(command_prefix='.', description=description)
if os.path.isfile(configFile):
    bot.config = configparser.ConfigParser()
# else:
#     bot
bot.remove_command("help")
  
server = discord.Server(id=DISCORD_API_ID)

def reloadConfig():
    pass

# creating a 2D empty array for exp queues
qu = []
global expTable
expTable = []

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print('------')
    await bot.change_presence(game=discord.Game(name='Yes my master'))
    global expTable 
    expTable = getLevel() #pulling exp templates

@bot.event
async def on_message(message):
    # DATABASE OPERATIONS. DISABLE UNLESS ACTUALLY RUNNING AS SERVICE
    print(message.author.name+"#"+message.author.discriminator)
    if validate(message):
        await add(message)
    await bot.process_commands(message)

startup_extensions = ["classes", "misc"]

@bot.command()
async def loadExt(name):
    try: 
        bot.load_extension(name)
    except(AttributeError, ImportError) as e:
        await bot.say("Cog load failed: {}, {}".format(type(e), str(e)))
        return
    await bot.say("{} cog loaded.".format(name))

@bot.command()
async def unload(name):
    bot.unload_extension(name)
    await bot.say("{} cog unloaded".format(name))

# pulling all members from the server. Disable unless admin using
# @bot.command(pass_context = True)
# async def pull(ctx):
#     members = ctx.message.server.members
#     with codex.open('ids.txt', 'a', 'utf-8') as log:
#             log.write('[')
#     for i in members:
#         # target.write('{"name" : "')
#         # target.write(i.name)
#         # target.write(', "user_id" : "')
#         # target.write(i.id)
#         # target.write('"}, ')
#         name = bytes(i.name, 'utf-8').decode('utf-8', 'ignore')
#         with codex.open('ids.txt', 'a', 'utf-8') as log:
#             log.write('{"name" : "' + name + '", "user_id" : "' + i.id + '", "id" : "' + i.discriminator + '"}, ')
#     with codex.open('ids.txt', 'a', 'utf-8') as log:
#             log.write(']')

# handle 60 second cooldown timer for exp gain
def validate(message):
    # check if user is in queue
    flag = False
    for i in qu:
        if i[0] == message.author.id:
            # user already in queue
            flag = True
    if flag == True:
        print("dupe found")
        return False
    # user not in queue
    qu.append([message.author.id, time.time()])
    print("added to array")
    return True

# formula used to calculate exact experience needed for next level
def calcLevel(x):
    return 5*math.pow(x, 2) + 40*x + 55

# used to update the queue
async def update():
    await bot.wait_until_ready()
    print("ready")
    while not bot.is_closed:        
        for i, item in enumerate(qu):
            if time.time() - item[1] >= 5:
                print("entry expired")
                del qu[i]
        await asyncio.sleep(1)

# handles adding new users and updating existing user exp to database
async def add(message):
    # check if user is in database
    cur.execute("SELECT * FROM "+database+" WHERE user_id = (%s)", (str(message.author.id),))
    entry = cur.fetchone()
    if entry == None:
        # user not in database
        cur.execute("INSERT INTO "+database+" (name, user_id, exp) VALUES (%s, %s, %s)", 
            (message.author.name, str(message.author.id), random.randint(15, 25), ))
        conn.commit()
    else:
        list(entry)
        # user in database
        changeInExp = random.randint(15, 25)
        if updateLevel(changeInExp, entry[3], entry[4]) == True:
            # user has leveled up, perform special operations
            cur.execute("UPDATE "+database+" SET level = {} WHERE user_id = {}".format(userLevel(changeInExp+entry[3]), message.author.id))
            await bot.send_message(message.channel, "<@"+str(message.author.id)+"> is now level **"+str(userLevel(entry[3]+changeInExp))+"**!")
        # else user has not leveled, just add exp
        cur.execute("UPDATE "+database+" SET exp = exp+(%s) WHERE user_id = (%s)", (changeInExp, int(message.author.id), ))
        cur.execute("UPDATE experience E SET level = (SELECT MAX(T.level) FROM template T, experience E1 WHERE T.exp <= E1.exp AND E.user_id = E1.user_id)")
        conn.commit()

# used to pull template levels and exp goals from db
def getLevel():
    cur.execute("SELECT level, exp FROM template ORDER BY level")
    i = 0
    table = []
    stop = False
    while stop == False:
        temp = cur.fetchone()
        if temp == None:
            stop = True
        else:
            table.append(temp)
            i = i+1
    return table

# used to find the current level of user given experience
def userLevel(experience):
    global expTable
    print(expTable[5][1])
    lowerBound = 0
    upperBound = 0
    for foo in expTable:
        if experience > foo[1]:
            lowerBound = foo[0]
        if experience < foo[1]:
            upperBound = foo[0]
    return lowerBound
    

# detect if user is eligible for the next level
def updateLevel(change, experience, currLevel):
    print("Experience : {} and Change : {}".format(experience, change))
    print("CurrLevel: {}".format(currLevel))
    foo = change + experience
    print("foo : {}".format(foo))
    afterChange = userLevel(foo)
    print("afterChange : {}".format(afterChange))
    if afterChange != currLevel:
        return True
    return False  

@bot.command(pass_context = True)
async def rank(ctx):
    cur.execute("SELECT exp FROM experience WHERE user_id = {}".format(ctx.message.author.id))
    msg = cur.fetchone()
    await bot.say(msg)  



# Voting done, command disabled
# @bot.command()
# async def vote():
#     embed = discord.Embed(colour=discord.Colour(0xdc4643), timestamp=datetime.datetime.utcfromtimestamp(1490339531))

#     embed.set_thumbnail(url="https://cdn.discordapp.com/app-icons/293110345076047893/15e2a6722723827ff9bd53ca787df959.jpg")
#     embed.set_author(name="CSSS-Minion", icon_url="https://cdn.discordapp.com/app-icons/293110345076047893/15e2a6722723827ff9bd53ca787df959.jpg")
#     embed.set_footer(text="CSSS-Minion", icon_url="https://cdn.discordapp.com/app-icons/293110345076047893/15e2a6722723827ff9bd53ca787df959.jpg")

#     embed.add_field(name="CSSS Voting Information", value="The voting period for the Computing Science Student Society General Elections for the 2017-2018 term begins on Monday March 20th, 2017 at 11:59 PM and closes on Monday March 27th, 2017 at 11:59 PM. \n\nVisit https://www.sfu.ca/~pjalali/speeches.html to view candidate speeches, and http://websurvey.sfu.ca/survey/273372327 to vote.")

#     await bot.say(embed=embed)

@bot.command(pass_context = True)
async def voteresult(ctx):
    if ctx.invoked_subcommand is None:
        embed = discord.Embed(title="CSSS Exec Positions", colour=discord.Colour(0xdc4643), timestamp=datetime.datetime.utcfromtimestamp(1490339531))

        embed.set_thumbnail(url="https://cdn.discordapp.com/app-icons/293110345076047893/15e2a6722723827ff9bd53ca787df959.jpg")
        embed.set_author(name="CSSS-Minion", icon_url="https://cdn.discordapp.com/app-icons/293110345076047893/15e2a6722723827ff9bd53ca787df959.jpg")
        embed.set_footer(text="CSSS-Minion", icon_url="https://cdn.discordapp.com/app-icons/293110345076047893/15e2a6722723827ff9bd53ca787df959.jpg")

        embed.add_field(name="President", value="David Miiller")
        embed.add_field(name="Vice President", value="Jon Loewen")
        embed.add_field(name="Treasurer", value="Dustin Cao")
        embed.add_field(name="Director of Resources", value="Kiarash Mirsalehi")
        embed.add_field(name="Director of Events", value="Brendan Chan")
        embed.add_field(name="Director of Communications", value="Henry Zhao")
        embed.add_field(name="Director of Archives", value="Josh Wu")
        embed.add_field(name="Source Code", value="https://github.com/henrymzhao/csss-minion/")

        await bot.say(embed=embed)    

@bot.group(pass_context = True)
async def help(ctx):

    if ctx.invoked_subcommand is None:
        embed = discord.Embed(title="CSSS-Minion Commands", colour=discord.Colour(0xdc4643), timestamp=datetime.datetime.utcfromtimestamp(1490339531))

        embed.set_thumbnail(url="https://cdn.discordapp.com/app-icons/293110345076047893/15e2a6722723827ff9bd53ca787df959.jpg")
        embed.set_author(name="CSSS-Minion", icon_url="https://cdn.discordapp.com/app-icons/293110345076047893/15e2a6722723827ff9bd53ca787df959.jpg")
        embed.set_footer(text="CSSS-Minion", icon_url="https://cdn.discordapp.com/app-icons/293110345076047893/15e2a6722723827ff9bd53ca787df959.jpg")

        embed.add_field(name=".help", value="Displays this help menu.")
        embed.add_field(name=".newclass <class>", value="Start a new class group. Great for notifying everyone in that particular class.")
        embed.add_field(name=".iam <class>", value="Places yourself in an existing class.")
        embed.add_field(name=".wolf <query>", value="Asks WolframAlpha a question! Wrap your questions in \"quotes\"!")
        # embed.add_field(name=".vote", value="Find voting details for the CSSS Exec election!.")
        embed.add_field(name=".voteresult", value="Find out the winners of the CSSS annual election!")
        embed.add_field(name=".help mc", value="Displays commands for the CSSS Minecraft server. Only usable within #minecraft")
        embed.add_field(name="Source Code", value="https://github.com/henrymzhao/csss-minion/")

        await bot.say(embed=embed)

@help.command(pass_context = True)
async def mc(ctx):
    if ctx.message.channel.name != "minecraft":
        await bot.say("Please move to #minecraft for this command.")
    else:
        embed = discord.Embed(title="CSSS-Minion Minecraft Commands", colour=discord.Colour(
            0xdc4643), timestamp=datetime.datetime.utcfromtimestamp(1490339531))
        embed.set_thumbnail(
            url="https://media-elerium.cursecdn.com/avatars/13/940/635581309636616244.png")
        embed.set_author(
            name="CSSS-Minion", icon_url="https://cdn.discordapp.com/app-icons/293110345076047893/15e2a6722723827ff9bd53ca787df959.jpg")
        embed.set_footer(
            text="CSSS-Minion", icon_url="https://s-media-cache-ak0.pinimg.com/originals/aa/65/70/aa657074a12fb0d961a1789c671b73e3.jpg")
        embed.add_field(name=".help mc", value="Displays this help menu.\n")
        embed.add_field(name=".status", value="Displays the current server status.\n")
        embed.add_field(name=".info", value="Information about how to connect to server.\n")
        await bot.say(embed=embed)

@bot.command(pass_context = True)
async def status(ctx):
    if ctx.message.channel.name != "minecraft":
        await bot.say("Please move to #minecraft for this command.")
    else: 
        server = MinecraftServer.lookup(ip)
        try:
            status = server.status()
        except IOError as e:
            await bot.say("It's dead Jim.")
        # try:
        #     query = server.query()
        # except Sock as e:
        #     await bot.say("Server too slow for query!")
        em = discord.Embed(title='CSSS FTB Server Status', description=
        """The server has {0} players and replied in {1} ms.\n""".format(status.players.online, status.latency), colour=0x3D85C6 )
        # + "\n{} are currently online.".format(", ".join(query.players.names)), colour=0x3D85C6)
        await bot.send_message(ctx.message.channel, embed=em)

@bot.command(pass_context = True)
async def info(ctx):
    if ctx.message.channel.name != "minecraft":
        await bot.say("Please move to #minecraft for this command.")
    else:    
        em = discord.Embed(title='CSSS FTB Server Information', description="""IP: 172.93.48.238
Modpack: FTBBeyond 1.5.3
Minecraft: 1.10.2
Cracked: YES
See pinned message to download cracked client.""", colour=0x3D85C6)
        await bot.send_message(ctx.message.channel, embed=em)

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

bot.loop.create_task(update())
bot.run(token)
