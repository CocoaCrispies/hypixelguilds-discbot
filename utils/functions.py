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
import nbt
import base64
import io
import gzip
import zlib

def open_json(f_name):
    with open(f_name) as json_file:
        data = json.load(json_file)
        return data

  

def table2json(table, keys: list):
    soup = BeautifulSoup(table, "html.parser")
    leaderboard = []
    for row in soup.find_all('tr'):
        values = [td.get_text(strip=True) for td in row.find_all('td')]
        row = dict(zip(keys, values))
        leaderboard.append(row)
    return leaderboard
def sk1er_api(uname):
    r = requests.get(f"https://api.sk1er.club/guild/player/{uname}").json()
    return r
def fetch_uuid_uname(uname_or_uuid):
    r = requests.get(f'https://mc-heads.net/minecraft/profile/{uname_or_uuid}').json()
    return r['name'], r['id']
  
def get_Guild_Info(guild_id):
    data = requests.get(f'https://api.hypixel.net/guild?id={guild_id}&key=79a681b0-45fe-473a-a8a5-444e2f67edf3').json()
    return data

def decode_inventory_data(raw):
   data = nbt.nbt.NBTFile(fileobj = io.BytesIO(base64.b64decode(raw)))
   return data.pretty_tree()

def print_item(nbt):
    piece = nbt['i'].tags[0]['tag']['display']['Name']
    piece_fix = []
    p = ""
    for i, v in enumerate(piece): 
        piece_fix.append(v)
    p = p.join(piece_fix)
    return p

def codeify(text):
    formatted = f"```{text}```"
    return formatted
def inventory_data(username, profile):
    key_file = open_json('config.json')
    api_key = key_file['api-key-hypixel']
    uuid = fetch_uuid_uname(username)[1]
    profile_id_link = requests.get(f"https://api.hypixel.net/player?key={api_key}&uuid={uuid}").json()
    profile_id = list(profile_id_link['player']['stats']['SkyBlock']['profiles'].keys())[profile-1]
    data = requests.get(f"https://api.hypixel.net/skyblock/profile?key={api_key}&profile={profile_id}").json()
    print(data)
    inv_raw = data['profile']['members'][uuid]['inv_armor']['data']
    print(inv_raw)
    return decode_inventory_data(inv_raw)

def skyblockProfile(playerName):
    r = requests.get(f"http://sky.shiiyu.moe/api/v2/profile/{playerName}").json()
    return r

def authorCheck(author):
    def innerCheck(message):
        if message.author != author:
            return False
        try: 
            int(message.content) 
            return True 
        except ValueError: 
            return False
    return innerCheck