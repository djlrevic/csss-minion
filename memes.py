import discord
import random
from discord.ext import commands
from os import path



class Memes:

    top = path.dirname(__file__)
    sub = "memepics"
    def __init__(self, bot):
        self.bot = bot
        
   
    @commands.command()
    async def beep(self, ctx):    
        await ctx.send("boop")
        
     
    @commands.command()
    async def ding(self, ctx):
        await ctx.send("dong")    


    @commands.command()
    async def dank(self, ctx):
        await ctx.send("memes")

    @commands.command(pass_context=True)
    async def eggplant(self,ctx):
        """And they're like, it's better than yours"""
        await self.bot.embed_this_for_me("🍆My eggplant brings all the boys to the yard🍆", ctx)        
        
    @commands.command(pass_context=True)# also this http://i.imgur.com/dmqYSvu.jpg
    async def impeach(self,ctx):
        """Impeach our dear leader"""
        img = path.join(self.top,self.sub,"meme_in_peach.png")
        await ctx.send(file=discord.File(img))
        

    @commands.command(pass_context=True)
    async def kms(self,ctx):
        """Don't"""
        img = path.join(self.top, self.sub, "meme_kms.gif")
        await ctx.send(file=discord.File(img))

        
    @commands.command(pass_context=True)
    async def goodluck(self,ctx):
        """Wish someone good luck"""
        img = path.join(self.top, self.sub, "meme_good_luck.jpg")
        await ctx.send(file=discord.File(img))

        
    @commands.command(pass_context=True)
    async def prettygood(self,ctx):
        img = path.join(self.top, self.sub, "meme_pretty_good.jpg")
        await ctx.send(file=discord.File(img))
       
    @commands.command(pass_context=True)
    async def henry(self, ctx):
        im = path.join(self.top, self.sub, "dear_leader_henry.jpg")
        await ctx.send(file=discord.File(img))
    
        
    @commands.command(pass_context=True)
    async def joke(self,ctx):
        img = path.join(self.top, self.sub, "Joke_over_Henry.png")
        await ctx.send(file=discord.File(img))


    @commands.command(pass_context=True)
    async def doraemon(self, ctx):
        images = [
            'doraemon1.png',
            'doraemon2.png',        
            'doraemon3.png',
            'doraemon4.png',
            'doraemon5.png'
            ]
        img = path.join(self.top,self.sub,images[random.randint(0,len(images)-1)])
        await ctx.send(file=discord.File(img))


    @commands.command(pass_context=True)
    async def triggered(self,ctx):
        """When someone has a mildly different opinion."""
        images = [
            'triggered_beanie.gif',
            'triggered_nicolas_cage.gif',
            'triggered_ninja_turtle.gif',
            'triggered_sherlock.gif',
            'triggered_sjw.gif',
            'triggered_tenor.gif',
            'triggered_thomas_tank_engine.png',
            'triggered_undertale_skeleton.gif'
            ]
        img = path.join(self.top,self.sub,images[random.randint(0,len(images)-1)])
        await ctx.send(file=discord.File(img))
        
        
def setup(bot):
    bot.add_cog(Memes(bot))
