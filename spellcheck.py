import discord
import enchant
from discord.ext import commands

class Spellcheck:
    
    def __init__(self, bot, dictionary):
        self.bot = bot
        self.spchk = dictionary
        
        
    @commands.command(pass_context=True)
    async def spell(self,ctx, word: str):
        """Check your spelling"""
        if self.spchk.check(word):
            #await self.bot.say("Yes! "+word+" is spelled correctly.")
            await self.bot.embed_this_for_me("Yes! *"+word+"* is spelled correctly!",ctx)
        else:
            suggest = "Here are my suggestions for you: "
            for sgs in self.spchk.suggest(word):
                suggest += sgs +", "
#            await self.bot.say(suggest)
            await self.bot.embed_this_for_me(suggest,ctx)
        
        
def setup(bot):
    dictionary = enchant.Dict("en_US") # should crash here if no dictionary installed. See comments above
    bot.add_cog(Spellcheck(bot, dictionary))
