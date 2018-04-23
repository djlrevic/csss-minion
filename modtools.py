import discord
import asyncio
from discord.ext import commands

AVOID = ['342891382584770560', '300564141096304650', '360722519860445184', '312038519294001152', '321832332279676928']

class Modtools:
  def __init__(self, bot):
    self.bot = bot
    self.muted_role = 349848771007348738  # for testing server
    # self.muted_role =  # for csss server



  def purge_predicate(self, message):
      """A check on each message to be purged."""
      return self.minion(message.author)

  # will delete the mentioned person's messages
  @commands.command(pass_context=True)
  async def purge(self, ctx, *msg):
      return False  # disable command for now
      await ctx.send('test')
      #ch = ctx.message.mentions[0]
      await ctx.channel.purge(check=self.purge_predicate)
      await ctx.send('done')




  
  # Adds the "muted" permissions to all channels
  @commands.command(pass_context=True)
  async def propagateMute(self, ctx):
    if self.bot.Henry(ctx):
      for role in ctx.message.server.roles:
        if role.id == self.muted_role:
          MUTED_ROLE = role

      overwrite = discord.PermissionOverwrite()
      setattr(overwrite, 'send_messages', False)
      setattr(overwrite, 'manage_messages', False)
      setattr(overwrite, 'manage_channels', False)
      setattr(overwrite, 'manage_server', False)
      setattr(overwrite, 'manage_nicknames', False)
      setattr(overwrite, 'manage_roles', False)
      for channel in ctx.message.server.channels:
        if channel.id not in AVOID:
          await self.bot.edit_channel_permissions(channel, MUTED_ROLE, overwrite)

#  @commands.command(pass_context=True)
#  async def lock(self, ctx):
#    """Locks the current channel."""
#    for role in ctx.message.server.roles:
#      if role.id == '338575090847580160':
#        MUTED_ROLE = role
#      if role.id == '296466915235332106':
#        BOTS_ROLE = role
#    if self.minion(ctx):
#      everyone = []
#      for user in ctx.message.server.members:
#        if ctx.message.channel.permissions_for(user).send_messages and BOTS_ROLE not in user.roles: #don't mute bots
#          everyone.append(user)
#      for user in everyone:
#        await self.bot.add_roles(user, MUTED_ROLE)
#      await self.bot.say("Locking Channel")
#    else:
#      await self.bot.say("You ain't no mod, shoo!")



  @commands.command(pass_context=True)
  async def unlock(self, ctx):
    """Unlocks the current channel."""
    if self.minion(ctx.message.author):
        for role in ctx.message.guild.roles:
            if role.id == self.muted_role:
                MUTED_ROLE = role
        everyone = []
        for user in ctx.message.guild.members:
            if ctx.message.channel.permissions_for(user).send_messages:
                everyone.append(user)
        for user in everyone:
            if MUTED_ROLE in user.roles:
                await self.bot.remove_roles(user, MUTED_ROLE)
        await ctx.send("Unlocking Channel")
    else:
      await ctx.send("You ain't no mod, shoo!")

  async def ch_perms(self, channel, user, value):
    """Helper function"""
    overwrite = discord.PermissionOverwrite()
    overwrite.send_messages = value
    await self.bot.edit_channel_permissions(channel, user, overwrite)

  @commands.command(pass_context=True)
  async def unrestrict(self, ctx, *msg):
    """Undo any restrictions on a user for all channels.
    Usage: !unrestrict [users..]
    Removes the MUTED role from a user
    """
    if self.minion(ctx.message.author):
      for role in ctx.message.guild.roles:
        if role.id == self.muted_role:
          MUTED_ROLE = role
      channels = ctx.message.guild.channels
      for user in ctx.message.mentions:
        await ctx.send("Unrestricting user "+user.name)
        for ch in channels:
          await ctx.message.mentions[0].remove_roles(MUTED_ROLE, reason='no longer being a dingus')
          #await self.ch_perms(ch, user, None) #None sets to default(inherited) value.
    else:
      await ctx.send("You ain't no mod, shoo!")

  @commands.command(pass_context=True)
  async def restrict(self, ctx):
    """Basically just gives the MUTED role to a user"""
    if self.minion(ctx.message.author):  # only runs if the command issuer is a minion
      for role in ctx.message.guild.roles:
        if role.id == self.muted_role:
          MUTED_ROLE = role
      await ctx.message.mentions[0].add_roles(MUTED_ROLE, reason='for being dumb')
      await ctx.send("{} has been muted.".format(ctx.message.mentions[0].mention))
    else:
      await ctx.send("You ain't no mod, shoo!")

  def minion(self, author):
    for role in author.roles:
      if 349833623463002113 == role.id: # testing server
      #if "314296819272122368" == role.id:  # csss server
        return True
    return False

  @commands.command(pass_context=True)
  async def modsay(self, ctx, *msg):
    """Give a stern message.
       Heavily inspired by brenfan's .em code <3
    """
    author = ctx.message.author
    if author.permissions_in(ctx.message.channel).manage_channels or author.server_permissions.manage_channels:

      try:
        color = red
      except Exception:
        color = discord.Colour(0xff0000)
      string = "\n\n["+" ".join(msg)+"]()"
      embed = discord.Embed(description = string, color = color, title="An Echo From the Heavens Says...", footer="Moderator Warning")
      embed.set_author(name=author.display_name, icon_url = author.avatar_url)
      embed.set_footer(text="Moderator Warning")
      await ctx.send(embed=embed)
    try:
      await self.bot.delete_message(ctx.message)
    except Exception:
      print("Not allowed to delete message")

  @commands.command(pass_context=True)
  async def clear(self, ctx, amount):
    """Clear set amount of messages
    """
    if len(ctx.message.mentions) > 0:
      send_msg = await ctx.send("Feature coming. Bug Henry.")
      # await self.bot.purge_from(ctx.message.channel, limit = 50, check=is_me)
    else:
      if(str.isdigit(amount)):
        await ctx.channel.purge(limit=int(amount))
        send_msg = await ctx.send("{} message(s) has been deleted.".format(amount))

    await asyncio.sleep(3)
    await send_msg.delete()

def setup(bot):
  bot.add_cog(Modtools(bot))
