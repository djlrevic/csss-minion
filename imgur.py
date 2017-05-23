import discord
from discord.ext import commands
import requests

class Imgur:

    def __init__(self, bot):
        self.bot = bot
        self.headers = {'authorization':'Client-ID '+self.bot.imgur_id}
        self.url = 'https://api.imgur.com/3/gallery/search/{{sort}}/{{window}}/{{page}}' #nice
    
    def imgur_api(self, search):
        querystring={'q':search}
        img = None
        res = requests.request('GET', self.url, headers=self.headers, params=querystring)
        if res.status_code == 200:
            ret = res.json()
            
            if len(ret['data']) == 0: #shit's bad
                return None
            
            if 'animated' in ret['data'][0]: # animated URL, yoink!
                if 'link' in ret['data'][0]:
                    img = ret['data'][0]['link']
                    desc = ret['data'][0]['title']
            
            else: #not animated, construct our own URL
                img = "http://i.imgur.com/6rqtdQ2.jpg"
                if 'cover' in ret['data'][0]:
                    img = "http://i.imgur.com/"+ret['data'][0]['cover']+".jpg"
                    desc = ret['data'][0]['title']
        return (desc,img)   
    
    
    @commands.command(pass_context=True)
    async def imgur(self,ctx, *word:str):
        """Search for a picture on imgur"""
        msg = self.imgur_api(" ".join(word))
        if msg == None:
            await self.bot.embed_this_for_me("Nothing found in imgur's vast database.\nPerhaps you really are a special snowflake?",ctx)
        else:
            em = discord.Embed(title=msg[0] ,colour=0xfff)
            em.set_image(url=msg[1])
            await self.bot.send_message(ctx.message.channel, embed=em)
   
def setup(bot):
    bot.add_cog(Imgur(bot))
