# py -m pip install -U __
# pylint: disable=C
import discord
import os
# import sympy
from discord.ext import commands
# from sympy import *
import wolframalpha
from mcstatus import MinecraftServer
import datetime
import configparser
import getpass
import psycopg2
import urllib.parse
import random
import time
import asyncio
import codecs as codex
import math

configFile = "botMain.settings"

#check if config file exists, if not, input manually
if not os.path.isfile(configFile):
    DISCORD_API_ID = getpass.getpass('Discord API: ')
    token = getpass.getpass('Token: ')
    wolframid = getpass.getpass('Wolframalpha: ')
    ip = "172.93.48.238:25565"
    description = "Bot of the CSSS"
    postgrespass = getpass.getpass('Database Password: ')
else:
    #Load the config file
    config = configparser.ConfigParser()
    config.read(configFile)
    description = config.get("Discord", "Description")
    wolframid = config.get("WolfGram", "TokenId")
    DISCORD_API_ID = config.get("Discord", "API_ID")
    token = config.get("Discord", "Token")
    ip = "172.93.48.238:25565"
    postgrespass = config.get("Postgres", "Password")

# SQL SETUP------------------------------------------------------------------------------
urllib.parse.uses_netloc.append("postgres")
conn = psycopg2.connect("port='5432' user='zocnciwk' host='tantor.db.elephantsql.com' password='"+postgrespass+"'")
cur = conn.cursor()

global expTable
expTable = []

# used to pull template levels and exp goals from db
def getLevel():
    cur.execute("SELECT level, exp FROM template ORDER BY level")
    i = 0
    table = []
    stop = False
    while stop == False:
        temp = cur.fetchone()
        if temp == None:
            stop = True
        else:
            table.append(temp)
            i = i+1
    return table

# used to find the current level of user given experience
def userLevel(experience):
    global expTable
    for foo in expTable:
        if experience >= foo[1]:
            level = foo[0]
    return level

# detect if user is eligible for the next level
async def updateLevel(change, experience):
    currLevel = userLevel(experience)[0]
    afterChange = userLevel(experience+change)[0]
    if afterChange != currLevel:
        return True
    return False    

# formula used to calculate exact experience needed for next level
def calcLevel(x):
    return 5*math.pow(x, 2) + 40*x + 55