import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from urllib import parse


class Imgur:

    def __init__(self, bot):
        self.bot = bot
   
    def parseDeeper(self, url):
        print(url)
        ret = requests.get(url)
        newurl = None
        if ret.status_code == 200:
            res = None
            soup = BeautifulSoup(ret.text, "html.parser")
            print("this is soup", type(soup))
            target = soup.find(itemprop="embedURL")
            if target == None:
                target = soup.find(name="twitter:player")
            if target == None:
                target = soup.find(name='twitter:image')
            if target == None:
                target = soup.find(itemprop='contentURL')
            print(type(target))
            newurl = target['content']
        if newurl == None:
            print("we dun goofed")
        return newurl
   
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
                req = self.parseDeeper(res)
                return req
            else:
                return "Either the HTML parser failed or you searched for dumb shit."
        else:
            return "imgur Server Error "+str(ret.status_code)
    
    
    def parseResponse_embed(self, word):
        query = "http://imgur.com/search?q="+word
        keystr = "//i.imgur.com/"
        ret = requests.get(query)
        if ret.status_code == 200:
            res = None
            html = ret.text
            soup = BeautifulSoup(html, "html.parser")
            for link in soup.find_all('img'):
                hyperlink = link.get('src')
                if hyperlink is not None:
                    decoded = parse.unquote(hyperlink) #URL decoding, not important.
                    if keystr in hyperlink:
                        #res = "http://"+hyperlink[2:len(hyperlink)-5] + hyperlink[len(hyperlink)-4:]
                        res = "http://"+hyperlink[2:len(hyperlink)-5] + ".gif"
                        break;     
            if res is not None:
                return res
            else:
                return "Either the HTML parser failed or you searched for dumb shit."
        else:
            return "imgur Server Error "+str(ret.status_code)
    
    
    
    @commands.command(pass_context=True)
    async def imgur(self,ctx, *word:str):
        """Search for a picture on imgur"""
        word = " ".join(word)
        msg = self.parseResponse_embed(word)
        em = discord.Embed(colour=0xfff)
        em.set_image(url=msg)
        await self.bot.send_message(ctx.message.channel, embed=em)
        #await self.bot.say(msg)     
        
        #TEST FUNCTION
    @commands.command(pass_context=True)
    async def testimg(self, ctx, *word:str):
        """This is for testing"""
#        msg = "http://i.imgur.com/Yq9u0Hq.png"  
        msg = "http://i.imgur.com/nuZFJNm.png" 
        em = discord.Embed(colour=0xfff)
        em.set_image(url=msg)
        await self.bot.send_message(ctx.message.channel, embed=em)
        await self.bot.say(msg)   
   
   
def setup(bot):
    bot.add_cog(Imgur(bot))
