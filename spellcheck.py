import discord
import enchant
from discord.ext import commands

class Spellcheck:
    
    def __init__(self, bot, dictionary):
        self.bot = bot
        self.spchk = dictionary
        
        
    @commands.command()
    async def spell(self, word: str):
        if self.spchk.check(word):
            await self.bot.say("Yes! "+word+" is spelled correctly.")
        else:
            suggest = "Here are my suggestions for you: "
            for sgs in self.spchk.suggest(word):
                suggest += sgs +", "
            await self.bot.say(suggest)
        
        
def setup(bot):
    dictionary = enchant.Dict("en_US") # should crash here if no dictionary installed. See comments above
    bot.add_cog(Spellcheck(bot, dictionary))
