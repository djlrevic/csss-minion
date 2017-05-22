import discord
from discord.ext import commands
import random as r
import datetime

class Announce:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def announce(self, ctx, title, desc):
        author = ctx.message.author
        color = discord.Colour(r.randrange(0xffffff))
        embed = discord.Embed(title = title, description = desc, color = color, timestamp = datetime.datetime.utcnow())
        embed.set_thumbnail(url=author.avatar_url)
        embed.set_author(name=author.display_name, icon_url = author.avatar_url)
        await self.bot.delete_message(ctx.message)
        await self.bot.say(embed = embed)

    @commands.command(pass_context = True)
    async def embed(self, ctx, *desc):
        author = ctx.message.author
        color = discord.Colour(r.randrange(0xffffff))
        string = ""
        for w in desc:
            string += w + " "
        string = string.strip()
        embed = discord.Embed(description = string, color = color, timestamp = datetime.datetime.utcnow())
        #embed.set_thumbnail(url=author.avatar_url)
        embed.set_author(name=author.display_name, icon_url = author.avatar_url)
        await self.bot.delete_message(ctx.message)
        await self.bot.say(embed = embed)




def setup(bot):
    bot.add_cog(Announce(bot))
