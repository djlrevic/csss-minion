import discord
import asyncio
from discord.ext import commands
import os, time, datetime



class RTBF:
  def __init__(self, bot):
    self.bot = bot
    self.queue = asyncio.Queue()
    main_loop = asyncio.get_event_loop()
    main_loop.create_task(self.looptons())  # start main async loop

  async def test(self):
    print(' ')


  async def looptons(self):
    while True:
      print('top of loop')
      channel, request_author = await self.queue.get()

      time_before = datetime.datetime.utcnow()
      time_after = None
      end_signal = False
      while not end_signal:
          print('inside loop')
          print('before loop')
          time_after, end_signal = await self.deleteme(channel, request_author, time_before, time_after)
          print('after loop')
          await asyncio.sleep(5)

  async def deleteme(self, channel, request_author, time_before, time_after):
    newtime = None
    end_signal = False
    try:
      async for msg in channel.history(limit=1000, before=time_before,after=time_after, reverse=True):
        if msg.author.id == request_author.id:
          await msg.delete()
          newtime = msg.created_at
            
    except discord.Forbidden:
      print('forbidden from this channel')
    except discord.HTTPException:
      print('http exception')
    print("No more messages to delete in", channel.name)
    print("Finished a loop of deleting messages")
    if newtime == time_after:
      print("resetting time_after", newtime, time_after)
      time_after = None  # reset
    else:
      time_after = newtime  # to delete the next 1000 messages
    if time_before - newtime < datetime.timedelta(minutes=5):
      end_signal = True
        # if the time_after and time_before are close enough, return a true end_signal
    print('exiting method')
    return time_after, end_signal


  async def forgetin(self, channels, request_author):
    for ch in channels:
      await self.queue.put((ch, request_author))

  async def forgetall(self, request_author):
    for ch in self.bot.get_guild(request_author.serverID).text_channels:
        await self.queue.put((ch, request_author))

    def is_bot_owner(self, m):
        m.author.id == self.bot.user.id
        print(m.author.id == self.bot.user.id)

  @commands.command(pass_context=True)
  async def test(self, ctx, *msg):
      await ctx.send("this was only a test")

  @commands.command(pass_context=True)
  async def forgetmein(self, ctx, *msg):
    channels = ctx.message.channel_mentions
    author = ctx.author
    await self.forgetin(channels, author)

def setup(bot):
    bot.add_cog(RTBF(bot))
