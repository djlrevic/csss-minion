import discord
from discord.ext import commands
import pprint
from pagination import Pages
import inspect

class Devtools:
  def __init__(self, bot):
    self.bot = bot

  @commands.command(pass_context=True)
  async def inspect(self, ctx):
    for role in ctx.message.author.roles:
      if self.bot.Henry(ctx) or role.id == 321832268282855436: #bot devs
        theObject = None
        if len(ctx.message.mentions) > 0:
          theObject = ctx.message.mentions[0]
        elif len(ctx.message.channel_mentions) > 0:
          theObject = ctx.message.channel_mentions[0]
        elif len(ctx.message.role_mentions) > 0:
          theObject = ctx.message.role_mentions[0]
        else:
          await ctx.send("I didn't understand what you are inspecting.")

        if theObject is not None:
          items = []
          dictionary = [x for x in dir(theObject) if not x.startswith('_')]
          for name in dictionary:
            attr = getattr(theObject, name)
            if 'object' not in str(attr) and 'method' not in str(attr):
              items.append([str(name), str(attr), False])
          p = Pages(self.bot, ctx=ctx, message=ctx.message, entries = items, per_page=10)
          p.embed = discord.Embed(title="Inspection Results", colour=discord.Colour(0xdc4643))
          p.embed.set_thumbnail(url="https://cdn.discordapp.com/app-icons/293110345076047893/15e2a6722723827ff9bd53ca787df959.jpg")
          p.embed.set_author(name="CSSS-Minion", icon_url="https://cdn.discordapp.com/app-icons/293110345076047893/15e2a6722723827ff9bd53ca787df959.jpg")
          p.embed.set_footer(text="CSSS-Minion", icon_url="https://cdn.discordapp.com/app-icons/293110345076047893/15e2a6722723827ff9bd53ca787df959.jpg")

          await p.paginate()
      else:
        await ctx.send("You not a dev, shoo!")

def setup(bot):
  bot.add_cog(Devtools(bot))
