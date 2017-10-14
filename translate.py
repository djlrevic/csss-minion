import discord
from discord.ext import commands
import json
import requests
import urllib.parse


class Translate:

    def __init__(self, bot):
        self.bot = bot
        # https://www.youtube.com/watch?v=T3EIEOSN3EA
        
        self.codes = json.load(open("lang.json"))
      
    def sneakpastgooglesecurity(self, msg, tlang, slang='en'): # default to english
        fmt = self.bot.lang_url.format(slang,tlang,urllib.parse.quote_plus(msg))
        #fmt = self.url.format(slang,tlang,msg)
        #print(fmt)
        req = requests.get(fmt)
        if req.status_code == 200:
            ret = req.json()
            #print(ret)
            newm = ''
            for tr in ret[0]:
                newm += tr[0]
            if type(newm) == str and len(newm) >= 1:
                return newm
            else:
                return "Something goofed"
        
            
        
        
    @commands.command(pass_context=True)
    async def translate(self, ctx, *args):
        """Translate a string into a specified language!
        usage: !translate <target> (source)
        example translate into spanish: <!translate "I like cheese" es>
        To specify source language, include a third arg:
        !translate "Je suis formé à la guerre de Nerf et j'ai le plus d'étoiles d'or dans toute la classe maternelle." en fr
        Supported languages and language codes listed on this webpage
        https://cloud.google.com/translate/docs/languages
        
        """
        if len(args) < 2:
            #print("not enough arguments")
            await self.bot.embed_this_for_me("Not enough arguments or bad language code.",ctx)
            return
        if args[1] not in self.codes:
            #print("not supported language code")
            await self.bot.embed_this_for_me("Please visit https://cloud.google.com/translate/docs/languages for a list of supported languages and codes",ctx)
            return
        if len(args) == 3:
            msg = self.sneakpastgooglesecurity(args[0],args[1],args[2])    
        elif len(args) == 2:
            msg = self.sneakpastgooglesecurity(args[0],args[1])
        #await self.bot.embed_this_for_me(msg,ctx)
        #print("msg length: ",len(msg))
        #print(type(msg))
        mstr = u"{}".format(msg)
        #print(mstr)
        msgs = self.bot.fit_msg(msg,1024)
        em = discord.Embed(colour=0xfff,title="Results from translate")
        for m in msgs:
            em.add_field(name="text", value=m)
        await ctx.send(embed=em)
        
        
        
def setup(bot):
    bot.add_cog(Translate(bot))
