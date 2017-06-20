import requests
import discord
from discord.ext import commands

class UrbanDict:

    def __init__(self, bot):
        self.bot = bot
        self.key = self.bot.mashape_key #this key is your key, this key is my key.
        self.headers = {"X-Mashape-Key": self.key, "Accept": "text/plain"}
        
    # take raw json response and return appropriate message for bot to say    
    def parseResponse(self, json):
        if json.status_code == 200:
            r = json.json()
            if r['result_type'] == "exact":
                msg = " " #python strings are funny sometimes
                msg += r['list'][0]['word']
                msg +="```"+ r['list'][0]['definition'] +"```"
                msg += "**example: **"+r['list'][0]['example']
                msg += "\n<"+r['list'][0]['permalink']+">"
                return msg
                
            elif r['result_type'] == "no_results":
                return "You probably typed in some dumb shit, cuz I can't find it." 
                
            else:
                return "Contact Nos ASAP cuz shit's broke"
                  
        else:
            return "Bad response from server  *shrugs*"
     
        
    @commands.command(pass_context=True)
    async def urban(self,ctx, *msg:str):
        """Lookup some jargon from the urban dictionary."""
        word = " ".join(msg)
        query = "https://mashape-community-urban-dictionary.p.mashape.com/define?term="+word
        req = requests.get(query, headers=self.headers)
        ret = self.parseResponse(req)
        msgs = self.bot.fit_msg(ret,1024)
        try:
            await self.bot.embed_this_for_me(msgs[0],ctx)
        except:
            await self.bot.say("The content is probably too long for discord to handle")
        
def setup(bot):
    bot.add_cog(UrbanDict(bot))
