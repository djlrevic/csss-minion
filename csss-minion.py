import discord
from discord.ext import commands

description = 'Bot of the CSSS'

bot = commands.Bot(command_prefix='.', description=description)

token = "***REMOVED***"
DISCORD_API_ID = '***REMOVED***'

# server = discord.utils.get(self.bot.guilds, id = DISCORD_API_ID)
# channel = discord.utils.get(server.text_channels, id = DISCORD_API_ID)
server = discord.Server(id=DISCORD_API_ID)
roles = server.roles

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def add(number1 : int, number2 : int):
    await bot.say(number1+number2)

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
            newRole = await bot.create_role(server, name = course, mentionable = True, hoist = True)
            await bot.add_roles(ctx.message.author, newRole)
            await bot.say(course+" class has been created. You have been placed in it.")
       
bot.run(token)