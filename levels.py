import discord
from discord.ext import commands
from pagination import Pages
import psycopg2
import urllib.parse
import time
import random
import math
import asyncio

class Levels:
  def __init__(self, bot):
    self.bot = bot
    database = "experience" #database name used for exp
    # SQL SETUP------------------------------------------------------------------------------
    urllib.parse.uses_netloc.append("postgres")
    self.conn = psycopg2.connect("port='5432' user='zocnciwk' host='tantor.db.elephantsql.com' password='"+bot.postgrespass+"'")
    self.cur = self.conn.cursor()
    # SQL SETUP------------------------------------------------------------------------------
    # creating a 2D empty array for exp queues
    self.expQueue = []
    self.EXP_COOLDOWN_TIMER = 60 #seconds
    self.bot.loop.create_task(self.update_exp())

  # used to update the queue
  async def update_exp(self):
    while not self.bot.is_closed:
      for i, item in enumerate(self.expQueue):
        if time.time() - item[1] >= self.EXP_COOLDOWN_TIMER:
          # print("entry expired")
          del self.expQueue[i]
      await asyncio.sleep(1)

  # Check if author is currently on cooldown
  def validate(self, message):
    for item in self.expQueue:
      if message.author.id == item[0]:
        # author on cooldown
        return False
    # author not on cooldown, add author id and current time to queue
    # print("entry added to queue")
    self.expQueue.append([message.author.id, time.time()])
    return True

  async def on_message(self, message):
    if self.validate(message):
      await self.add(message)

  # handles adding new users and updating existing user exp to database
  async def add(self, message):
    database = 'experience'
    entry = self.db_select(database, message.author.id)
    exp_amount = random.randint(15, 25)
    if entry == None:
      # user not in database
      # print("entry added to db")
      print('{} added to db, gaining {} exp.'.format(message.author.name, exp_amount))
      self.db_insert(database, ['name', 'user_id', 'exp', 'level', 'true_experience'], [message.author.name, message.author.id, exp_amount, self.currentLevel(exp_amount), exp_amount])
    else:
      list(entry)
      if self.changeInLevel(exp_amount, entry[3], entry[4]) == 'levelup':
        # user's levelled up
        self.db_update(database, 'level', self.currentLevel(entry[3]), 'user_id', message.author.id)
        await self.bot.send_message(message.channel, "{} has leveled up to {}".format(message.author.name, self.currentLevel(entry[3])))

      # if changeInLevel(exp_amount, entry[3], entry[4]) == 'leveldown':
      #   # user's levelled down
        # self.db_update(database, 'level', currentLevel(entry[3]), 'user_id', message.author.id)
      # update user new experience
      # print("entry update exp")

      print('{} gained {} exp.'.format(message.author.name, exp_amount))
      self.db_update(database, 'exp', entry[3]+exp_amount, 'user_id', message.author.id)
      self.db_update(database, 'true_experience', entry[3]+exp_amount, 'user_id', message.author.id)

  def changeInLevel(self, change, experience, currLevel):
    curr_experience = experience + change
    new_level = self.currentLevel(experience)
    if new_level > currLevel:
      # user has leveled up
      return 'levelup'

  # outputs closest level based on total experience
  def currentLevel(self, experience):
    if experience is 0:
      return 0
    # grab the template experience list from database
    self.cur.execute("SELECT level, total_experience FROM template ORDER BY level")
    templateList = self.cur.fetchall()
    for level in templateList:
      if experience <= level[1]:
        return level[0]-1
    # should never reach here, error out with -1
    self.bot.say("Something went wrong.")
    return -1

  # outputs current exp for level (not total exp)
  def currentExp(self, level, experience):
    self.cur.execute("SELECT total_experience FROM template WHERE level = {}".format(level))
    return experience - self.cur.fetchone()[0]

  # formula used to calculate exact experience needed for next level
  # x = level
  def calcLevel(self, x):
    return 5*math.pow(x, 2) + 50*x + 100

  @commands.command(pass_context = True)
  async def rank(self, ctx):
    if len(ctx.message.mentions) > 0:
      ctx.message.author = ctx.message.mentions[0]
    self.cur.execute('SELECT * FROM (SELECT *, row_number() OVER(ORDER BY exp DESC) FROM experience) AS filter WHERE filter.user_id={}'.format(ctx.message.author.id))
    res = list(self.cur.fetchone())
    self.cur.execute('SELECT count(*) from experience')
    totalUsers = self.cur.fetchone()[0]
    level = res[4]
    totalExperience = res[3]
    currentExperience = self.currentExp(level, totalExperience)
    rank = res[6]
    nextLevel = self.calcLevel(int(level))

    embed = discord.Embed(colour=discord.Colour(0x1d86c9))
    embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
    embed.set_footer(text="CSSS-Minion")
    embed.add_field(name="Rank", value="{}/{}".format(rank, totalUsers), inline=True)
    embed.add_field(name="Level", value=level, inline=True)
    embed.add_field(name="Experience", value="{} / {} XP [{} total]".format(int(currentExperience), int(nextLevel), int(totalExperience)), inline=True)
    await self.bot.say(embed=embed)

  @commands.command(pass_context = True)
  async def levels(self, ctx):
    self.cur.execute('SELECT * FROM (SELECT *, row_number() OVER(ORDER BY exp DESC) FROM experience) AS filter')
    res = list(self.cur.fetchall())
    # print(res)
    items = []
    for item in res:
      items.append(['#{}. {}'.format(str(item[6]), str(item[1])), 'Level: {} \nExperience: {}'.format(str(item[4]), str(int(item[3])))])

    p = Pages(self.bot, message=ctx.message, entries = items, per_page=10)
    p.embed = discord.Embed(title="Server Level Rankings", colour=discord.Colour(0xdc4643))
    p.embed.set_thumbnail(url="https://cdn.discordapp.com/app-icons/293110345076047893/15e2a6722723827ff9bd53ca787df959.jpg")
    p.embed.set_author(name="CSSS-Minion", icon_url="https://cdn.discordapp.com/app-icons/293110345076047893/15e2a6722723827ff9bd53ca787df959.jpg")
    p.embed.set_footer(text="CSSS-Minion", icon_url="https://cdn.discordapp.com/app-icons/293110345076047893/15e2a6722723827ff9bd53ca787df959.jpg")

    await p.paginate()

  # database accessors ----------------------------------------------------------------------------
  def db_update(self, database, column, value, where, query):
    self.cur.execute("UPDATE {} SET {} = {} WHERE {} = {}".format(database, column, value, where, query))
    self.conn.commit()

  def db_insert(self, database, name, value):
    self.cur.execute("INSERT INTO {} ({}) VALUES ({})".format(database, ', '.join(str(n) for n in name), "'{0}'".format("','".join( str(v) for v in value))))
    self.conn.commit()

  def db_select(self, database, query, item = '*'):
    self.cur.execute("SELECT {} FROM {} WHERE user_id = ({})".format(', '.join(str(n) for n in item), database, query))
    return self.cur.fetchone()

def setup(bot):
  bot.add_cog(Levels(bot))
