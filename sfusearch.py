import discord
from discord.ext import commands
import requests
import re
from bs4 import BeautifulSoup
from urllib import parse
import datetime
# http://www.sfu.ca/students/calendar/2017/spring/courses/cmpt/120.html


class SfuSearch:

    def __init__(self, bot):
        self.bot = bot
        self.seasons = ["fall", "spring", "summer"]
   
    def gettime():
        now = datetime.datetime.now()
   
   
    # take raw json response and return appropriate message for bot to say    
    def parseResponse(self, query):
        ret = requests.get(query)
        parr = []
        if ret.status_code == 200:
            res = None
            html = ret.text
            soup = BeautifulSoup(html, "html.parser")
            
            msg =  ""

            for title in soup.find_all('h1'):            
                #parr.append(re.sub('\s'," ",title.text))
                msg = re.sub('\s'," ",title.text) + "\n"            

            for paragraph in soup.find_all('p'):
                parr.append(paragraph.text)   
          
            if len(parr) < 1:
	                return "Unable to retrieve data from SFU page"
            elif len(parr) < 2:
                return "Unable to find page"
            else:
                return msg + parr[1]
                #return parr[1]    
            
        else:
            return "SFU Server Error "+str(ret.status_code)
    
    
    def semester(self, month:str):
        """map months to semesters"""
        semesters = {
            "january":"spring",       
            "february":"spring",
            "march":"spring",
            "april":"spring",
            "may":"summer",
            "june":"summer",
            "july":"summer",
            "august":"summer",
            "september":"fall",
            "october":"fall",
            "november":"fall",
            "december":"fall",
            '1':"spring",       
            '2':"spring",
            '3':"spring",
            '4':"spring",
            '5':"summer",
            '6':"summer",
            '7':"summer",
            '8':"summer",
            '9':"fall",
            '10':"fall",
            '11':"fall",
            '12':"fall"
            }
        if month in semesters:
            return semesters[month]
        else:
            print(str(month) +" is not in the dict")
            return "fall"
    
    # coursepart must contain both course and subject
    def parsecoursepart(self, coursepart:str):
        subject = None
        course = None
        for i, c in enumerate(coursepart):
            if c.isdigit():
                subject = coursepart[:i]
                course = coursepart[i:]
                break;
          #fix undefined error
        return (subject, course)
    
    
    def createurl(self, word):
        semester = None
        subject = None
        if len(word) == 1:
            coursepart = word[0]
            if len(coursepart) < 4:
                # assume cmpt course search
                course = coursepart
            else:
                # assume course and subject search
                subject, course = self.parsecoursepart(coursepart)
                        
            
        elif len(word) == 2:
            
            if word[0] in self.seasons: # two parts are season and coursepart
                semester = word[0]
                subject, course = self.parsecoursepart(word[1])
            elif word[1] in self.seasons:
                semester = word[1]
                subject, course = self.parsecoursepart(word[0])
            else:
                # two parts are course and subject
                if any(char.isdigit() for char in word[0]): #subjects have no digits
                    subject = word[1]
                    course = word[0]
                    
                elif any(char.isdigit() for char in word[1]):
                    subject = word[0]
                    course = word[1]
                else:
                    # some sort of error occured
                    print("An error occured")
        
        else:
            print("bad number of args")
        query = "http://www.sfu.ca/students/calendar/"
        now = datetime.datetime.now()
        year = str(now.year)
        if semester == None:
            semester = self.semester(str(now.month))
        if subject == None:
            subject = "cmpt"
        #coursenumber = word
        
        query += year +"/"+ semester + "/courses/" + subject + "/" + course
        return query
        
    
    
    @commands.command(pass_context=True)
    async def sfu(self,ctx, *words:str):
        """Lookup an SFU class
        usage: !sfu <cmpt120> or !sfu <cmpt> <120>
        
        """
        url = self.createurl(words)
        msg = self.parseResponse(url)
        mg = msg + "\n"+url
        await self.bot.embed_this_for_me(mg,ctx)
        #await self.bot.say(mg)
#        await self.bot.say(url)
    
    
   
def setup(bot):
    bot.add_cog(SfuSearch(bot))
