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
        elif isinstance(error, discord.ext.commands.errors.CommandNotFound):
            ctx.send("Command not found!")      
        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':
                await ctx.send('I could not find that member. Please try again.')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please input your username or other argument and try again!")
        elif isinstance(error, hypixel.PlayerNotFoundException):
            await ctx.send("User does not exist!")
        elif isinstance(error, discord.errors.Forbidden):
            await ctx.send("Verified, but nick could not be changed due to you having higer permissions then me!")
        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)