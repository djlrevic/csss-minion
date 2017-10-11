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

    # @commands.command(pass_context = True)
    # async def voteresult(self, ctx):
    #     """Return the voting results from the previous CSSS election."""
    #     if ctx.invoked_subcommand is None:
    #         embed = discord.Embed(title="CSSS Exec Positions", colour=discord.Colour(0xdc4643), timestamp=datetime.datetime.utcfromtimestamp(1490339531))

    #         embed.set_thumbnail(url="https://cdn.discordapp.com/app-icons/293110345076047893/15e2a6722723827ff9bd53ca787df959.jpg")
    #         embed.set_author(name="CSSS-Minion", icon_url="https://cdn.discordapp.com/app-icons/293110345076047893/15e2a6722723827ff9bd53ca787df959.jpg")
    #         embed.set_footer(text="CSSS-Minion", icon_url="https://cdn.discordapp.com/app-icons/293110345076047893/15e2a6722723827ff9bd53ca787df959.jpg")

    #         embed.add_field(name="President", value="David Miiller")
    #         embed.add_field(name="Vice President", value="Jon Loewen")
    #         embed.add_field(name="Treasurer", value="Dustin Cao")
    #         embed.add_field(name="Director of Resources", value="Kiarash Mirsalehi")
    #         embed.add_field(name="Director of Events", value="Brendan Chan")
    #         embed.add_field(name="Director of Communications", value="Henry Zhao")
    #         embed.add_field(name="Director of Archives", value="Josh Wu")
    #         embed.add_field(name="Source Code", value="https://github.com/henrymzhao/csss-minion/")

    #         await self.bot.say(embed=embed)


    # the following several functions are inspired by formatterhelper and default_help command
    def is_cog(self,ctx, command):
        return not self.is_bot(ctx,command) and not isinstance(command, Command)


    def is_bot(self,ctx,command):
        return command is ctx.bot


    def clean_prefix(self,context):
        """The cleaned up invoke prefix. i.e. mentions are ``@name`` instead of ``<@id>``."""
        user = context.bot.user
        # this breaks if the prefix mention is not the bot itself but I
        # consider this to be an *incredibly* strange use case. I'd rather go
        # for this common use case rather than waste performance for the
        # odd one.
        return context.prefix.replace(user.mention, '@' + user.name)



    def get_command_signature(self,ctx, command):
        """Retrieves the signature portion of the help page."""
        result = []
        prefix = self.clean_prefix(ctx)
        cmd = command
        parent = cmd.full_parent_name
        if len(cmd.aliases) > 0:
            aliases = '|'.join(cmd.aliases)
            fmt = '{0}[{1.name}|{2}]'
            if parent:
                fmt = '{0}{3} [{1.name}|{2}]'
            result.append(fmt.format(prefix, cmd, aliases, parent))
        else:
            name = prefix + cmd.name if not parent else prefix + parent + ' ' + cmd.name
            result.append(name)

        params = cmd.clean_params
        if len(params) > 0:
            for name, param in params.items():
                if param.default is not param.empty:
                    # We don't want None or '' to trigger the [name=value] case and instead it should
                    # do [name] since [name=None] or [name=] are not exactly useful for the user.
                    should_print = param.default if isinstance(param.default, str) else param.default is not None
                    if should_print:
                        result.append('[{}={}]'.format(name, param.default))
                    else:
                        result.append('[{}]'.format(name))
                elif param.kind == param.VAR_POSITIONAL:
                    result.append('[{}...]'.format(name))
                else:
                    result.append('<{}>'.format(name))

        return ' '.join(result)


    @commands.group(pass_context = True)
    async def help(self, ctx):
        """Display this help menu"""
        if ctx.invoked_subcommand is None:
            items = []
            print(type(self.bot.commands))
            for k in self.bot.commands: # grab all commands registered with the bot
                com = self.bot.commands[k]
                sig = self.get_command_signature(ctx,com) # grabs command signature
                items.append([sig,com.help]) # append command signature and pydoc to list


            items.append(["Source Code", "https://github.com/henrymzhao/csss-minion/"]) # keep src as last entry
            p = Pages(self.bot, message=ctx.message, entries = items, per_page=4)
            p.embed = discord.Embed(title="CSSS-Minion Commands", colour=discord.Colour(0xdc4643),timestamp=datetime.datetime.utcfromtimestamp(1490339531))
            p.embed.set_thumbnail(url="https://cdn.discordapp.com/app-icons/293110345076047893/15e2a6722723827ff9bd53ca787df959.jpg")
            p.embed.set_author(name="CSSS-Minion", icon_url="https://cdn.discordapp.com/app-icons/293110345076047893/15e2a6722723827ff9bd53ca787df959.jpg")
            p.embed.set_footer(text="CSSS-Minion", icon_url="https://cdn.discordapp.com/app-icons/293110345076047893/15e2a6722723827ff9bd53ca787df959.jpg")

            await p.paginate()

            # await self.bot.say(embed=embed)

    @help.command(pass_context = True)
    async def mc(self, ctx):
        """Display the help menu for the minecraft server"""
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
        """Display the number of players on the minecraft server"""
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
        """Display the minecraft server information"""
        if ctx.message.channel.name != "minecraft":
            await self.bot.say("Please move to #minecraft for this command.")
        else:
            em = discord.Embed(title='CSSS FTB Server Information', description="""IP: 172.93.48.238
    Modpack:  FTB Infinity 2.7 (Not 3.0 !)
    Minecraft: 1.7.10
    Cracked: YES
    See pinned message to download cracked client.""", colour=0x3D85C6)
            await self.bot.send_message(ctx.message.channel, embed=em)

def setup(bot):
    bot.add_cog(Info(bot))
