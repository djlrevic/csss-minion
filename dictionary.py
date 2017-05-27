import discord
from discord.ext import commands
from PyDictionary import PyDictionary

class Dictionary:
    
    def __init__(self, bot):
        self.bot = bot
        self.dictionary = PyDictionary('lxml')
       
       #TODO a query like 'a;lskejf;laskjf;lkjvldskjrlgjslfgnhslkfnhsoifjosijosjeojsopejr' gives a valid response with an unknown subject. UNKNOWN FIX
    @commands.command(pass_context=True)
    async def meaning(self,ctx, word:str):
        """Return the meaning of a word"""
        ret = self.dictionary.meaning(word)
        if ret is None:
            #await self.bot.say("```Meaning for "+word+" not found.```")
            await self.bot.embed_this_for_me("Meaning for *"+word+"* not found", ctx)
        else:
            def_str = ""
            for k in ret.keys():
                def_str +=k + ":\n"
                for i in ret[k][:3]:
                     def_str += i + "\n"
                def_str += "\n"
            #await self.bot.say("```"+def_str+"```")
            await self.bot.embed_this_for_me(def_str, ctx)
       
    @commands.command(pass_context=True)
    async def stealthegg(self, ctx):
        await self.bot.delete_message(ctx.message)
        await self.bot.say(":eggplant:")
        
        
        
    @commands.command(pass_context=True)
    async def synonym(self,ctx, word:str):
        """Return the synonym of a word"""
        ret = self.dictionary.synonym(word)
        if ret is None:
            #await self.bot.say("```Synonym for "+word+" not found.```")
            await self.bot.embed_this_for_me("Synonym for *"+word+"* not found", ctx)
        else:
            def_str = "Synonyms for "+word+": "
            for j in ret:
                def_str += j + ", "
#            await self.bot.say("```"+def_str+"```")
            await self.bot.embed_this_for_me(def_str, ctx)
    
    @commands.command(pass_context=True)
    async def antonym(self,ctx, word:str):
        """Return the antonym of a word"""
        ret = self.dictionary.antonym(word)
        if ret is None:
#            await self.bot.say("```Antonym for "+word+" not found.```")
            await self.bot.embed_this_for_me("Antonym for *"+word+"* not found", ctx)
        else:
            def_str = "Antonyms for "+word+": "
            for j in ret:
                def_str += j + ", "
#            await self.bot.say("```"+def_str+"```")
            await self.bot.embed_this_for_me(def_str, ctx)
 
        
def setup(bot):
    bot.add_cog(Dictionary(bot))
