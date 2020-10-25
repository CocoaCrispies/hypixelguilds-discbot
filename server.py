# bot.py
from gevent import monkey as curious_george
curious_george.patch_all(thread=False, select=False)
from discord.utils import get
import discord.ext
import hypixel
import requests
import os
import datetime
import sys
import traceback
from discord import Activity, ActivityType
from discord.ext import commands
from discord.ext.commands import UserConverter
import json
from bs4 import BeautifulSoup
import aiohttp
import math
from os import listdir
from os.path import isfile, join
from utils.functions import *
from utils.errors import *
key_file = open_json('config.json')
api_key = key_file['api-key-hypixel']

hypixel.setKeys({api_key})
cogs_dir = "cogs"
startup_extensions = ["admin"]
TOKEN = key_file['api-key-discord']
bot = commands.Bot(command_prefix="/", help_command=None, case_insensitive=True)
@bot.event

@bot.event
async def on_ready():
    print("Bot is ready!")
    
    
if __name__ == "__main__":
    for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
        try:
            bot.load_extension(cogs_dir + "." + extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.')
            traceback.print_exc()
    bot.run(TOKEN)
                  
                  
    