# py -m pip install -U __
# pylint: disable=C
import discord
import os
from discord.ext import commands
import configparser
import getpass
import psycopg2
import urllib.parse
import random
import asyncio
import codecs as codex
import math
import time
import subprocess
import sys
from io import StringIO
import logging

configFile = "botMain.settings"

#check if config file exists, if not, input manually
if not os.path.isfile(configFile):
  DISCORD_API_ID = getpass.getpass('Discord API: ')
  token = getpass.getpass('Token: ')
  wolframid = getpass.getpass('Wolframalpha: ')
  ip = "172.93.48.238:25565"
  description = "Bot of the CSSS"
  postgrespass = getpass.getpass('Database Password: ')
  mashape_key = getpass.getpass('Mashape Key: ')
  local_postgres_pw = getpass.getpass('Database Password: ')
  imgur_id = getpass.getpass('Imgur client id: ')
else:
  #Load the config file
  config = configparser.ConfigParser()
  config.read(configFile)
  description = config.get("Discord", "Description")
  wolframid = config.get("Wolfram", "TokenId")
  DISCORD_API_ID = config.get("Discord", "API_ID")
  token = config.get("Discord", "Token")
  ip = "172.93.48.238:25565"
  postgrespass = config.get("Postgres", "Password")
  mashape_key = config.get("Mashape", "Token")
  local_postgres_pw = config.get("LocalPG", 'Password')
  imgur_id = config.get("Imgur", "client_id")

# SQL SETUP------------------------------------------------------------------------------
urllib.parse.uses_netloc.append("postgres")
conn = psycopg2.connect("port='5432' user='zocnciwk' host='tantor.db.elephantsql.com' password='"+postgrespass+"'")
cur = conn.cursor()
# SQL SETUP------------------------------------------------------------------------------

bot = commands.Bot(command_prefix='.', description=description)
bot.wolframid = wolframid
bot.mcip = ip
bot.remove_command("help")
bot.mashape_key = mashape_key
bot.imgur_id = imgur_id
bot.lang_url = config.get("Translate","url")

# creating a 2D empty array for exp queues
expQueue = []
global expTable
expTable = []

@bot.event
async def on_ready():
  print('Logged in as')
  print(bot.user.name)
  print('------')
  await bot.change_presence(game=discord.Game(name='Yes my master'))
  global expTable

@bot.event
async def on_message(message):
  # DATABASE OPERATIONS. DISABLE UNLESS ACTUALLY RUNNING AS SERVICE
  # print(message.author.name+"#"+message.author.discriminator)
  if validate(message):
    await add(message)
  await bot.process_commands(message)

@bot.command()
async def test():
  await bot.say('testing')

# Check if author is currently on cooldown
async def validate(message):
  for item in expQueue:
    if message.author.id == item[0]:
      # author on cooldown
      return False
  # author not on cooldown, add author id and current time to queue
  expQueue.append([message.author.id, time.time()])
  return True

# handles adding new users and updating existing user exp to database
async def add(message):
  database = 'experience'

  entry = db_select(database, message.author.id)

def db_select(database, query):
  cur.execute("SELECT * FROM (%s) WHERE user_id = (%s)", (str(database), str(query),))
  return cur.fetchone()


bot.run(token)
