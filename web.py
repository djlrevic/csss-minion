import discord
import requests
import json
import urllib
from discord.ext import commands
from bs4 import BeautifulSoup
from urllib import parse



class Web:

    def __init__(self, bot):
        self.bot = bot
        self.headers = {"X-Mashape-Key": self.bot.mashape_key, "Accept": "text/plain"} #urbandict mashape key
        self.emojis = None # cache


    def imgur_api(self, search):
        querystring={'q':search}
        img = None
        desc = None
        headers = {'authorization':'Client-ID '+self.bot.imgur_id}
        url = 'https://api.imgur.com/3/gallery/search/{{sort}}/{{window}}/{{page}}' # I don't know how this works, but it does.
        res = requests.request('GET', url, headers=headers, params=querystring)
        if res.status_code == 200:
            ret = res.json()
            
            if len(ret['data']) == 0: #shit's bad
                return None
            
            if 'animated' in ret['data'][0]: # animated URL, yoink!
                if 'link' in ret['data'][0]:
                    img = ret['data'][0]['link']
                    desc = ret['data'][0]['title']
            
            else: #not animated, construct our own URL
                img = "http://i.imgur.com/6rqtdQ2.jpg"
                if 'cover' in ret['data'][0]:
                    img = "http://i.imgur.com/"+ret['data'][0]['cover']+".jpg"
                    desc = ret['data'][0]['title']
        return (desc,img)


    @commands.command(pass_context=True)
    async def imgur(self,ctx, *word:str):
        """Search for a picture on imgur"""
        msg = self.imgur_api(" ".join(word))
        if msg == None:
            await self.bot.embed_this_for_me("Nothing found in imgur's vast database.\nPerhaps you really are a special snowflake?",ctx)
        else:
            em = discord.Embed(title=msg[0] ,colour=0xfff)
            em.set_image(url=msg[1])
            await ctx.send(embed=em)



    def parseLinksResponse(self, word): # webscraping duckduckgo results
        removestr = ["search.yahoo.com", "advertising-and-affiliates"]
        keystr = ["https://", "http://"]
        query = "https://duckduckgo.com/html/?q="+word
        ret = requests.get(query)
        if ret.status_code == 200:
            results = []
            results.append("Results provided by DuckDuckGo... Don't get any viruses now...")
            html = ret.text
            soup = BeautifulSoup(html, "html.parser")
            for link in soup.find_all('a'):
                hyperlink = link.get('href')
                if hyperlink is not None:
                    decoded = parse.unquote(hyperlink) #URL decoding, important.
                    if removestr[0] in decoded or removestr[1] in decoded:
                        continue; # don't add these
                    if keystr[0] in decoded: #https link
                        cutoff = decoded[decoded.find('https://'):] # find only the URL part
                        if cutoff not in results: # don't put 4 duplicates in arr
                            results.append(cutoff)
                    elif keystr[1] in decoded: #http link
                        cutoff = decoded[decoded.find('http://'):] # find only the URL part
                        if cutoff not in results: # don't put 4 duplicates in arr
                            results.append(cutoff)    
            res = results[0]
            for r in results[1:6]: # return 6 results
                res += "\n<"+r+">"  # escape discord embedding       
            if len(results) == 1:
                return "DuckDuckGo could not find any results"
            else:
                return res
        else:
            return "DuckDuckGo Server Error"


    @commands.command(pass_context=True)
    async def links(self,ctx, *query):
        """Search for links using DuckDuckGo!"""
        word = " ".join(query)
        msg = self.parseLinksResponse(word)
        await self.bot.embed_this_for_me(msg,ctx)

    def parseSearchResponse(self, word):
        """ neat"""
        bang = False
        if word[0] == '!': # duckduckgo has built-in bang redirects. we will just display the link.
            url = 'http://api.duckduckgo.com/?q={}&format=json&pretty=1&no_redirect=1'.format(urllib.parse.quote_plus(word))
            bang = True
        else:
            url = 'https://api.duckduckgo.com/?q={}&format=json'.format(urllib.parse.quote_plus(word))
        
        ret = requests.get(url)
        json = ret.json()
        msg = ""
        em = discord.Embed(colour=0xfff)
        if ret.status_code == 200:
            if bang:
                return em.add_field(name='Bang redirect', value=json['Redirect'])
                
            for i in range(0, 3):
                try:
                    title = BeautifulSoup(json['RelatedTopics'][i]['Result'], 'html.parser').a.text
                    text = json['RelatedTopics'][i]['Text']
                    link = json['RelatedTopics'][i]['FirstURL']            
                    em.add_field(name=title, value=text + '\n' + link)
                except KeyError as e: #.... I hate this json
                    print("key error in search command", e)
                except IndexError as e:
                    print("index error in search command", e)
            if len(em.fields) < 1:
                em.add_field(name='Nothing found', value='Are you unique? Or just spammy?')
            return em
        else:
            em.add_field(name="There was an error!?", value=str(ret.status_code))
            return em


    @commands.command()
    async def search(self, ctx, *query):
        """Search for instant answers using DuckDuckGo!"""
        word = " ".join(query)
        msg = self.parseSearchResponse(word)
        await ctx.send(embed=msg)
        #await self.bot.embed_this_for_me(msg, ctx)

    
    def parseWikiResponse(self, json):
        msg = json.json()
        if json.status_code == 200 and not len(msg[1]) == 0:
            if isinstance(msg[1][0], str) and ("(disambiguation)" in msg[1][0] or "may refer to:" in msg[2][0]): #wiki has no standard, so we need to check for all of these cases         
                definition_str = "Search for *"+msg[0]+"* is too general. Try one of these: \n"
                for i in range(0,len(msg[1])):
                    if "may refer to:" not in msg[2][i]:
                        definition_str += "\n"+msg[1][i]
            else: # found it!
                definition_str = "Wiki summary for "+ msg[0] + "\n\n" +msg[2][0] + "\n" + msg[3][0]
        else:
            definition_str = "There was an error "+str(json.status_code)+". There is no page for this."
        return definition_str
    
       
    @commands.command(pass_context=True)
    async def wiki(self, ctx, *msg):
        """Look up a subject on wikipedia."""   
        query = " ".join(msg)
        json = requests.get('https://en.wikipedia.org/w/api.php?action=opensearch&search='+query+'&limit=5&format=json&redirects=resolve')
        definition_str = self.parseWikiResponse(json)
        await self.bot.embed_this_for_me(definition_str, ctx)
        
       
    # take raw json response and return appropriate message for bot to say    
    def parseUrbanResponse(self, json):
        if json.status_code == 200:
            r = json.json()
            if r['result_type'] == "exact":
                msg = " " #python strings are funny sometimes
                msg += r['list'][0]['word']
                msg +="```"+ r['list'][0]['definition'] +"```"
                msg += "**example: **"+r['list'][0]['example']
                msg += "\n<"+r['list'][0]['permalink']+">"
                return msg
                
            elif r['result_type'] == "no_results":
                return "You probably typed in some dumb shit, cuz I can't find it." 
                
            else:
                return "Contact Nos ASAP cuz shit's broke"
                  
        else:
            return "Bad response from server  *shrugs*"       
       
       
    @commands.command(pass_context=True)
    async def urban(self,ctx, *msg:str):
        """Lookup some jargon from the urban dictionary."""
        word = " ".join(msg)
        query = "https://mashape-community-urban-dictionary.p.mashape.com/define?term="+word
        req = requests.get(query, headers=self.headers)
        ret = self.parseUrbanResponse(req)
        await ctx.send(ret) #embedding increases risk of breaking char count by a lot
       
       
    def requestVid(self, query:str):
        """Request a video using the special nos API."""
        keystr = "/watch?v=" # video id
        noResults = firstRes = 'nothing' # wizardry
        query = "https://www.youtube.com/results?search_query="+query
        ret = requests.get(query)
        if ret.status_code == 200:
            html = ret.text
            soup = BeautifulSoup(html, "html.parser")
            for link in soup.find_all('a'):
                hyperlink = link.get('href')
                if keystr in hyperlink:
                    firstRes = hyperlink
                    break;
            fullURL = "https://www.youtube.com"+firstRes
            if noResults == firstRes:
                return "No search results found"
            else:
                return fullURL
        else:
            return "Youtube Server Error"       
       
       
    @commands.command(pass_context=True)
    async def youtube(self, ctx, *msg):
        """Search for a youtube video."""
        query = " ".join(msg)
        link = self.requestVid(query)
        await ctx.send(link)
       
       
    @commands.command(pass_context=True)
    async def eggwrite(self, ctx, *msg):
        """Use the bot to write with eggplant emojis!"""
        if self.emojis == None:
            self.emojis = ctx.message.guild.emojis
        word = " ".join(msg)
        newstr = ctx.message.author.name + " says: "
        origin = ctx.message
        for s in word:
            if s.isalpha():
                #convert to eggplant letter
                for em in self.emojis:
                    if str(em)[3] == "_" and str(em)[2] == s.upper():
                        newstr += str(em)
                        break;
            elif s == " ":
                #change to 5 spaces
                newstr += "     "
            else:
                newstr += s
        try:
            await ctx.send(newstr)
            await origin.delete()
        except:
            await ctx.send("Your message was likely too long.")
        #await self.bot.embed_this_for_me(newstr,ctx) #do not do this :/       
       
       
def setup(bot):
    bot.add_cog(Web(bot))
