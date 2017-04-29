import discord
from discord.ext import commands
from PyDictionary import PyDictionary

# !meaning #meaning of a word
# !synonym #synonyms of a word
# !antonym #antonyms of a word
# !translate #translation of a word

class Dictionary:
    """Makes wordart from strings or someshizz"""
    
    def __init__(self, bot):
        self.bot = bot
        self.dictionary = PyDictionary()
        
       
    @commands.command()
    async def meaning(self, word:str):
        ret = self.dictionary.meaning(word)
        if ret is None:
            await self.bot.say(word+" not found.")
        else:
            await self.bot.say(ret)
        
        
    @commands.command()
    async def synonym(self, word:str):
        ret = self.dictionary.synonym(word)
        if ret is None:
            await self.bot.say(word+" not found.")
        else:
            await self.bot.say(ret)
    
    @commands.command()
    async def antonym(self, word:str):
        ret = self.dictionary.antonym(word)
        if ret is None:
            await self.bot.say(word+" not found.")
        else:
            await self.bot.say(ret)
    
    @commands.command()
    async def translate(self, word:str, lang:str):
        ret = self.dictionary.translate(word, lang)
        if ret is None:
            await self.bot.say(word+" not found.")
        else:
            await self.bot.say(ret)
        
def setup(bot):
    bot.add_cog(Dictionary(bot))
