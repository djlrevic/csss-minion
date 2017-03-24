# py -m pip install -U __
import discord
# import sympy
from discord.ext import commands
# from sympy import *
import wolframalpha
from mcstatus import MinecraftServer

description = 'Bot of the CSSS'

bot = commands.Bot(command_prefix='.', description=description)
wolframid = 'J9E82A-53G2L78JKQ'
wClient = wolframalpha.Client(wolframid)

bot.remove_command("help")

token = ""
with open("token.txt") as f:
    for line in f:
        DISCORD_API_ID = line
        token = line

server = discord.Server(id=DISCORD_API_ID)
roles = server.roles

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print('------')

# @bot.command()
# async def add(number1 : int, number2 : int):
#     await bot.say(number1+number2)

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

@bot.command()
async def vote():
    await bot.say(
    """```The voting period for the Computing Science Student Society General Elections for the 2017-2018 term begins on Monday March 20th, 2017 at 11:59 PM and closes on Monday March 27th, 2017 at 11:59 PM.\n\nVisit https://www.sfu.ca/~pjalali/speeches.html to view candidate speeches, and http://websurvey.sfu.ca/survey/273372327 to vote.```""")

@bot.command()
async def help():
    await bot.say(

        """```I am the minion of the CSSS, here's what I can do:\n\n
        .help               
            -   bring up this message
        .newclass <class>   
            -   Start a new class group. Great for notifying everyone in that class
        .iam <class>        
            -   Place yourself in an existing class
        .wolf <query>       
            -   Asks WolframAlpha a question! 
            -   Make sure to wrap your entire question in quotation marks
        .vote               
            -   Find voting details for the CSSS exec election!
        
Questions? @henrymzhao to find out more.
        
My code can be found here: https://github.com/henrymzhao/csss-minion```
        """
    )

@bot.command(pass_context = True)
async def status(ctx):
    server = MinecraftServer.lookup("172.93.48.238:25565")
    status = server.status()
    query = server.query()
    em = discord.Embed(title='CSSS FTB Server Status', description=
    """The server has {0} players and replied in {1} ms.\n""".format(status.players.online, status.latency) + "\n{} are currently online.".format(", ".join(query.players.names)), colour=0x3D85C6)
    await bot.send_message(ctx.message.channel, embed=em)

@bot.command(pass_context = True)
async def info(ctx):
    em = discord.Embed(title='CSSS FTB Server Information', description="""IP: 172.93.48.238
Modpack: Direwolf20 v1.10.0
Minecraft: 1.7.10
Cracked: NO (working on it)""", colour=0x3D85C6)
    await bot.send_message(ctx.message.channel, embed=em)

bot.run(token)