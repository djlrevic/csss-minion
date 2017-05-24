import discord
from discord.ext import commands
import requests
import json
import random

# TODO:
# is most of poetry_url redundant with new commands.bot?

class Poem:
    poetry_base_url = "http://poetrydb.org/"
    def __init__(self, bot):
        self.bot = bot
        self.poetry_title_cache = None
        
    # cache titles to avoid 2 API calls when servicing random poem
    def populate_poetry_cache(self):
        url = self.poetry_base_url + "title"
        json = requests.get(url)
        if json.status_code == 200:
            msg = json.json()
            if "titles" in msg:
                self.poetry_title_cache = msg
                print("Cache filled")
                #print(type(msg))
                #print(type(self.poetry_title_cache))
            else:
                print("Cache not filled")
        else:
            print("Error populating poetry cache: "+ json.status_code)    
        
        
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
    
    def poetry_url(self, args):
        length = len(args)
        url = self.poetry_base_url
        if length == 0:
            #empty?? shouldn't be
            if self.poetry_title_cache == None:
                self.populate_poetry_cache()
            idx = random.randrange(0,len(self.poetry_title_cache["titles"])-1)
            url += "title/"+self.poetry_title_cache["titles"][idx]
            print("nothing?")
        elif length == 1:
            if len(args[0]) == 0:
                #random poem
                if self.poetry_title_cache == None:
                    self.populate_poetry_cache()
                idx = random.randrange(0,len(self.poetry_title_cache["titles"])-1)
                url += "title/"+self.poetry_title_cache["titles"][idx]
            else:
                url += "title/"+args[0]
        elif length == 2:
            url += "author,title/"+args[1]+";"+args[0]
        elif length == 3:
            url += "author,title,linecount/"+args[1]+";"+args[0]+";"+args[2]
        return url
            
    

    def poetry_json(self, url):
        json = requests.get(url)
        msg = json.json()
        if json.status_code == 200:
            if "status" in msg: #means there is db error
                title = "error"
                new_str = "Database Error: "+str(msg["status"])+"\n"+msg["reason"]
            else:
                title = msg[0]["title"]+", by "+msg[0]["author"]
                new_str = "\n"
                for part in msg[0]["lines"]:
                    new_str += part
                    new_str += "\n"
        else:
            new_str = "HTTP Error: "+str(json.status_code)
        return (title,new_str)# return tuple, one is the title, other is poem/error.
         
    @commands.command(pass_context=True)
    async def poem(self,ctx, *args):
        """Searches for a poem
        usage: !poem <title> <author> <length>
        
        """
        #print(args)
        url = self.poetry_url(args)
        msg = self.poetry_json(url)
        msgs = self.fit_msg(msg[0]+"\n"+msg[1])
        #print("There are "+str(len(msgs))+" parts to this msg")
        if msg[0] == "error":
            await self.bot.say("Spelling error or not in database.")
        else:
            await self.bot.say("Sending "+msg[0]+" to "+str(ctx.message.author))
            for msg in msgs:
                await self.bot.send_message(ctx.message.author, msg)
        
        
def setup(bot):
    bot.add_cog(Poem(bot))
