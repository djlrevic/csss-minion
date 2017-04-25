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

configFile = "botMain.settings"

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
    wolframid = config.get("WolfGram", "TokenId")
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

wClient = wolframalpha.Client(wolframid)
bot = commands.Bot(command_prefix='.', description=description)
bot.remove_command("help")
  
server = discord.Server(id=DISCORD_API_ID)

def reloadConfig():
    pass

# creating a 2D empty array for exp queues
qu = []

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print('------')
    await bot.change_presence(game=discord.Game(name='Yes my master'))

@bot.event
async def on_message(message):
    print(message.author.name+"#"+message.author.id)
    if validate(message):
        await add(message)
    await bot.process_commands(message)

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

# used to update the queue
async def update():
    await bot.wait_until_ready()
    print("ready")
    while not bot.is_closed:        
        for i, item in enumerate(qu):
            if time.time() - item[1] >= 60:
                print("entry expired")
                del qu[i]
        await asyncio.sleep(1)

# handles adding new users and updating existing user exp to database
async def add(message):
    # check if user is in database
    cur.execute("SELECT * FROM experience WHERE user_id = (%s)", (int(message.author.id),))
    entry = cur.fetchone()
    if entry == None:
        # user not in database
        cur.execute("INSERT INTO experience (name, user_id, exp) VALUES (%s, %s, %s)", 
            (message.author.name, int(message.author.id), random.randint(15, 25), ))
        conn.commit()
    else:
        # user in database
        cur.execute("UPDATE experience SET exp = exp+(%s) WHERE user_id = (%s)", (random.randint(15, 25), int(message.author.id), ))
        conn.commit()


@bot.command(pass_context=True)
async def howoldami(ctx):
    await bot.say(ctx.message.author.joined_at)

@bot.command(pass_context=True)
async def poll(ctx, *args):
    if len(args) == 0:
        # no question
        await bot.say("Give me a question!")
    elif len(args) > 9:
        # too many options
        await bot.say("Too many choices yo!")
    elif len(args) == 1:
        # just the question itself, hence by default assume y/n true/false
        question = await bot.say("Question: **"+ args[0] + "** (Y/N).")
        await bot.add_reaction(question, '👍')
        await bot.add_reaction(question, '👎')
        # await bot.add_reaction(question, '1\U000020e3') #example with unicode
    else:
        # actual question with choices
        print(len(args))
        choice = [0] * (len(args)-1)
        # creating individual options
        for i in range(1, len(args)):
            choice[i-1] = str(i)+". "+str(args[i])
        question = await bot.say("Question: **" + args[0] + "**" + "\n" + "\n".join(choice)) #use join to display array of strings in a list
        for i in range(1, len(args)):
            await bot.add_reaction(question, str(i)+'\U000020e3')

@bot.command()
async def play(msg):
    await bot.change_presence(game = discord.Game(name=msg))

@bot.command(pass_context = True)
async def iam(ctx, course : str):
    course = course.lower()
    found = 0
    for i in range(0, len(ctx.message.server.roles)):
        if course == ctx.message.server.roles[i].name:
            found = i
    if found == 0:
        await bot.say("This class doesn't exist. Try creating it with .newclass name")
    else:
        await bot.add_roles(ctx.message.author, ctx.message.server.roles[found])
        await bot.say("You've been placed in "+ course)

# Remove user from role
@bot.command(pass_context = True)
async def iamn(ctx, course : str):
    course = course.lower()
    found = 0
    for i in range(0, len(ctx.message.author.roles)):
        if course == ctx.message.author.roles[i].name:
            found = i
    if found == 0:
        await bot.say("You are not currently in this class.")
    else:
        await bot.remove_roles(ctx.message.author, ctx.message.author.roles[found])
        await bot.say("You've been removed from " + course)

@bot.command(pass_context = True)
async def newclass(ctx, course):
    course = course.lower()
    dupe = False
    for j in range(0, len(ctx.message.server.roles)):
        if ctx.message.server.roles[j].name == course:
            dupe = True
    if dupe == True:
        await bot.say("Class already exists")    
    else:
        # temp value
        flag = True
        # temp value

        # flag = False
        # for i in range(0, len(ctx.message.author.roles)):
        #     if ctx.message.author.roles[i].name == "Regular":
        #         flag = True
        if flag == True:
            newRole = await bot.create_role(server, name = course, mentionable = True)# , hoist = True)
            await bot.add_roles(ctx.message.author, newRole)
            await bot.say(course+" class has been created. You have been placed in it.")
        else:
            await bot.say("You need to be level 10 and above to create classes! My master said this is to reduce spam.")

# @bot.command()
# async def calc(equation : str):
#     await bot.say("``"+sympify+(equation)+"``")
       
@bot.command()
async def wolf(query : str):
    res = wClient.query(query)
    try:
        await bot.say("```"+(next(res.results).text)+"```")
    except AttributeError:
        await bot.say("I ain't found shit.")

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

bot.loop.create_task(update())
bot.run(token)
