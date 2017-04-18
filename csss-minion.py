# py -m pip install -U __
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

configFile = "botMain.settings"

#check if config file exists
if not os.path.isfile(configFile):
    exit("Config file not found")
    

#Load the config file
config = configparser.ConfigParser()
config.read(configFile)

description = config.get("Discord","Description")

bot = commands.Bot(command_prefix='.', description=description)
wolframid = config.get("WolfGram","TokenId")
wClient = wolframalpha.Client(wolframid)

DISCORD_API_ID = config.get("Discord","API_ID")
token = config.get("Discord","Token")
ip = "172.93.48.238:25565"


bot.remove_command("help")
  
server = discord.Server(id=DISCORD_API_ID)
roles = server.roles

def reloadConfig():
    pass

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print('------')

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


bot.run(token)
