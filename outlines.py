import discord
from discord.ext import commands
from sfuapi import courses

class Outlines:

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def outline(self, *args):
        #probably a better way to do this
        #await self.bot.say(args)
        try:
            if len(args) == 2:
                keys, data = (courses.list_outline(args[0], args[1]))
            elif len(args) == 3:
                keys, data = (courses.list_outline(args[0], args[1], args[2]))
            elif len(args) == 4:
                keys, data = (courses.list_outline(args[0], args[1], args[2], args[3]))
            elif len(args) == 5:
                keys, data = (courses.list_outline(args[0], args[1], args[2], args[3], args[4]))
            else:
                keys, data = ['Error'], ["Usage: outline <department> <number> (section) (year) (semester)"]
        except Exception as e:
            data = {'Error': "{}".format(e)}
        embed = discord.Embed(title = "SFU Course Outlines", color = discord.Colour(0xa6192e))
        embed.set_thumbnail(url="http://www.sfu.ca/content/sfu/clf/jcr:content/main_content/image_0.img.1280.high.jpg/1468454298527.jpg")
        embed.set_footer(text= "Written by Brendan")
        for key, entry in zip(keys, data):
            print(key)
            if entry != "":
                embed.add_field(name = key.title(), value = entry, inline = False)
        if len(keys) != 1:
            embed.add_field(name = "URL", value = "https://www.sfu.ca/outlines.html?" + data[0].lower())
        await self.bot.say( embed=embed)


def setup(bot):
    bot.add_cog(Outlines(bot))
