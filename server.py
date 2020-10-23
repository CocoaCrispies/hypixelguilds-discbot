import discord.ext
import hypixel
import requests
import os
import datetime
import sys
import traceback
from discord import Activity, ActivityType
from discord.ext import commands
import json
from bs4 import BeautifulSoup
import aiohttp
import math
from tinydb import TinyDB, Query
import json
db = TinyDB('db.json')
configKeys = json.load(open('config.json'))
def table2json(table, keys: list):
    soup = BeautifulSoup(table, "html.parser")
    leaderboard = []
    for row in soup.find_all('tr'):
        values = [td.get_text(strip=True) for td in row.find_all('td')]
        row = dict(zip(keys, values))
        leaderboard.append(row)
    return leaderboard

apiKey = configKeys["hy-key"]

hypixel.setKeys({configKeys["hy-key"]})
def sk1er_api(uname):
    r= requests.get(f"https://api.sk1er.club/guild/player/{uname}").json()
    return r
def fetch_uuid_uname(uname_or_uuid):
    r = requests.get(f'https://mc-heads.net/minecraft/profile/{uname_or_uuid}').json()
    return r['name'], r['id']
def get_Guild_Info(guild_id):
    data = requests.get(f'https://api.hypixel.net/guild?id={guild_id}&key=79a681b0-45fe-473a-a8a5-444e2f67edf3').json()
    return data
TOKEN = configKeys["disc-keys"]
commandList = ["**help**"+"\n"+"_Commands and their arguments!_","\n","btw, if u wanna support me, heres a kofi, bc server spacec is expensive: ko-fi.com/cocoa","**support**"+"\n"+"_Sends link to help server_","**gexp**"+"\n"+"_Checks the guild exp of every member and checks if they are below the amout you input! Arg1 is your IGN, arg2 is the amount of gexp to check for!_", "**gpstats**"+"\n"+"_Shows stats of the guild that the player is a part of. Arg is IGN_", "**invite**"+"\n"+"_Gives the bot invite link!_", "**servers**"+"\n"+"_Counts how many discord servers the bot is connected to!_"]

bot = commands.Bot(command_prefix="+", help_command=None, case_insensitive=True)
@bot.event
async def on_command_error(ctx, error):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """
        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound, )
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':
                await ctx.send('I could not find that member. Please try again.')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please input your username or other argument and try again!")
        elif isinstance(error, commands.MissingRole):
            await ctx.send("You do not have permissions to do this!")
        elif isinstance(error, hypixel.PlayerNotFoundException):
            await ctx.send("User does not exist!")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permissions to do this! | Permission required: Administrator")
        #elif isinstance(error, discord.HTTPException):
            #await ctx.send("This is a known error being worked on, sorry for the inconvenience")
        elif isinstance(error, UnboundLocalError):
          await ctx.send("Something went wrong here :/")
        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


@bot.event
async def on_ready():
    await bot.change_presence(activity=Activity(name=f"{len(bot.guilds)} servers", type=ActivityType.watching))
    print("Bot is ready!")
@bot.command(name='servers', help='Shows the amount of sevrers bot is conencted to')
async def servers(ctx):
  await ctx.send(f"```{len(bot.guilds)} servers```")
  await bot.change_presence(activity=Activity(name=f"{len(bot.guilds)} servers", type=ActivityType.watching))
@bot.command(name='help', help='Gives you help lmfao')
async def help(ctx):
  embed = discord.Embed(title="**Help and Commands**", color = 6959775)
  embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/728291929833341031/733772466325028916/Discord_Bot0000.jpg")
  embed.description = "Commands and their arguments!"
  embed.add_field(name = "**Commands:**", value ='\n'.join(commandList))
  #embed.add_field(name = "Arguments", value = '\n'.join(argList))
  embed.set_footer(text="Code by: Cocoa#3581, and the help from people on StackOverflow and the Hypixel Fourms! Support me on ko-fi.com/cocoa")
  await ctx.send(embed=embed)
@bot.command(name='support', help='Sends link to help server')
async def suport(ctx):
    await ctx.send("Help Server: https://discord.gg/jXMQVrY")
    await bot.change_presence(activity=Activity(name=f"{len(bot.guilds)} servers", type=ActivityType.watching))
@bot.command(name='invite', help='Sends link to help server')
async def invite(ctx):
    await ctx.send("Invite the Hypixel Guild Bot using this link!" + "\n" + "https://discord.com/api/oauth2/authorize?client_id=732003254010904648&permissions=124992&scope=bot")
    await bot.change_presence(activity=Activity(name=f"{len(bot.guilds)} servers", type=ActivityType.watching))

@bot.command(name='gstats', help='Shows stats of the guild that the player is a part of. Arg is IGN')
async def gstats(ctx, arg):
  async with ctx.typing():
    Name = arg
    #this is werid
    #uname, uuid = fetch_uuid_uname(Name)
    Player = hypixel.Player(Name)
    print(" ")
    print('Guild Id: ' + Player.getGuildID())
    print(" ")
    memberList = []
    gamesList = []
    guild = get_Guild_Info(Player.getGuildID())
    memberNumber = len(guild['guild']['members'])
    sk1erResponse = sk1er_api(Name)
    try:
      for x in range(len(guild['guild']['preferredGames'])):
          gamesList.append(guild['guild']['preferredGames'][x-1])
    except:
      gamesList = ["N/A"]
      pass
    embed = discord.Embed(title="**"+guild['guild']['name']+"**", inline = True, color = 6959775) #,color=Hex code

    try:
      embed.description = guild['guild']['description']
    except:
      pass
    async with aiohttp.ClientSession(headers={'discord.py bot': 'Cool Python Application'}) as session:  # Replace the user agent with something unique that can be used to identify the request
      async with session.get(f'https://sk1er.club/leaderboards/newdata/GUILD_LEVEL') as resp:
        content = await resp.read()
      await session.close()
      lbjson = table2json(content, ['Position Change','-', 'Name', 'Level', 'Wins since guild update', 'Exp', 'Legacy Rank', 'Date Created'])
      Player = hypixel.Player(arg)
      guild = get_Guild_Info(Player.getGuildID())
      for x in range(len(lbjson)-1) :
        try:
          if lbjson[x]['Name'] == guild['guild']['name'] :
            lbspot = lbjson[x]['Position Change']
            guildNumber = x
          else:
            continue
        except:
          continue

    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/728291929833341031/733772466325028916/Discord_Bot0000.jpg')
    embed.add_field(name="** :crown: Guild Master:**", value=  fetch_uuid_uname(guild['guild']['members'][0]['uuid'])[0])
    embed.add_field(name="**:slot_machine: Number Of Members: **", value= memberNumber)

    try:
      embed.add_field(name="** :mega: Guild Tag: **", value= "**[" + guild['guild']['tag'] + "]**")
    except:
      embed.add_field(name="** :mega: Guild Tag: **", value= "No Tag Found!")
      pass
    try:
      embed.add_field(name="**:video_game: Preferred Games:**", value= '\n'.join(gamesList))
    except:
      pass
    embed.add_field(name = "** :golf: Guild Leaderboard Positon:**", value = lbspot)

    embed.add_field(name="**:calendar: Date Created:**", value= datetime.datetime.fromtimestamp(float(guild['guild']['created'])/1000).strftime('%Y-%m-%d'))
    embed.add_field(name= "**:game_die: Guild Level:**", value = str(math.floor(sk1erResponse['guild']['level_calc'])))

    embed.add_field(name="**:thermometer: Total Guild EXP:**", value = '{:,}'.format(guild['guild']['exp']))
    embed.set_footer(text="Code by: Cocoa#3581, and the help from people on StackOverflow and the Hypixel Fourms! ko-fi.com/cocoa")
    print(embed.to_dict())
    await ctx.send(embed=embed)
    await bot.change_presence(activity=Activity(name=f"{len(bot.guilds)} servers", type=ActivityType.watching))
    #-----------------------------------------------------------------------------------------------------------------------------------
@bot.command(name='gexp', help='Checks the guild exp of every member and checks if they are below the amout you input! Arg1 is your IGN, arg2 is the amount of gexp to check for!')
async def gexp(ctx, arg, arg2):
  async with ctx.typing():
    embed = discord.Embed(title="People Under GEXP Reqs:", color = 6959775, inline = True) #,color=Hex code
    Name = arg
    #uname, uuid = fetch_uuid_uname(Name)
    Player = hypixel.Player(Name)
    memberList = {}

    guild = get_Guild_Info(Player.getGuildID())
    memberNumber = len(guild['guild']['members'])
    for x in range(memberNumber - 1):
      if sum(guild['guild']['members'][x]['expHistory'].values()) < int(arg2):
        Member = fetch_uuid_uname(guild['guild']['members'][x]['uuid'])
        if len(guild['guild']['members'][x]['expHistory'].values()) < 7:
          memberList.update({Member[0]:"API Error, please try again for this person"})
        else:
         memberList.update({Member[0]:sum(guild['guild']['members'][x]['expHistory'].values())})
      else:
        continue

    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/728291929833341031/733772466325028916/Discord_Bot0000.jpg")

    for key, value in memberList.items():
      embed.add_field(name=f"{key}:", value=f"``{value}``")
    embed.set_footer(text="Code by: Cocoa#3581, and the help from people on StackOverflow and the Hypixel Fourms! ko-fi.com/cocoa")
    await ctx.send(embed=embed)
    await bot.change_presence(activity=Activity(name=f"{len(bot.guilds)} servers", type=ActivityType.watching))
@bot.command(name = 'gpstats', decription= 'Shows the guild stats of the player specified!')
async def gpstats(ctx, arg):
  Name = arg
  #uname, uuid = fetch_uuid_uname(Name)
  Player = hypixel.Player(Name)
  memberList = []
  gamesList = []
  guild = get_Guild_Info(Player.getGuildID())
  memberNumber = len(guild['guild']['members'])
  target = ""
  targetNum = 0
  for x in range(memberNumber - 1):
    if guild['guild']['members'][x]['uuid'] == fetch_uuid_uname(Name)[1]:
      target = guild['guild']['members'][x]['uuid']
      targetNum = x
      break
    else:
      continue
  targetGuild = get_Guild_Info(hypixel.Player(target))
  embed = discord.Embed(title=fetch_uuid_uname(target)[0]+"'s Guild Stats:", color = 6959775)
  embed.set_thumbnail(url=f"https://mc-heads.net/avatar/{target}")
  embed.add_field(name="**:european_castle: Guild Name:**", value= guild['guild']['name'])
  embed.add_field(name="**:shield: Rank:**", value = guild['guild']['members'][targetNum]['rank'])
  embed.add_field(name="\n\u200b", value= "\n\u200b")
  embed.add_field(name="**:clock1: Date Joined:**", value= datetime.datetime.fromtimestamp(float(guild['guild']['members'][targetNum]['joined'])/1000).strftime('%Y-%m-%d'))
  embed.add_field(name="**:thermometer: Guild EXP Over 7 Days:**", value= '{:,}'.format(sum(guild['guild']['members'][targetNum]['expHistory'].values())))
  embed.add_field(name="\n\u200b", value= "\n\u200b")
  try:
    embed.add_field(name="**:bookmark: Quest Participation:**", value= "   "+ str(guild['guild']['members'][targetNum]['questParticipation'])+" Total")
  except:
    embed.add_field(name="**:bookmark: Quest Participation:**", value= "No Participation!")
  embed.set_footer(text="Code by: Cocoa#3581, and the help from people on StackOverflow and the Hypixel Fourms! ko-fi.com/cocoa")
  await ctx.send(embed=embed)
  await bot.change_presence(activity=Activity(name=f"{len(bot.guilds)} servers", type=ActivityType.watching))

@bot.command(name='verify')
async def verify(ctx, arg):
  Servers = Query()
  guild_search = db.search(Servers.id == ctx.guild.id)
  if (guild_search == []):
    db.insert({"id":ctx.guild.id,"verify":True})
  if (guild_search[0]['verify'] == True):
    pass
  else:
    playerProfile = sk1er_api(arg)
    roles = []
    user = ctx.message.author
    request_json = requests.get(f"https://api.hypixel.net/player?key={apiKey}&name={arg}").json()
    try:
        discord_name = request_json['player']['socialMedia']['links']["DISCORD"]
    except:
        await ctx.send("""
    **Verification Instructions**

    **1)** Go to a Hypixel lobby.
    **2)** Right click "My Profile" in the hotbar, it is slot number 2.
    **3)** Click "Social Media". It is to the right of the Redstone block ("Status") button.
    **4)** Click "Discord". It is the second last option.
    **5)** Paste your Discord username into chat and hit enter. For reference your username is: {name}
    **6)** You're done! Now wait at least 1 minute and verify again.

    **Video Example - Link Discord**
    https://youtu.be/6ZXaZ-chzWI
    """)
        pass
    name = f"{user.name}#{user.discriminator}"
    help_message = f"""
**Verification Instructions**

**1)** Go to a Hypixel lobby.
**2)** Right click "My Profile" in the hotbar, it is slot number 2.
**3)** Click "Social Media". It is to the right of the Redstone block ("Status") button.
**4)** Click "Discord". It is the second last option.
**5)** Paste your Discord username into chat and hit enter. For reference your username is: {name}
**6)** You're done! Now wait at least 1 minute and verify again.

**Video Example - Link Discord**
https://youtu.be/6ZXaZ-chzWI
"""
    for r in ctx.guild.roles:
      roles.append(r.name)

    if discord_name == name:
      try:
        await user.add_roles(discord.utils.get(user.guild.roles, name="Verified"))
        await ctx.send("``Sucessfully Verified!``")
      except AttributeError:
        await ctx.guild.create_role(name="Verified")
        await ctx.send("``Role 'Verified' didn't exist, so it was created! Please configure the role how you wish, and try again!``")
    else:
      await ctx.send(help_message)


@bot.command(name="verifytoggle")
@commands.has_permissions(administrator=True)
async def verifytoggle(ctx):
  Servers = Query()
  #db.insert({"id":ctx.guild.id,"verify":False})
  guild_search = db.search(Servers.id == ctx.guild.id)
  if (guild_search == []):
    db.insert({"id":ctx.guild.id,"verify":True})
    """if (guild_search[0]['verify'] == False):
      db.update({'verify': True}, Servers.id == ctx.guild.id)
      await ctx.send("Successfully Toggle to `False`, you can no longer verify")
    elif (guild_search[0]['verify'] == True):
      db.update({'verify': False}, Servers.id == ctx.guild.id)
      await ctx.send("Successfully Toggle to `True`, you can now verify")"""
    await ctx.send("Database entry created! Please run command again!")
  else:
    if (guild_search[0]['verify'] == False):
      db.update({'verify': True}, Servers.id == ctx.guild.id)
      await ctx.send("Successfully Toggle to `False`, you can no longer verify")
    elif (guild_search[0]['verify'] == True):
      db.update({'verify': False}, Servers.id == ctx.guild.id)
      await ctx.send("Successfully Toggle to `True`, you can now verify")


bot.run(TOKEN)
