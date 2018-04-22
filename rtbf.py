import discord
import asyncio
from discord.ext import commands
import os, time, datetime


class RTBF:
  def __init__(self, bot):
    self.bot = bot
    self.queue = asyncio.queue()
    main_loop = asyncio.get_event_loop()
    main_loop.create_task(looptons()) #start main async loop
    
    async def looptons():
        while True:
            channel, request_author = await self.queue.get()
            
            
            time_before = datetime.datetime.utcnow()
            end_signal = False
            while not end_signal:
                
                print('before loop')
                time_after, end_signal = await deleteme(channel, request_author, time_before, time_after)
                print('after loop')
                await asyncio.sleep(5)
    
    
    
    #main async loop 
    async def looptons():
        time_after = None
        while True:
            time_before = datetime.datetime.utcnow() - datetime.timedelta(minutes=30)
            print('before loop')
            time_after = await deleteme(channel, request_author, time_before, time_after)
            print('after loop')
            await asyncio.sleep(5)
    
    
    async def deleteme(channel, request_author, time_start, time_end):
        newtime = None
        try:
            async for msg in channel.history(limit=1000, before=time_before,after=time_after, reverse=True):
                if msg.author.id == request_author.id:
                    await msg.delete()
                newtime = msg.created_at
            
        except discord.Forbidden:
            print('forbidden from this channel')
        except discord.HTTPException:
            print('http exception')
        print("No more messages to delete in", ch.name)
        print("Finished a loop of deleting messages")
        if newtime == time_after:
            print("resetting time_after", newtime, time_after)
            time_after = None #reset
        else:
            time_after = newtime # to delete the next 1000 messages
        if(time_before - newtime < datetime.timedelta(minutes=5)
            end_signal = True
        #if the time_after and time_before are close enough, return a true end_signal
        return (time_after, end_signal)
    



    async def forgetin(channels, request_author):
        for ch in channels:
            await self.queue.put((ch, request_author))
            
            """
            print("attempting to delete messages in: ", ch.name)
            try:
                async for msg in ch.history(limit=None, reverse=True):
                    if msg.author.id == request_author.id:
                        await msg.delete()
            
            except discord.Forbidden:
                print('forbidden from this channel')
            except discord.HTTPException:
                print('http exception')
            print("No more messages to delete in", ch.name)
            """    

    async def forgetall(request_author):
        for ch in self.bot.get_guild(serverID).text_channels:
            await self.queue.put((ch, request_author))
            
            """
            print("attempting to delete messages in: ", ch.name)
            try:
                async for msg in ch.history(limit=None, reverse=True):
                    if msg.author.id == request_author.id:
                        await msg.delete()
            
            except discord.Forbidden:
                print('forbidden from this channel')
            except discord.HTTPException:
                print('http exception')
            print("No more messages to delete in", ch.name)
	"""


    def is_bot_owner(m):
        m.author.id == bot.user.id
        print(m.author.id == bot.user.id)

    @commands.command(pass_context=True)
    async def test(ctx, *msg):
        await ctx.channel.say("this was only a test")

    @commands.command(pass_context=True)
    async def forgetmein(ctx, *msg):
        channels = ctx.message.channel_mentions
        author = ctx.author
        forgetin(channels, author)
        
        
        
