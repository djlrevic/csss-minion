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
import time
import asyncio
import decimal
from collections import Counter
#opencv-python is a dependency 

#note to self... this will need refactoring one day. That day is not today.

query_spam_reduction = """ WITH numbers AS
(
         SELECT   date,
                  Count(DISTINCT r)
         FROM     (
                         SELECT date,
                                unnest(regexp_split_to_array(msgs, e'\\s+')) AS r
                         FROM   "public"."wordartmessages") c
         GROUP BY date
         HAVING   count(distinct r) = 1)
DELETE
FROM   wordartmessages
WHERE  date IN
       (
              SELECT date
              FROM   numbers) """



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
        start = time.time()
        self.bot = bot
        cur = self.bot.conn_wc.cursor()
        
        query = "CREATE TABLE IF NOT EXISTS "+self.tablename+"(user_id bigint, msgs varchar(2000), date text, UNIQUE(user_id, date))" # create table if doesn't exist
        try:
            cur.execute(query)
        except Exception as e: # idk what could go wrong here, so catch all errors and print
            print("Could not create wordart table, something really bad happened.", e)
        self.bot.conn_wc.commit()
        cur.close()
        print("Populating caches, prepare for major lagspike")
        self.populateCaches()
        print("wordart took "+str(time.time()-start)+" seconds to initalize.")
    
    @commands.command(pass_context=True)
    async def clearspam(self, ctx):
        cur = self.bot.conn_wc.cursor()
        msg = await self.bot.say("Clearing the spam your mightyness")
       # cur.callproc('spam_reduction')
        try:
            cur.execute(query_spam_reduction)
        except Exception as e:# idk what could go wrong here, so catch all errors and print
            print("Could not execute spam reduction query. omg what happened?", e)
        self.bot.conn_wc.commit()
        cur.close()
        await self.bot.edit_message(msg, "Spam is cleared your mightyness")
    
    
    
    # populates a word and image cache for the server's wordcloud
    # calls are limited to __init__, nos, and henry
    def populateCaches(self):
        try:
            cur = self.bot.conn_wc.cursor()
            cur.execute("SELECT msgs FROM "+self.tablename) # hashtag no limits
            entries = cur.fetchall()
            arr = []
            for i in range(0, len(entries)):
                arr.append(entries[i][0])
            if len(arr) < 1:
                self.serverCache = self.backupArr
            else:
                self.serverCache = arr
        except Exception as e:
            print("server cache retrieval error: \n", e)
            self.serverCache = self.backupArr
        text = " ".join(self.serverCache)
        print("generating word cloud")
        wc = WordCloud(width=1024, height=1024, max_words=200000, stopwords=self.STOPWORDS).generate(text) # take it to the limit
        wc.to_file(self.serverImage)
    
    @commands.command(pass_context=True)
    async def top10(self, ctx):
        test = " ".join(self.serverCache)
        small = []
        # yes I know that servercache is already an array,
        # yes I know that it is strange that I am joining into a string
        # and then splitting it again.
        # I just don't know why it breaks if I don't do this :/
        # Henry I know you will see this and ask questions...
        # Please let it be. Same with mytop10
        for i in test.split():
            if(len(i) < 50):
                small.append(i)
        
        r = list(filter(lambda x: x not in self.STOPWORDS, small))
        r = Counter(r).most_common()
        msg = ""
        for rank in r[:10]:
            msg += str(rank[1])            
            msg += "\t\t"
            msg += rank[0]
            msg += "\n"
        await self.bot.embed_this_for_me(msg, ctx)
    
    @commands.command(pass_context=True)
    async def mytop10(self, ctx):
        words = self.wordsFromDB(ctx.message.author)
        test= " ".join(words)
        small = []
        for i in test.split():
            if(len(i) < 50):
                small.append(i)
        r = list(filter(lambda x: x not in self.STOPWORDS, small))
        r = Counter(r).most_common()
        msg = ""
        for rank in r[:10]:
            msg += str(rank[1])            
            msg += "\t\t"
            msg += rank[0]
            msg += "\n"
        await self.bot.embed_this_for_me(msg, ctx)    
    
       
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
            print("Something broke. Printing error message: ", e)
            return self.backupArr
        
    def createImage(self, arr, saveName):
        text = " ".join(arr)
        savedir = path.join(self.d,self.e, saveName) # local image gets overwritten each time. will this break if too many requests?
        wc = WordCloud(max_words=20000, stopwords=self.STOPWORDS).generate(text)
        wc.to_file(savedir)
        return savedir
        
        
        # idk how it subscribes to the event... but it works!
    async def on_message(self, message):   
        cur = self.bot.conn_wc.cursor()
        query = "INSERT INTO "+self.tablename+" VALUES (%s,%s,%s)"
        data = (message.author.id, message.content, message.timestamp)
        try:
            cur.execute(query, data)
            self.bot.conn_wc.commit()
        except psycopg2.IntegrityError as e:
            print("on_message integrity error: ", e)
        cur.close()

    @commands.command(pass_context=True)
    async def avatart(self, ctx, *args):
        """Make a wordcloud in the shape of your avatar.
        usage: !avatart <invert> <bgcolor>
        
        """
        fmt = "Making artwork {}, hold your horses!"
        msg = await self.bot.say(fmt.format(ctx.message.author.mention))
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
            await self.bot.send_file(ctx.message.channel, fin_img, content=ctx.message.author.mention)
            await self.bot.delete_message(msg)
        except:
            await self.bot.say("```Something has gone horribly wrong.```")
        


    # only refresh cache if an authorized ID
    @commands.command(pass_context=True)
    async def refreshCache(self, ctx):
        """Refresh the server wordart cache. Admin only."""
        start = time.time()
        if ctx.message.author.id == "173177975045488640" or ctx.message.author.id == "173702138122338305": #users authorized to refresh
            msg = await self.bot.say("```Working...```")
            self.populateCaches()
            fmt = "Refreshing cache took {0} seconds {1}."
            await self.bot.delete_message(msg)
            await self.bot.say(fmt.format(str(float(round((time.time()-start), 3)))
, ctx.message.author.mention)) # what in god's name
        else:
            await self.bot.say("```Bad boy! Down!```")


    @commands.command(pass_context=True)
    async def servart(self,ctx):
        """Make a wordcloud out of the server's most common words."""
        await self.bot.send_file(ctx.message.channel, self.serverImage, content=ctx.message.author.mention)

    @commands.command(pass_context=True)
    async def wordart(self,ctx):
        """Make a wordcloud out of your most common words."""
        words = self.wordsFromDB(ctx.message.author)
        filename = self.createImage(words, "wow.png")
        await self.bot.send_file(ctx.message.channel,filename,content=ctx.message.author.mention)
        
def setup(bot):
    bot.add_cog(WordArt(bot))
