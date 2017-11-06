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
            await self.bot.say("Give me a question!")
        elif len(args) > 9:
            # too many options
            await self.bot.say("Too many choices yo!")
        elif len(args) == 1:
            # just the question itself, hence by default assume y/n true/false
            question = await self.bot.say("Question: **"+ args[0] + "** (Y/N).")
            await self.bot.add_reaction(question, '👍')
            await self.bot.add_reaction(question, '👎')
            # await bot.add_reaction(question, '1\U000020e3') #example with unicode
        else:
            # actual question with choices
            print(len(args))
            choice = [0] * (len(args)-1)
            # creating individual options
            for i in range(1, len(args)):
                choice[i-1] = str(i)+". "+str(args[i])
            question = await self.bot.say("Question: **" + args[0] + "**" + "\n" + "\n".join(choice)) #use join to display array of strings in a list
            for i in range(1, len(args)):
                await self.bot.add_reaction(question, str(i)+'\U000020e3')

    @commands.command()
    async def playmsg(self, msg):
        """Change minion's playing message
        Usage: playing <msg>
        """
        await self.bot.change_presence(game = discord.Game(name=msg, type=0))

    @commands.command(pass_context=True)
    async def howoldami(self, ctx):
        """Display when you joined the server"""
        await self.bot.say("You joined this server on {}".format(ctx.message.author.joined_at))
        #calculate the difference between then and the current time
        currentTime = datetime.datetime.now()
        timeDifference = currentTime - ctx.message.author.joined_at
        #currently only returns days, because I'm too lazy to format the rest
        #and it doesn't feel particularly useful
        daysSinceJoining = timeDifference.days
        await self.bot.say("that was {} days ago".format(daysSinceJoining))

    @commands.command()
    async def wolf(self, *args):
        """Get wolfram alpha to help with your homework
        Usage: wolf <query>
        """
        res = wClient.query(" ".join(args))
        try:
            await self.bot.say("```"+(next(res.results).text)+"```")
        except AttributeError:
            await self.bot.say("I ain't found shit.")

def setup(bot):
    # bot.config.read("botMain.settings")
    # wolframid = bot.config.get("Wolfram", "TokenId")
    bot.add_cog(Misc(bot, bot.wolframid))
