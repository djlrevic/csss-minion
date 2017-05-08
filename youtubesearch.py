import requests
import discord
from discord.ext import commands
from bs4 import BeautifulSoup #it's so beautiful


class YoutubeSearch:


    def __init__(self, bot):
        self.bot = bot
        
    def requestVid(self, query:str):
        keystr = "/watch?v=" # video id
        noResults = firstRes = 'nothing' # wizardry
        query = "https://www.youtube.com/results?search_query="+query
        ret = requests.get(query)
        if ret.status_code == 200:
        
            html = ret.text
            soup = BeautifulSoup(html, "html.parser")
            for link in soup.find_all('a'):
                hyperlink = link.get('href')
                if keystr in hyperlink:
                    firstRes = hyperlink
                    break;
            fullURL = "https://www.youtube.com"+firstRes
            if noResults == firstRes:
                return "No search results found"
            else:
                return fullURL
        else:
            return "Youtube Server Error"
        
    @commands.command(pass_context=True)
    async def youtube(self, ctx, query :str):
        link = self.requestVid(query)
        await self.bot.say(link)
        
        
def setup(bot):
    bot.add_cog(YoutubeSearch(bot))
