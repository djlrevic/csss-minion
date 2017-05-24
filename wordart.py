import discord
from discord.ext import commands
from wordcloud import WordCloud
from os import path
from psycopg2 import sql
import requests
import cv2
from PIL import Image
import numpy as np
from colour import Color
import io
import os
#opencv-python is a dependency 

#note to self... this will need refactoring one day. That day is not today.

class WordArt:
    tablename = "wordartMessages"
    backupArr = ['sad','oh no', 'terrible timing', 'broken', 'sad','sad', 'nuuu',':(', 'broken', 'sad','brokenhearted', 'next time?', 'database_down', 'database_down', 'database_down']
    STOPWORDS = set([x.strip() for x in open(os.path.join(os.path.dirname(__file__), 'stopwords.txt')).read().split('\n')])

    testimg = "testimg.png"
    d = path.dirname(__file__)
    e = "wordart_dir"
    serverCache = None
    serverImage = path.join(d,e, "server.png")
    
       
    def __init__(self, bot):
        self.bot = bot
        cur = self.bot.conn_wc.cursor()
        query = "CREATE TABLE IF NOT EXISTS "+self.tablename+"(user_id bigint, msgs varchar(2000), date text, UNIQUE(user_id, date))" # create table if doesn't exist
        cur.execute(query)
        self.bot.conn_wc.commit()
        cur.close()
        self.populateCaches()
    
    # populates a word and image cache for the server's wordcloud
    # calls are limited to __init__, nos, and henry
    def populateCaches(self):
        try:
            cur = self.bot.conn_wc.cursor()
            cur.execute("SELECT msgs FROM "+self.tablename+" LIMIT 2000") #yeah boy we're limiting
            entries = cur.fetchall()
            arr = []
            for i in range(0, len(entries)):
                arr.append(entries[i][0])
            if len(arr) < 1:
                self.serverCache = self.backupArr
            else:
                self.serverCache = arr
        except:
            print("server cache retrieval error")
            self.serverCache = self.backupArr
        text = " ".join(self.serverCache)
        wc = WordCloud(width=1024, height=1024, max_words=2000, stopwords=self.STOPWORDS).generate(text)
        wc.to_file(self.serverImage)
    
       
       
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
            return arr           
        except Exception as e:
            print("Something broke. Printing error message: ")
            print(e)
            return self.backupArr
        
    def createImage(self, arr, saveName):
        text = " ".join(arr)
        savedir = path.join(self.d,self.e, saveName) # local image gets overwritten each time. will this break if too many requests?
        wc = WordCloud(max_words=2000, stopwords=self.STOPWORDS).generate(text)
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

    @commands.command(pass_context=True)
    async def avatart(self, ctx, *args):
        """Make a wordcloud in the shape of your avatar.
        usage: !avatart <invert> <bgcolor>
        
        """
        await self.bot.say("```Making artwork "+str(ctx.message.author)+", hold your horses!```")
        fin_img = path.join(self.d,self.e,"fin.png")
        
        # this whole block is lol
        if len(args) >= 2:
            if args[0] == "yes" or args[0] == "true" or args[0] == "invert":
                thresh = cv2.THRESH_BINARY_INV
            else:
                thresh = cv2.THRESH_BINARY
            try:
                if Color(args[1]):
                    bg_colour = args[1]
            except:
                bg_colour = "white"
        elif len(args) == 1:
            try:
                if Color(args[0]):
                    bg_colour = args[0]
            except:
                bg_colour = "white"
            if args[0] == "yes" or args[0] == "true" or args[0] == "invert":
                thresh = cv2.THRESH_BINARY_INV
            else:
                thresh = cv2.THRESH_BINARY
        else:
            thresh = cv2.THRESH_BINARY
            bg_colour = "white"     
        ava = ctx.message.author.avatar_url # grab avatar URL
        try:
            if ava == "":
                print("there's no avatar for this user: "+str(ctx.message.author))
                await self.bot.say("```I can't make avatar art without an avatar you silly goose. But it's ok, I have something special for you.```")
                img = cv2.imread(path.join(self.d,self.e,"default_avatar.jpg"),1)
            else:
                img_data = requests.get(ava, stream=True).content #dl from dat url
                img = cv2.imdecode(np.frombuffer(img_data, np.uint8),1) # convert from string butter to uint8    
        
            img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # grayscale that motha
            ret,img_bw = cv2.threshold(img_gray,127,255, thresh) #threshold values
            scaled = cv2.resize(img_bw, (1024,1024), interpolation = cv2.INTER_LINEAR)
        
            word = self.wordsFromDB(ctx.message.author) # retrieve words from DB
            text = " ".join(word)
            avatar_mask = np.array(scaled) # create mask
            wc = WordCloud(background_color=bg_colour, max_words=20000,stopwords=self.STOPWORDS, mask=avatar_mask)
            wc.generate(text)
            wc.to_file(fin_img) # save masked wordart to file
            await self.bot.send_file(ctx.message.channel, fin_img)
        except:
            await self.bot.say("```Something has gone horribly wrong.```")
        


    # only refresh cache if an authorized ID
    @commands.command(pass_context=True)
    async def refreshCache(self, ctx):
        """Refresh the server wordart cache. Admin only."""
        if ctx.message.author.id == "173177975045488640" or ctx.message.author.id == "173702138122338305": #users authorized to refresh
            await self.bot.say("```Working...```")
            self.populateCaches()
            
            await self.bot.say("```Repopulated the caches my master```")
        else:
            await self.bot.say("```Bad boy! Down!```")


    @commands.command(pass_context=True)
    async def servart(self,ctx, *args):
        """Make a wordcloud out of the server's most common words."""
        await self.bot.send_file(ctx.message.channel, self.serverImage)

    @commands.command(pass_context=True)
    async def wordart(self,ctx):
        """Make a wordcloud out of your most common words."""
        words = self.wordsFromDB(ctx.message.author)
        filename = self.createImage(words, "wow.png")
        await self.bot.send_file(ctx.message.channel, filename)
        
def setup(bot):
    bot.add_cog(WordArt(bot))
