import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from urllib import parse


class Imgur:

    def __init__(self, bot):
        self.bot = bot
   
   
    # take raw json response and return appropriate message for bot to say    
    def parseResponse(self, word):
        query = "http://imgur.com/search?q="+word
        keystr = "/gallery/"
        ret = requests.get(query)
        if ret.status_code == 200:
            res = None
            html = ret.text
            soup = BeautifulSoup(html, "html.parser")
            for link in soup.find_all('a'):
                hyperlink = link.get('href')
                if hyperlink is not None:
                    decoded = parse.unquote(hyperlink) #URL decoding, not important.
                    if keystr in hyperlink:
                        res = "http://imgur.com"+hyperlink
                        break;     
            if res is not None:
                return res
            else:
                return "Either the HTML parser failed or you searched for dumb shit."
        else:
            return "imgur Server Error "+str(ret.status_code)
    
    
    
    @commands.command(pass_context=True)
    async def imgur(self,ctx, *word:str):
        word = " ".join(word)
        msg = self.parseResponse(word)
        await self.bot.say(msg)
        
   
def setup(bot):
    bot.add_cog(Imgur(bot))
