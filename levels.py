import discord
from discord.ext import commands
from pagination import Pages

class Levels():
  def __init__(self, self.bot):
    self.self.bot = self.bot

  database = "experience" #database name used for exp
  # SQL SETUP------------------------------------------------------------------------------
  urllib.parse.uses_netloc.append("postgres")
  conn = psycopg2.connect("port='5432' user='zocnciwk' host='tantor.db.elephantsql.com' password='"+self.bot.postgrespass+"'")
  cur = conn.cursor()
  # SQL SETUP------------------------------------------------------------------------------
  # creating a 2D empty array for exp queues
  expQueue = []
  EXP_COOLDOWN_TIMER = 60 #seconds

  # used to update the queue
  async def update_exp():
    await self.bot.wait_until_ready()
    while not self.bot.is_closed:
      for i, item in enumerate(expQueue):
        if time.time() - item[1] >= EXP_COOLDOWN_TIMER:
          # print("entry expired")
          del expQueue[i]
        await asyncio.sleep(1)

  # Check if author is currently on cooldown
  def validate(message):
    for item in expQueue:
      if message.author.id == item[0]:
        # author on cooldown
        return False
    # author not on cooldown, add author id and current time to queue
    # print("entry added to queue")
    expQueue.append([message.author.id, time.time()])
    return True

  # handles adding new users and updating existing user exp to database
  async def add(message):
    database = 'experience'
    entry = db_select(database, message.author.id)
    if entry == None:
      # user not in database
      exp_amount = random.randint(15, 25)
      # print("entry added to db")
      db_insert(database, ['name', 'user_id', 'exp', 'level', 'true_experience'], [message.author.name, message.author.id, exp_amount, currentLevel(exp_amount), exp_amount])
    else:
      list(entry)
      changeInExp = random.randint(15, 25)
      if changeInLevel(changeInExp, entry[3], entry[4]) == 'levelup':
        # user's levelled up
        db_update(database, 'level', currentLevel(entry[3]), 'user_id', message.author.id)
        await self.bot.send_message(message.channel, "{} has leveled up to {}".format(message.author.name, currentLevel(entry[3])))

      # if changeInLevel(changeInExp, entry[3], entry[4]) == 'leveldown':
      #   # user's levelled down
        # db_update(database, 'level', currentLevel(entry[3]), 'user_id', message.author.id)
      # update user new experience
      # print("entry update exp")

      db_update(database, 'exp', entry[3]+changeInExp, 'user_id', message.author.id)
      db_update(database, 'true_experience', entry[3]+changeInExp, 'user_id', message.author.id)

  def changeInLevel(change, experience, currLevel):
    curr_experience = experience + change
    new_level = currentLevel(experience)
    if new_level > currLevel:
      # user has leveled up
      return 'levelup'

  # outputs closest level based on total experience
  def currentLevel(experience):
    if experience is 0:
      return 0
    # grab the template experience list from database
    cur.execute("SELECT level, total_experience FROM template ORDER BY level")
    templateList = cur.fetchall()
    for level in templateList:
      if experience <= level[1]:
        return level[0]-1
    # should never reach here, error out with -1
    self.bot.say("Something went wrong.")
    return -1

  # outputs current exp for level (not total exp)
  def currentExp(level, experience):
    cur.execute("SELECT total_experience FROM template WHERE level = {}".format(level))
    return experience - cur.fetchone()[0]

  # formula used to calculate exact experience needed for next level
  # x = level
  def calcLevel(x):
    return 5*math.pow(x, 2) + 50*x + 100

  @commands.command(pass_context = True)
  async def rank(ctx):
    if len(ctx.message.mentions) > 0:
      ctx.message.author = ctx.message.mentions[0]
    cur.execute('SELECT * FROM (SELECT *, row_number() OVER(ORDER BY exp DESC) FROM experience) AS filter WHERE filter.user_id={}'.format(ctx.message.author.id))
    res = list(cur.fetchone())
    cur.execute('SELECT count(*) from experience')
    totalUsers = cur.fetchone()[0]
    level = res[4]
    totalExperience = res[3]
    currentExperience = currentExp(level, totalExperience)
    rank = res[6]
    nextLevel = calcLevel(int(level))

    embed = discord.Embed(colour=discord.Colour(0x1d86c9))
    embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
    embed.set_footer(text="CSSS-Minion")
    embed.add_field(name="Rank", value="{}/{}".format(rank, totalUsers), inline=True)
    embed.add_field(name="Level", value=level, inline=True)
    embed.add_field(name="Experience", value="{} / {} XP [{} total]".format(int(currentExperience), int(nextLevel), int(totalExperience)), inline=True)
    await self.bot.say(embed=embed)

  @commands.command(pass_context = True)
  async def levels(ctx):
    cur.execute('SELECT * FROM (SELECT *, row_number() OVER(ORDER BY exp DESC) FROM experience) AS filter')
    res = list(cur.fetchall())
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
  def db_update(database, column, value, where, query):
    cur.execute("UPDATE {} SET {} = {} WHERE {} = {}".format(database, column, value, where, query))
    conn.commit()

  def db_insert(database, name, value):
    cur.execute("INSERT INTO {} ({}) VALUES ({})".format(database, ', '.join(str(n) for n in name), "'{0}'".format("','".join( str(v) for v in value))))
    conn.commit()

  def db_select(database, query, item = '*'):
    cur.execute("SELECT {} FROM {} WHERE user_id = ({})".format(', '.join(str(n) for n in item), database, query))
    return cur.fetchone()

def setup(self.bot):
  self.bot.add_cog(Levels(self.bot))
  self.bot.loop.create_task(update_exp())
