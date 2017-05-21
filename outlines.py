import discord
from discord.ext import commands
from sfuapi import courses

class Outlines:

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def outline(self, *args):
        #probably a better way to do this
        if len(args) < 2:
            data = {'Error':"Usage: outline <department> <number> (section) (year) (semester)"}
        elif len(args) == 2:
            data= (courses.print_outline(args[0], args[1]))
        elif len(args) == 3:
            data = (courses.print_outline(args[0], args[1], args[2]))
        elif len(args) == 4:
            data = (courses.print_outline(args[0], args[1], args[2], args[3]))
        elif len(args) == 5:
            data = (courses.print_outline(args[0], args[1], args[2], args[3], args[4]))
        else:
            data = {'Error':"Usage: outline <department> <number> (section) (year) (semester)"}

        embed = discord.Embed(title = "SFU Course Outlines", color = discord.Colour(0xa6192e))
        for key, entry in data.iteritems():
            embed.add_field(name = key.title(), value = value)


        await self.bot.say(embed=embed)


def setup(bot):
    bot.add_cog(Outlines(bot))
