import discord
from discord.ext import commands
import requests
import datetime
import time
import asyncio
import sqlite3
import discord.client
import __main__
import sys

#TODO
#proper errors for unit types.
#add cron jobs
#stop isvan


class Remindme:

    def __init__(self, bot):
        self.bot = bot
        self.remindmelist = list()
        self.remindmedb = sqlite3.connect("remindmedb")
        c = self.remindmedb.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS remindme (user_id bigint, msg varchar(2000), datetime datetime, channel_id varchar(20))")
        self.remindmedb.commit()
        c.close()
        self.mass_populate()
        main_loop = asyncio.get_event_loop()
        await main_loop.create_task(self.loop_remindme())
        if __main__.__file__ == "bot.py":
            self.remindmechannel = "304837708650643459" #testing channel
        else:
            self.remindmechannel = "228761314644852736"  #production channel

    async def loop_remindme(self):
        """This loop is subscribed to check the time.
        note, the while loop might be redundant.

        """
        dt = datetime.datetime
        await asyncio.sleep(5)
        while True:
            #check time against items in loop
            now = dt.now().isoformat(' ')
            #print("checking for current remindmes")
            for item in self.remindmelist:
                #print(item)
                if now > item[2]:
                    await self.notify_user(item[0],item[1], item[3])
                    self.remindmelist.remove(item)
                    self.remove_from_db(item)
            await asyncio.sleep(5)

        # must pass in year, month, day for datetime.
    @commands.command(pass_context=True)
    async def remindme(self, ctx, *word:str):
        """remind the user to do some thing at some time.
        usage: !remindme "hang the cat to dry" 2017 8 5
        format: year month day [hour] [minute] [second]
        """
        time = self.parse_time(word[1:]) #ignore msg and parse the time
        msg = word[0]
        if False == time or None == time: # bad input
            await self.bot.say("I cannot remember this.\n.format: remindme (message) year month day [hour] [minute] [second]")
            return
        #add to long term queue. probably using sqlite.
        self.add_to_storage(ctx.message.author.id, msg, time, ctx.message.channel.id)
        #add to short term queue. probably using list.
        self.add_to_queue(ctx.message.author.id, msg, time, ctx.message.channel.id)
        #print(self.bot.get_user_info(173177975045488640))
        await self.bot.send_message(ctx.message.channel, "Remembering: "+msg+" until "+str(time) + " for "+ ctx.message.author.name)

    @commands.command(pass_context=True)
    async def remindmein(self, ctx, *word:str):
        """usage: remindmein 2 days 'do that thing'
        """
        unit = int(word[0])
        unittype = word[1]
        msg = " ".join(word[2:])
        if int(unit) > pow(2,32):
            print("unit too big for max size.")
            await self.bot.say("Your unit might be too big")
        time = await self.parse_time_relative(unit, unittype)
        if False == time:
            await self.bot.say("I cannot remember this.")
            return
        self.add_to_storage(ctx.message.author.id, msg, time, ctx.message.channel.id)
        self.add_to_queue(ctx.message.author.id, msg, time, ctx.message.channel.id)
        await self.bot.send_message(ctx.message.channel, "Remembering: "+msg+" until "+str(time)[:19] + " for "+ ctx.message.author.name)


    @commands.command(pass_context=True)
    async def allreminders(self, ctx):
        """list all the active reminders."""
        await self.bot.say(self.remindmelist)


    @commands.command(pass_context=True)
    async def myreminders(self, ctx):
        """list only user's reminders"""
        userid = int(ctx.message.author.id)
        userlist = list()
        for item in self.remindmelist:
            if item[0] == userid:
                userlist.append(item)
        await self.bot.say(userlist)



    async def notify_user(self, userid, msg, channel):
        """send the message to remind the user"""
        user = await self.bot.get_user_info(userid)
        #mgiht break here
        try:
            await self.bot.send_message(self.bot.get_channel(channel),user.mention+"\nReminder: "+msg)
        except:
            await self.bot.send_message(self.bot.get_channel(self.remindmechannel),user.mention+"\nReminder: "+msg)


    def mass_populate(self):
        """retrieve all reminders from SQLite database and populate queue."""
        c = self.remindmedb.cursor()
        c.execute("SELECT * FROM remindme")
        alist = c.fetchall()
        for item in alist:
            self.add_to_queue(item[0],item[1],item[2], item[3])
        c.close()


    def add_to_storage(self, userid, msg, time, channel):
        """store in database so you can populate later."""
        c = self.remindmedb.cursor()
        data = (userid, msg, time, channel)
        c.execute("INSERT INTO remindme VALUES (?,?,?,?)", data)
        self.remindmedb.commit()
        c.close()


    def add_to_queue(self, userid, msg, time, channel):
        """add to list so you can remember now."""
        self.remindmelist.append((userid, msg, time, channel))


    def remove_from_db(self, item):
        """delete entry from database once a user is reminded"""
        c = self.remindmedb.cursor()
        data = (item[0], item[1], item[2])
        c.execute("DELETE FROM remindme WHERE user_id = ? AND msg = ? AND datetime = ?", data)
        self.remindmedb.commit()
        c.close()



    def parse_time(self, times): # make this more impressive in the future
        """Take the non-standard input and decode into standard datetime format.
        Return the time, False if no translation."""
        length = len(times)
        if length < 3:
            return False
        elif length < 4:
            year, month, day = times
            return datetime.datetime(int(year),int(month),int(day)).isoformat(' ')
        elif length < 5:
            year, month, day, hour = times
            return datetime.datetime(int(year),int(month),int(day),int(hour)).isoformat(' ')
        elif length < 6:
            year, month, day, hour, minute = times
            return datetime.datetime(int(year),int(month),int(day),int(hour),int(minute)).isoformat(' ')
        elif length < 7:
            year, month, day, hour, minute, second = times
            return datetime.datetime(int(year),int(month),int(day),int(hour),int(minute),int(second)).isoformat(' ')
        else:
            year, month, day, hour, minute, second, microsecond = times
            return datetime.datetime(int(year),int(month),int(day),int(hour),int(minute),int(second),int(microsecond)).isoformat(' ')


    async def parse_time_relative(self, unit, unittype):
        now = datetime.datetime.now()
        unit = int(round(unit))
        if unittype == "year" or unittype == "years":
            future = now + datetime.timedelta(weeks=unit*12*4)
        elif unittype == "month" or unittype == "months":
            future = now + datetime.timedelta(weeks=unit*4)
        elif unittype == "week" or unittype == "weeks":
            future = now + datetime.timedelta(weeks=unit)
        elif unittype == "day" or unittype == "days":
            future = now + datetime.timedelta(days=unit)
        elif unittype == "hour" or unittype == "hours":
            future = now + datetime.timedelta(hours=unit)
        elif unittype == "minute" or unittype == "minutes":
            future = now + datetime.timedelta(minutes=unit)
        elif unittype == "second" or unittype == "seconds":
            future = now + datetime.timedelta(seconds=unit)
        else:
            print("There is no proper unit type, warning!")
            await self.bot.say("There is no proper unit type, warning!\nyear(s), month(s), week(s), day(s), hour(s), minute(s), and second(s) are accepted time units.")
            return False
            #future = now
        return future.isoformat(' ')


def setup(bot):
    bot.add_cog(Remindme(bot))
