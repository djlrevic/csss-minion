#pylint: disable=C
import discord
from discord.ext import commands
import datetime
from mcstatus import MinecraftServer
from pagination import Pages

class Info():
    def __init__(self, bot):
        self.bot = bot

    # Voting done, command disabled
    # @commands.command()
    # async def vote():
    #     embed = discord.Embed(colour=discord.Colour(0xdc4643), timestamp=datetime.datetime.utcfromtimestamp(1490339531))

    #     embed.set_thumbnail(url="https://cdn.discordapp.com/app-icons/293110345076047893/15e2a6722723827ff9bd53ca787df959.jpg")
    #     embed.set_author(name="CSSS-Minion", icon_url="https://cdn.discordapp.com/app-icons/293110345076047893/15e2a6722723827ff9bd53ca787df959.jpg")
    #     embed.set_footer(text="CSSS-Minion", icon_url="https://cdn.discordapp.com/app-icons/293110345076047893/15e2a6722723827ff9bd53ca787df959.jpg")

    #     embed.add_field(name="CSSS Voting Information", value="The voting period for the Computing Science Student Society General Elections for the 2017-2018 term begins on Monday March 20th, 2017 at 11:59 PM and closes on Monday March 27th, 2017 at 11:59 PM. \n\nVisit https://www.sfu.ca/~pjalali/speeches.html to view candidate speeches, and http://websurvey.sfu.ca/survey/273372327 to vote.")

    #     await bot.say(embed=embed)

    @commands.command(pass_context = True)
    async def voteresult(self, ctx):
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

            await self.bot.say(embed=embed)    

    @commands.group(pass_context = True)
    async def help(self, ctx):

        if ctx.invoked_subcommand is None:
            items = []
            items.append([".help", "Displays this help menu."])
            items.append([".newclass <class>", "Start a new class group. Great for notifying everyone in that particular class."])
            items.append([".iam <class>", "Places yourself in an existing class."])
            items.append([".wolf <query>", "Asks WolframAlpha a question! Wrap your questions in \"quotes\"!"])
            # items.append([".vote", "Find voting details for the CSSS Exec election!."])
            items.append([".voteresult", "Find out the winners of the CSSS annual election!"])
            items.append([".help mc", "Displays commands for the CSSS Minecraft server. Only usable within #minecraft"])
            items.append([".gameR help", "Displays commands for the for the Roullette game"])
            items.append([".meaning <word>", "Display the meaning of an english word"])
            items.append([".synonym <word>", "Display synonyms for an english word"])
            items.append([".antonym <word>", "Display antonyms for an english word"])
            items.append([".spell <word>", "Check the spelling of an english word"])
            items.append([".poem <title> <author>", "Retrieve a poem from the poem database"])
            items.append([".wiki <query>", "Retrieve summary of a wikipedia article"])
            items.append([".wordart", "Make a wordcloud out of your common words"])
            items.append([".avatart <invert> <colour>", "Turn your avatar into a wordcloud!"])
            items.append(["Source Code", "https://github.com/henrymzhao/csss-minion/"])

            p = Pages(self.bot, message = ctx.message, entries = items, per_page = 4)
            p.embed = discord.Embed(title="CSSS-Minion Commands", colour=discord.Colour(0xdc4643), timestamp=datetime.datetime.utcfromtimestamp(1490339531))
            p.embed.set_thumbnail(url="https://cdn.discordapp.com/app-icons/293110345076047893/15e2a6722723827ff9bd53ca787df959.jpg")
            p.embed.set_author(name="CSSS-Minion", icon_url="https://cdn.discordapp.com/app-icons/293110345076047893/15e2a6722723827ff9bd53ca787df959.jpg")
            p.embed.set_footer(text="CSSS-Minion", icon_url="https://cdn.discordapp.com/app-icons/293110345076047893/15e2a6722723827ff9bd53ca787df959.jpg")

            await p.paginate()

            # await self.bot.say(embed=embed)

    @help.command(pass_context = True)
    async def mc(self, ctx):
        if ctx.message.channel.name != "minecraft":
            await self.bot.say("Please move to #minecraft for this command.")
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
            await self.bot.say(embed=embed)

    @commands.command(pass_context = True)
    async def status(self, ctx):
        if ctx.message.channel.name != "minecraft":
            await self.bot.say("Please move to #minecraft for this command.")
        else: 
            server = MinecraftServer.lookup(self.bot.mcip)
            try:
                status = server.status()
            except IOError as e:
                await self.bot.say("It's dead Jim.")
            # try:
            #     query = server.query()
            # except Sock as e:
            #     await bot.say("Server too slow for query!")
            em = discord.Embed(title='CSSS FTB Server Status', description=
            """The server has {0} players and replied in {1} ms.\n""".format(status.players.online, status.latency), colour=0x3D85C6 )
            # + "\n{} are currently online.".format(", ".join(query.players.names)), colour=0x3D85C6)
            await self.bot.send_message(ctx.message.channel, embed=em)

    @commands.command(pass_context = True)
    async def info(self, ctx):
        if ctx.message.channel.name != "minecraft":
            await self.bot.say("Please move to #minecraft for this command.")
        else:    
            em = discord.Embed(title='CSSS FTB Server Information', description="""IP: 172.93.48.238
    Modpack: FTBBeyond 1.5.3
    Minecraft: 1.10.2
    Cracked: YES
    See pinned message to download cracked client.""", colour=0x3D85C6)
            await self.bot.send_message(ctx.message.channel, embed=em)

def setup(bot):
    bot.add_cog(Info(bot))
