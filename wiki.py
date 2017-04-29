import discord
from discord.ext import commands
import requests
import json

# TODO: 
# wiki summary concatenates the one displayed on the wiki, it's possible we don't need fit_msg here.
# prettify message

class Wiki:
    """Makes wordart from strings or someshizz"""
    
    def __init__(self, bot):
        self.bot = bot
        
    #fits any string into <2k size and plop into arr
    def fit_msg(self, msg):
        msgs = []
        # split on "\n" or " " if possible.
        splitSymbol = "\n"
        simpleSplit = False
        suc = msg.find(splitSymbol,0,2000)
        if suc == -1:
            splitSymbol = " "
        suc = msg.find(splitSymbol,0,2000)
        if suc == -1:
            simpleSplit = True
        
        while len(msg) >= 2000:
            for x in range(2000,0,-1):
                if simpleSplit:
                    print("Simple splitting at: "+str(x))
                    msgs.append(msg[:x]) # the first newline before 2k chars is cutoff point
                    msg = msg[x:] #put everything after newline back into str 
                    break;
                elif msg[x] == splitSymbol:
                    print("FOUND A SPLITSYMBOL: "+ str(x))
                
                    msgs.append(msg[:x]) # the first newline before 2k chars is cutoff point
                    msg = msg[x:] #put everything after newline back into str
                    break;
        else: # append msg if too short ALSO adds final part of string after looping
            msgs.append(msg)
        return msgs    
        
        
    @commands.command()
    async def wiki(self, query:str):
        """shit goes here"""
        json = requests.get('https://en.wikipedia.org/api/rest_v1/page/summary/'+query+'?redirect=true')
        msg = json.json()
        if json.status_code == 200:
            if "description" in msg or msg["description"] == "Wikipedia disambiguation page":
            # no page found
                definition_str = "Try to be more specific"
            else:
                definition_str = "\n"+msg['title']+"\n\n"+msg['extract']
        else:
            definition_str = "There was an error."+str(json.status_code)+" There is no page for this."
        msgs = self.fit_msg(definition_str)
        for msg in msgs:
            await self.bot.say("```"+msg+"```")
        
        
def setup(bot):
    bot.add_cog(Wiki(bot))
