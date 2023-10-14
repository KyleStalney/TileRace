import io
import os
import logging
import discord
import cleverbot

from random import randint
from discord.ext import commands
from urllib.parse import urlparse
from discord.commands import slash_command, Option

log = logging.getLogger(__name__)

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    @commands.has_role('Supports')
    async def speak(self, ctx, channel: Option(discord.TextChannel)):
        """Send a message in a given channel"""
        try:
            await ctx.respond(f"Enter the message for {channel.mention}", ephemeral=True)
            def check(m):
                return m.channel == ctx.channel and m.author == ctx.author
            msg = await self.bot.wait_for("message", check=check)
            await channel.send(msg.content)
            await msg.delete()
        except Exception as e:
            log.exception(f"speak,{type(e)} error occured,{e}")

    @commands.command()
    async def soos(self, ctx, message):
        """Talk to Soos using a Cleverbot API"""
        try:
            cb = cleverbot.Cleverbot(os.environ['CLEVERBOT_APIKEY'])
            reply = cb.say(message)
            await ctx.reply(reply)
        except Exception as e:
            log.error(f"soos,{type(e)} error occured,{e}")
