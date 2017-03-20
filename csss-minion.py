import discord
from discord.ext import commands

description = 'Bot of the CSSS'

bot = commands.Bot(command_prefix='.', description=description)

token = "***REMOVED***"
DISCORD_API_ID = '***REMOVED***'

# server = discord.utils.get(self.bot.guilds, id = DISCORD_API_ID)
# channel = discord.utils.get(server.text_channels, id = DISCORD_API_ID)
server = discord.Server(id=DISCORD_API_ID)
roles = server.role_hierarchy

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def add(left : int, right : int):
    await bot.say(left+right)

@bot.command(pass_context = True)
async def iam(ctx, entry : str):
    # print(discord.Role(name="exec"))
    # await bot.add_roles(ctx.message.author, )

@bot.command(pass_context = True)
async def newclass(ctx, entry):
    flag = False
    for i in range(0, len(ctx.message.author.roles)):
        if ctx.message.author.roles[i].name == "Regular":
            flag = True
    if flag == True:
       newRole = await bot.create_role(server, name = entry)
       await bot.add_roles(ctx.message.author, newRole)
       await bot.say(entry+" class has been created")

bot.run(token)