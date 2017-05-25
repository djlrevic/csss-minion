import discord
from discord.ext import commands
import requests
import json

#TODO wiki result lists input str instead of returned subject, must fix inconsistancy. < how to reproduce?

class Wiki:
    
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
                    #print("Simple splitting at: "+str(x))
                    msgs.append(msg[:x]) # the first newline before 2k chars is cutoff point
                    msg = msg[x:] #put everything after newline back into str 
                    break;
                elif msg[x] == splitSymbol:
                    #print("FOUND A SPLITSYMBOL: "+ str(x))
                    msgs.append(msg[:x]) # the first newline before 2k chars is cutoff point
                    msg = msg[x:] #put everything after newline back into str
                    break;
        else: # append msg if too short ALSO adds final part of string after looping
            msgs.append(msg)
        return msgs    
           
        
    @commands.command(pass_context=True)
    async def wiki(self,ctx, *msg):
        """Look up a subject on wikipedia"""
        query = " ".join(msg)
        link = " "
        json = requests.get('https://en.wikipedia.org/w/api.php?action=opensearch&search='+query+'&limit=5&format=json&redirects=resolve')
        msg = json.json()
        if json.status_code == 200 and not len(msg[1]) == 0:
            if isinstance(msg[1][0], str) and ("(disambiguation)" in msg[1][0] or "may refer to:" in msg[2][0]): #wiki has no standard, so we need to check for all of these cases
                definition_str = "Search for *"+msg[0]+"* is too general. Try one of these: \n"
                for i in range(0,len(msg[1])):
                    if "may refer to:" not in msg[2][i]:
                        definition_str += "\n"+msg[1][i]
            else:
                definition_str = "Wiki summary for "+ msg[0] + "\n\n" +msg[2][0]
                link = msg[3][0]
        else:
            definition_str = "There was an error "+str(json.status_code)+". There is no page for this."
        msgs = self.fit_msg(definition_str)
        await self.bot.embed_this_for_me(definition_str +"\n"+link, ctx)
       # for msg in msgs:
       #     await self.bot.say("```"+msg+"```")
       # if type(link) == str:
       #     await self.bot.say("<"+link+">")
        
def setup(bot):
    bot.add_cog(Wiki(bot))
