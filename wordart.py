import discord
from discord.ext import commands
from wordcloud import WordCloud
from os import path
from psycopg2 import sql


class WordArt:
    tablename = "wordartMessages"
    createTableQuery = "CREATE TABLE IF NOT EXISTS "+tablename+" (user_id int, msgs varchar(2000), date datetime, UNIQUE(user_id,date))"
    backupArr = ['sad','oh no', 'terrible timing', 'broken', 'sad','sad', 'nuuu',':(', 'broken', 'sad','brokenhearted', 'next time?']
    backupArr2 = ['wow','wow','nice','wholesome','doggo','neat','nice','kittens','cool','coolstuff']
    
    insertTableQuery = "INSERT INTO "+tablename+" VALUES ('%s', '%s', '%s')" #INCOMPLETE
    #ctx.message.author.id, ctx.message.content, ctx.message.timestamp
    queryTableQuery = "SELECT * FROM "+tablename+" WHERE user_id = '%s'" #works in sqlite <shrugs>
    
    testimg = "testimg.png"
    d = path.dirname(__file__)
    e = "wordart_dir"
    
       # create table if doesn't exist
    def __init__(self, bot):
        self.bot = bot
        cur = self.bot.conn_wc.cursor()
       # query = "CREATE TABLE IF NOT EXISTS "+self.tablename+"(user_id int, msgs text, date text)"
        query = "CREATE TABLE IF NOT EXISTS "+self.tablename+"(user_id bigint, msgs varchar(2000), date text, UNIQUE(user_id, date))"
        cur.execute(query)
        self.bot.conn_wc.commit()
        cur.close() #??? necessary?
       
       
       # open DB and retrieve messages from a userID
    def wordsFromDB(self, author):
        try:
            cur = self.bot.conn_wc.cursor() # USE NEW CURSOR FOR NEW THREAD
            cur.execute("SELECT msgs FROM "+self.tablename+" WHERE user_id = '%s'"% str(author.id))
            entries = cur.fetchall()
            cur.close()
            arr = []
            for i in range(0, len(entries)):
                arr.append(entries[i][0])
            #for j in entries:
            #    arr.append(j[0])
            #print(arr)
            return arr           
        except Exception as e:
            print("Something broke. Printing error message: ")
            print(e)
            return backupArr
        
    def createImage(self, arr):
        text = " ".join(arr)
        savedir = path.join(self.d,self.e, "wow.png")
        wc = WordCloud().generate(text)
        wc.to_file(savedir)
        return savedir
        
        
        # idk how it subscribes to the event... but it works!
    async def on_message(self, message):   
        cur = self.bot.conn_wc.cursor()
        query = "INSERT INTO "+self.tablename+" VALUES (%s,%s,%s)"
        data = (message.author.id, message.content, message.timestamp)
        cur.execute(query, data)
        self.bot.conn_wc.commit()
        cur.close()
        
        #test function, destroy later
    @commands.command(pass_context=True)
    async def upPic(self,ctx):
        await self.bot.send_file(ctx.message.channel, self.testimg)


    @commands.command(pass_context=True)
    async def wordart(self,ctx):
        words = self.wordsFromDB(ctx.message.author)
        filename = self.createImage(words)
        await self.bot.send_file(ctx.message.channel, filename)
        
def setup(bot):
    bot.add_cog(WordArt(bot))
