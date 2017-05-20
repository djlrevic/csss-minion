import discord
from discord.ext import commands
from sfuapi import roadconditions as road

class Roads:

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def roads(self, *args):
        if len(args) > 1:
            text = road.conditions(args[1])
        else:
            text = road.conditions()
        await self.bot.say(text)


def setup(bot):
    bot.add_cog(Roads(bot))
