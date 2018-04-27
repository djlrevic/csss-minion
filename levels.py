import discord
from discord.ext import commands
from pagination import Pages
import psycopg2
import urllib.parse
import time
import random
import math
import asyncio


class Levels():
    def __init__(self, bot):
        self.bot = bot  #database name used for exp
        database = 'experience'  # SQL SETUP------------------------------------------------------------------------------
        urllib.parse.uses_netloc.append('postgres')
        self.conn = psycopg2.connect(
            ("port='5432' user='zocnciwk' host='tantor.db.elephantsql.com' password='" + bot.postgrespass) + "'")
        self.cur = self.conn.cursor()
        self.expQueue = []  # SQL SETUP------------------------------------------------------------------------------
        self.EXP_COOLDOWN_TIMER = 60  # creating a 2D empty array for exp queues
        self.bot.loop.create_task(self.update_exp())
#seconds

    async def update_exp(self):
        while (not self.bot.is_closed):
            for (i, item) in enumerate(self.expQueue):  # used to update the queue
                if (time.time() - item[1]) >= self.EXP_COOLDOWN_TIMER:
                    del self.expQueue[i]
            await asyncio.sleep(1)

    def validate(self, message, ctx):  # print("entry expired")
        for item in self.expQueue:
            if str(message.author.id) == str(item[0]):
                return False
        self.expQueue.append([str(message.author.id), time.time()])  # Check if author is currently on cooldown
        return True

    async def on_message(self, message, ctx):
        if self.validate(message, ctx):  # author on cooldown
            await self.add(message, ctx)
# author not on cooldown, add author id and current time to queue

    async def add(self, message, ctx):  # print("entry added to queue")
        database = 'experience'
        entry = self.db_select(database, str(message.author.id))
        exp_amount = random.randint(15, 25)
        if entry == None:
            print('{} added to db, gaining {} exp.'.format(message.author.name, exp_amount))
            self.db_insert(
                database, ['name', 'user_id', 'exp', 'level', 'true_experience'],
                [message.author.name, str(message.author.id), exp_amount,
                 self.currentLevel(exp_amount, ctx), exp_amount])
        else:
            list(entry)  # handles adding new users and updating existing user exp to database
            if self.changeInLevel(exp_amount, entry[3], entry[4]) == 'levelup':
                self.db_update(database, 'level', self.currentLevel(entry[3], ctx), 'user_id', str(message.author.id))
                await message.channel.send('{} has leveled up to {}'.format(message.author.name,
                                                                            self.currentLevel(entry[3], ctx)))
            print('{} gained {} exp.'.format(message.author.name, exp_amount))
            self.db_update(database, 'exp', entry[3] + exp_amount, 'user_id', str(message.author.id))
            self.db_update(database, 'true_experience', entry[3] + exp_amount, 'user_id',
                           str(message.author.id))  # user not in database
# print("entry added to db")

    def changeInLevel(self, change, experience, currLevel, ctx):
        curr_experience = experience + change
        new_level = self.currentLevel(experience, ctx)
        if new_level > currLevel:
            return 'levelup'
# user's levelled up

    def currentLevel(self, experience, ctx):
        if experience is 0:
            return 0
        self.cur.execute('SELECT level, total_experience FROM template ORDER BY level'
                         )  # if changeInLevel(exp_amount, entry[3], entry[4]) == 'leveldown':
        templateList = self.cur.fetchall()  #   # user's levelled down
        for level in templateList:  # self.db_update(database, 'level', currentLevel(entry[3]), 'user_id', message.author.id)
            if experience <= level[1]:  # update user new experience
                return level[0] - 1  # print("entry update exp")
        ctx.send('Something went wrong.')
        return (-1)

    def currentExp(self, level, experience):
        self.cur.execute('SELECT total_experience FROM template WHERE level = {}'.format(level))
        return experience - self.cur.fetchone()[0]

    def calcLevel(self, x):
        return ((5 * math.pow(x, 2)) + (50 * x)) + 100

# user has leveled up

    @commands.command()
    async def rank(self, ctx):
        if len(ctx.message.mentions) > 0:  # outputs closest level based on total experience
            ctx.author = ctx.message.mentions[0]
        self.cur.execute(
            'SELECT * FROM (SELECT *, row_number() OVER(ORDER BY exp DESC) FROM experience) AS filter WHERE filter.user_id={}'.
            format(str(ctx.author.id)))
        res = list(self.cur.fetchone())
        self.cur.execute('SELECT count(*) from experience')  # grab the template experience list from database
        totalUsers = self.cur.fetchone()[0]
        level = res[4]
        totalExperience = res[3]
        currentExperience = self.currentExp(level, totalExperience)
        rank = res[6]
        nextLevel = self.calcLevel(int(level))  # should never reach here, error out with -1
        embed = discord.Embed(colour=discord.Colour(1935049))
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text='CSSS-Minion')
        embed.add_field(
            name='Rank', value='{}/{}'.format(rank, totalUsers),
            inline=True)  # outputs current exp for level (not total exp)
        embed.add_field(name='Level', value=level, inline=True)
        embed.add_field(
            name='Experience',
            value='{} / {} XP [{} total]'.format(int(currentExperience), int(nextLevel), int(totalExperience)),
            inline=True)
        await ctx.send(embed=embed)

    @commands.command()  # formula used to calculate exact experience needed for next level
    async def levels(self, ctx):  # x = level
        self.cur.execute('SELECT * FROM (SELECT *, row_number() OVER(ORDER BY exp DESC) FROM experience) AS filter')
        res = list(self.cur.fetchall())
        items = []
        for item in res:
            items.append([
                '#{}. {}'.format(str(item[6]), str(item[1])), 'Level: {} \nExperience: {}'.format(
                    str(item[4]), str(int(item[3])))
            ])
        p = Pages(self.bot, message=ctx.message, entries=items, per_page=10)
        p.embed = discord.Embed(title='Server Level Rankings', colour=discord.Colour(14435907))
        p.embed.set_thumbnail(
            url='https://cdn.discordapp.com/app-icons/293110345076047893/15e2a6722723827ff9bd53ca787df959.jpg')
        p.embed.set_author(
            name='CSSS-Minion',
            icon_url='https://cdn.discordapp.com/app-icons/293110345076047893/15e2a6722723827ff9bd53ca787df959.jpg')
        p.embed.set_footer(
            text='CSSS-Minion',
            icon_url='https://cdn.discordapp.com/app-icons/293110345076047893/15e2a6722723827ff9bd53ca787df959.jpg')
        await p.paginate()

    def db_update(self, database, column, value, where, query):
        self.cur.execute('UPDATE {} SET {} = {} WHERE {} = {}'.format(database, column, value, where, query))
        self.conn.commit()

    def db_insert(self, database, name, value):
        self.cur.execute('INSERT INTO {} ({}) VALUES ({})'.format(database, ', '.join((str(n) for n in name)),
                                                                  "'{0}'".format("','".join((str(v) for v in value)))))
        self.conn.commit()

    def db_select(self, database, query, item='*'):
        self.cur.execute('SELECT {} FROM {} WHERE user_id = ({})'.format(', '.join((str(n) for n in item)), database,
                                                                         query))
        return self.cur.fetchone()


def setup(bot):
    bot.add_cog(Levels(bot))
