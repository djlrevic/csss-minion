import discord
from discord.ext import commands
import random as r
import datetime

class Announce:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def announce(self, ctx, title, desc):
        """Make an announcement
        Usage: announce <title> <body>
        Restricted command
        """
        author = ctx.message.author
        if author.permissions_in(ctx.message.channel).manage_channels or author.server_permissions.manage_channels:

            try:
                color = author.colour
            except Exception:
                color = discord.Colour(r.randrange(0xffffff))
            embed = discord.Embed(title = title, description = desc, color = color, timestamp = datetime.datetime.utcnow())
            embed.set_thumbnail(url=author.avatar_url)
            embed.set_author(name=author.display_name, icon_url = author.avatar_url)
            await self.bot.say(embed = embed)
        try:
            await self.bot.delete_message(ctx.message)
        except Exception:
            #thats ok
            print("Not allowed to delete message")


    @commands.command(pass_context = True)
    async def em(self, ctx, *desc):
        """Make an embedded message
        Usage: em <body>
        Restricted command
        """
        author = ctx.message.author
        if author.permissions_in(ctx.message.channel).manage_channels or author.server_permissions.manage_channels:

            try:
                color = author.colour
            except Exception:
                color = discord.Colour(r.randrange(0xffffff))
            string = ""
            for w in desc:
                string += w + " "
            string = string.strip()
            embed = discord.Embed(description = string, color = color)
            #embed.set_thumbnail(url=author.avatar_url)
            embed.set_author(name=author.display_name, icon_url = author.avatar_url)
            await self.bot.say(embed = embed)
        try:
            await self.bot.delete_message(ctx.message)
        except Exception:
            #thats ok
            print("Not allowed to delete message")


    #@commands.command(pass_context = True)
    #async def allowedEmbed(self, ctx):
    #    #echoes permissions
    #    await self.bot.say(ctx.message.author.permissions_in(ctx.message.channel).manage_channels)




def setup(bot):
    bot.add_cog(Announce(bot))
