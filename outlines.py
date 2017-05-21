import discord
from discord.ext import commands
from sfuapi import courses

class Outlines:

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def outline(self, *args):
        #probably a better way to do this
        text = ""
        if len(args) < 2:
            text = ("Usage: outline <department> <number> (section) (year) (semester)")
        elif len(args) == 2:
            text = (courses.print_outline(args[0], args[1]))
        elif len(args) == 3:
            text = (courses.print_outline(args[0], args[1], args[2]))
        elif len(args) == 4:
            text = (courses.print_outline(args[0], args[1], args[2], args[3]))
        elif len(args) == 5:
            text = (courses.print_outline(args[0], args[1], args[2], args[3], args[4]))
        else:
            text = ("Usage: outline <department> <number> (section) (year) (semester)")

        await self.bot.say("```" + text + "```")


def setup(bot):
    bot.add_cog(Outlines(bot))
