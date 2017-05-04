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
#opencv-python is a dependency

#force scaling images? (so a 4k image doesn't break server)
#add background option
#add invert option

class WordArt:
    tablename = "wordartMessages"
    backupArr = ['sad','oh no', 'terrible timing', 'broken', 'sad','sad', 'nuuu',':(', 'broken', 'sad','brokenhearted', 'next time?']
    
    
    testimg = "testimg.png"
    d = path.dirname(__file__)
    e = "wordart_dir"
    
       
    def __init__(self, bot):
        self.bot = bot
        cur = self.bot.conn_wc.cursor()
        query = "CREATE TABLE IF NOT EXISTS "+self.tablename+"(user_id bigint, msgs varchar(2000), date text, UNIQUE(user_id, date))" # create table if doesn't exist
        cur.execute(query)
        self.bot.conn_wc.commit()
        cur.close()
       
       
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
        
    def createImage(self, arr):
        text = " ".join(arr)
        savedir = path.join(self.d,self.e, "wow.png") # local image gets overwritten each time. will this break if too many requests?
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

    # uses a user's avatar as a filter for wordart
  #  @commands.command(pass_context=True)
  #  async def avatart(self, ctx):
  #      slothy = path.join(self.d,self.e,"slothy.webp")
  #      avatar_bw = path.join(self.d,self.e,"avatar_bw.png")
  #      fin_img = path.join(self.d,self.e,"fin.png")
  #      
  #      ava = ctx.message.author.avatar_url # grab avatar URL
  #      img_data = requests.get(ava).content
  #      with open(slothy, "wb") as handler:
  #          handler.write(img_data) #save avatar picture to file
  #      img = cv2.imread(slothy,1)
  #      img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  #      ret,img_bw = cv2.threshold(img_gray,127,255, cv2.THRESH_BINARY)
  #      #cv2.imwrite(avatar_bw,img_bw) # write b&w avatar to file
  #      
  #      word = self.wordsFromDB(ctx.message.author) # retrieve words from DB
  #      text = " ".join(word)
  #      avatar_mask = np.array(img_bw) # create mask
  #      wc = WordCloud(background_color="white", max_words=2000, mask=avatar_mask)
  #      wc.generate(text)
  #      wc.to_file(fin_img) # save masked wordart to file
  #      await self.bot.send_file(ctx.message.channel, fin_img)

    @commands.command(pass_context=True)
    async def avatart(self, ctx, *args):
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
        img_data = requests.get(ava, stream=True).content #dl from dat url
        
        img = cv2.imdecode(np.frombuffer(img_data, np.uint8),1) # convert from string butter to uint8
        img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # grayscale that motha
        ret,img_bw = cv2.threshold(img_gray,127,255, thresh) #threshold values
        # it's different
        word = self.wordsFromDB(ctx.message.author) # retrieve words from DB
        text = " ".join(word)

        avatar_mask = np.array(Image.open(avatar_bw)) # create mask
        wc = WordCloud(background_color="black", max_words=2000, mask=avatar_mask)
        wc.generate(text)
        wc.to_file(fin_img) # save masked wordart to file
        
       
        await self.bot.send_file(ctx.message.channel, fin_img)


    @commands.command(pass_context=True)
    async def wordart(self,ctx):
        words = self.wordsFromDB(ctx.message.author)
        filename = self.createImage(words)
        await self.bot.send_file(ctx.message.channel, filename)
        
def setup(bot):
    bot.add_cog(WordArt(bot))
