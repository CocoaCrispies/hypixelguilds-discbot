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

class Admin(commands.Cog):
  def __init__(self,bot):
    self.bot = bot
    
  @commands.command()
  async def load(extension_name : str):
    """Loads an extension."""
    self.bot = bot
    try:
        self.bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await self.bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("{} loaded.".format(extension_name))

  @commands.command()
  async def unload(extension_name : str):
    self.bot = bot
    """Unloads an extension."""
    self.bot.unload_extension(extension_name)
    await self.bot.say("{} unloaded.".format(extension_name))    
def setup(bot):
    bot.add_cog(Admin(bot))