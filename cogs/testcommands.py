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
from utils.functions import *
from utils.errors import *

client = discord.Client()

key_file = open_json('config.json')
api_key = key_file['api-key-hypixel']

class testcommands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.command()
  async def hello(self, ctx):
    await ctx.send("hello world!")
  
  @commands.command()
  async def inventory(self, ctx, name: str):
    shuJson = skyblockProfile(name)
    msg = await client.wait_for(event='message', check = lambda message: message.author == ctx.author, timeout=15)
    print("test")
    selection = int(msg.content)-1
    armor = shuJson['profiles'][selection]['items']['armor']
    armorEmbed = discord.Embed(name="Armor")
    boots = armor[0]["display_name"]
    armorEmbed.add_field(name="Helmet", value=boots)
    await ctx.send(embed=armorEmbed)
def setup(bot):
    bot.add_cog(testcommands(bot))