import discord
from discord.ext import commands



class Memes:

    def __init__(self, bot):
        self.bot = bot
        
# also this http://i.imgur.com/dmqYSvu.jpg
    @commands.command(pass_context=True)
    async def impeach(self,ctx):
        """Impeach our dear leader"""
        em = discord.Embed(colour=0xfff)
        em.set_image(url="http://i.imgur.com/pCQT0pm.png")
        await self.bot.send_message(ctx.message.channel, embed=em)
        #await self.bot.say("Yessir! Right away, sir!" + "http://imgur.com/pCQT0pm")
        
    @commands.command(pass_context=True)
    async def triggered(self,ctx):
        """When someone has a mildly different opinion."""
        em = discord.Embed(colour=0xfff, title="Oh no you didn't!")
        em.set_image(url="http://orig09.deviantart.net/dfb2/f/2015/263/6/3/triggered_by_mrlorgin-d9aahmc.png")
        await self.bot.send_message(ctx.message.channel, embed=em)
        #await self.bot.say("Oh no you didn't!"+" http://orig09.deviantart.net/dfb2/f/2015/263/6/3/triggered_by_mrlorgin-d9aahmc.png")


    @commands.command(pass_context=True)
    async def remindme(self, ctx, *args):
        """Remindme function"""
        await self.bot.embed_this_for_me("Thanks for reminding me to write the rest of this function", ctx)
        #await self.bot.say("```Thanks for reminding me to write the rest of this function.```")

    @commands.command(pass_context=True)
    async def kms(self,ctx):
        """Don't"""
        em = discord.Embed(colour=0xfff)
        em.set_image(url="http://i.imgur.com/XStaKp3.gif")
        await self.bot.send_message(ctx.message.channel, embed=em)
        #await self.bot.say("http://i.imgur.com/XStaKp3.gif")

    @commands.command(pass_context=True)
    async def eggplant(self,ctx):
        """And they're like, it's better than yours"""
        await self.bot.embed_this_for_me("🍆My eggplant brings all the boys to the yard🍆", ctx)
        #await self.bot.say("🍆My eggplant brings all the boys to the yard🍆")
        
    @commands.command(pass_context=True)
    async def goodluck(self,ctx):
        """Wish someone good luck"""
        em = discord.Embed(colour=0xfff, title="May your luck be good")
        em.set_image(url="http://i.imgur.com/sbY9DeH.jpg")
        await self.bot.send_message(ctx.message.channel, embed=em)
        #await self.bot.say("http://i.imgur.com/sbY9DeH.jpg")
        
        
def setup(bot):
    bot.add_cog(Memes(bot))
