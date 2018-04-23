import discord
from discord.ext import commands
from sfuapi import roadconditions as road

class Roads:

    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def roads(self, ctx, *args):
        """Display road conditions for SFU
        Usage: roads <city>
        """
        if len(args) >= 1:
            text = road.conditions(args[0])
        else:
            text = road.conditions()

        text += road.announcements()
        await ctx.send("```" + text+ "```")




def setup(bot):
    bot.add_cog(Roads(bot))
