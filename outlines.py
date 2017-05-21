import discord
from discord.ext import commands
from sfuapi import courses

class Outlines:

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def outline(self, *args):
        #probably a better way to do this
        await self.bot.say(args)
        try:
            if len(args) < 2:
                data = {'Error':"Usage: outline <department> <number> (section) (year) (semester)"}
            elif len(args) == 2:
                data = (courses.dict_outline(args[0], args[1]))
            elif len(args) == 3:
                data = (courses.dict_outline(args[0], args[1], args[2]))
            elif len(args) == 4:
                data = (courses.dict_outline(args[0], args[1], args[2], args[3]))
            elif len(args) == 5:
                data = (courses.dict_outline(args[0], args[1], args[2], args[3], args[4]))
            else:
                data = {'Error':"Usage: outline <department> <number> (section) (year) (semester)"}
        except Exception as e:
            data = {'Error': "{}".format(e)}
        embed = discord.Embed(title = "SFU Course Outlines", color = discord.Colour(0xa6192e))
        for key, entry in data.items():
            if entry != "":
                embed.add_field(name = key.title(), value = entry)


        await self.bot.say(embed=embed)


def setup(bot):
    bot.add_cog(Outlines(bot))
