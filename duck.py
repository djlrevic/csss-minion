import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from urllib import parse
# note to self, do not use mashape API for duckduckgo. It has malformed JSON
# note to self, duckduckgo API doesn't return search results... just scrape


class Duck:

    def __init__(self, bot):
        self.bot = bot
        self.emojis = None
   
    # take raw json response and return appropriate message for bot to say    
    def parseResponse(self, word):
        removestr = ["search.yahoo.com", "advertising-and-affiliates"]
        keystr = ["https://", "http://"]
        query = "https://duckduckgo.com/html/?q="+word
        ret = requests.get(query)
        if ret.status_code == 200:
            results = []
            results.append("Results provided by DuckDuckGo... Don't get any viruses now...")
            html = ret.text
            soup = BeautifulSoup(html, "html.parser")
            for link in soup.find_all('a'):
                hyperlink = link.get('href')
                if hyperlink is not None:
                    decoded = parse.unquote(hyperlink) #URL decoding, important.
                    if removestr[0] in decoded or removestr[1] in decoded:
                        #print("removed a link "+decoded)
                        continue; # don't add these
                    if keystr[0] in decoded: #https link
                        #print("keystring found in "+ decoded)
                        cutoff = decoded[decoded.find('https://'):] # find only the URL part
                        #print("Have cutoff: "+cutoff)
                        if cutoff not in results: # don't put 4 duplicates in arr
                            #print("Adding cutoff: "+cutoff)
                            results.append(cutoff)
                    elif keystr[1] in decoded: #http link
                        #print("keystring found in "+decoded)
                        cutoff = decoded[decoded.find('http://'):] # find only the URL part
                        #print("Have cutoff: "+cutoff)
                        if cutoff not in results: # don't put 4 duplicates in arr
                            #print("Adding cutoff: "+cutoff)
                            results.append(cutoff)    
            res = results[0]
            for r in results[1:11]: # return 10 results
                res += "\n<"+r+">"  # escape discord embedding       
            if len(results) == 1:
                return "DuckDuckGo could not find any results"
            else:
                return res
        else:
            return "DuckDuckGo Server Error"
    
    
    
    @commands.command()
    async def search(self, *query):
        word = " ".join(query)
        msg = self.parseResponse(word)
        await self.bot.say(msg)
        
      #<:crabplant:314875003168489472>
  
    @commands.command(pass_context=True)
    async def eggwrite(self, ctx, *msg):
        if self.emojis == None:
            self.emojis = ctx.message.server.emojis
        word = " ".join(msg)
        newstr = ""
        for s in word:
            if s.isalpha():
                #convert to eggplant letter
                for em in self.emojis:
                    if str(em)[2] == s.upper():
                        newstr += str(em)
            elif s == " ":
                #change to 5 spaces
                newstr += "     "
            else:
                newstr += s
        await self.bot.say(newstr)
        
        
   # @commands.command()
   # async def eggwrite(self, *word):
   #     newstr = ""
   #     for s in word:
   #         if s.isalpha():
   #             newstr += "**:"+s.upper()+"_Eggplant:**"
   #             #newstr += ":regional_indicator_"+s.lower()+":"
   #         else:
   #             newstr += s
   #     await self.bot.say(newstr)
        
   
def setup(bot):
    bot.add_cog(Duck(bot))
