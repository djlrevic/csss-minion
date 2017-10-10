import discord
import random
from discord.ext import commands
from os import path



class Memes:


    top = path.dirname(__file__)
    sub = "wordart_dir"
    def __init__(self, bot):
        self.bot = bot
        
# also this http://i.imgur.com/dmqYSvu.jpg
    @commands.command(pass_context=True)
    async def impeach(self,ctx):
        """Impeach our dear leader"""
        em = discord.Embed(colour=0xfff, title="Little did they know he was in peach the whole time.")
        em.set_image(url="http://i.imgur.com/pCQT0pm.png")
        await self.bot.send_message(ctx.message.channel, embed=em)
        #await self.bot.say("Yessir! Right away, sir!" + "http://imgur.com/pCQT0pm")
        
    @commands.command(pass_context=True)
    async def triggered(self,ctx):
        images = ['https://cdn.discordapp.com/attachments/228761314644852736/361739947876548608/tenor.gif',
                    'https://giphy.com/gifs/ZEVc9uplCUJFu',
                    'https://i.imgur.com/P6XduSJ.gif',
                    'https://media.tenor.com/images/d213cc0fadd5b0aa5d088c2b8cd6dc47/tenor.gif',
                    'https://thumbs.gfycat.com/DearestSpiffyAlpaca-small.gif',
                    'https://media.giphy.com/media/oCdScruZnEHfy/source.gif',
                    'http://i0.kym-cdn.com/photos/images/newsfeed/001/034/138/cd0.gif',
                    'http://orig09.deviantart.net/dfb2/f/2015/263/6/3/triggered_by_mrlorgin-d9aahmc.png']
        """When someone has a mildly different opinion."""
        em = discord.Embed(colour=0xfff, title="Oh no you didn't!")
        em.set_image(url= images[random.randint(0, len(images) - 1)])
        await self.bot.send_message(ctx.message.channel, embed=em)
        #await self.bot.say("Oh no you didn't!"+" http://orig09.deviantart.net/dfb2/f/2015/263/6/3/triggered_by_mrlorgin-d9aahmc.png")

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
        
    @commands.command(pass_context=True)
    async def prettygood(self,ctx):
        em = discord.Embed(colour=0xfff)
        em.set_image(url='https://i.imgflip.com/y7owh.jpg')
        await self.bot.send_message(ctx.message.channel, embed=em)

    @commands.command()
    async def beep(self):    
        await self.bot.say("boop")
        
        
    @commands.command(pass_context=True)
    async def joke(self,ctx):
        img = path.join(self.top, self.sub, "thejoke_henry.png")
        await self.bot.send_file(ctx.message.channel, img)

    @commands.command(pass_context=True)
    async def doraemon(self, ctx):
        images = ['https://i.imgur.com/uPTZgf2.png',
                    'https://i.imgur.com/S5h6PLQ.png',
                    'https://i.imgur.com/Uh8S2Ao.png',
                    'https://i.imgur.com/uCPV26a.png',
                    'https://i.pinimg.com/236x/84/e2/e1/84e2e129c8f9345561418f4ff27fecaa.jpg',
                    'https://i.pinimg.com/736x/fb/b7/f2/fbb7f2f68a3901723c9c63d7d26b4e53--funny-animal-humor-cat-cat.jpg']
        rand = random.randint(0, len(images) - 1)
        if rand == 5:
            temp = random.randint(0, 1)
            if temp % 2 == 0:
                rand = random.randint(0, len(images) - 1)
        if rand == 5:
            em = discord.Embed(colour=0xfff, title = "Really? Do you still doubt I am doraemon?")
        else:
            em = discord.Embed(colour=0xfff, title="I am doraemon!")
        em.set_image(url=images[rand])
        await self.bot.send_message(ctx.message.channel, embed=em)


        
def setup(bot):
    bot.add_cog(Memes(bot))
