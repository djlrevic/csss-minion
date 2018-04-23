#pylint: disable=C
import discord
from discord.ext import commands
import wolframalpha

class Misc():
    def __init__(self, bot, wolframid):
        self.bot = bot
        global wClient
        wClient = wolframalpha.Client(wolframid)

    @commands.command(pass_context=True)
    async def poll(self, ctx, *args):
        """Create an instant poll
        Usage: poll <subject> [choices]...
        Defaults to yes/no if no choices supplied.
        """
        if len(args) == 0:
            # no question
            await ctx.send("Give me a question!")
        elif len(args) > 9:
            # too many options
            await ctx.send("Too many choices yo!")
        elif len(args) == 1:
            # just the question itself, hence by default assume y/n true/false
            question = await ctx.send("Question: **" + args[0] + "** (Y/N).")
            await question.add_reaction('👍')
            await question.add_reaction('👎')
            # await bot.add_reaction(question, '1\U000020e3') #example with unicode
        else:
            # actual question with choices
            print(len(args))
            choice = [0] * (len(args)-1)
            # creating individual options
            for i in range(1, len(args)):
                choice[i-1] = str(i)+". "+str(args[i])
            question = await ctx.send("Question: **" + args[0] + "**" + "\n" + "\n".join(choice)) #use join to display array of strings in a list
            for i in range(1, len(args)):
                await question.add_reaction(str(i)+'\U000020e3')

    @commands.command(pass_context=True)
    async def playmsg(self, ctx, msg):
        """Change minion's playing message
        Usage: playing <msg>
        """
        game = discord.Game(name=str(msg))
        await self.bot.change_presence(status=discord.Status.online, game=game)
        #await self.bot.change_presence(game=discord.Game(name=msg, type=0), afk=False)

    @commands.command(pass_context=True)
    async def howoldami(self, ctx):
        """Display when you joined the server"""
        await ctx.send("You joined this server on {}".format(ctx.message.author.joined_at))

    @commands.command(pass_context=True)
    async def wolf(self, ctx, *args):
        """Get wolfram alpha to help with your homework
        Usage: wolf <query>
        """
        res = wClient.query(" ".join(args))
        try:
            await ctx.send("```"+(next(res.results).text)+"```")
        except AttributeError:
            await ctx.send("I ain't found shit.")

def setup(bot):
    # bot.config.read("botMain.settings")
    # wolframid = bot.config.get("Wolfram", "TokenId")
    #bot.add_cog(Misc(bot))
    bot.add_cog(Misc(bot, bot.wolframid))
