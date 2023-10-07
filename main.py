import discord
import logging
import os
from tilerace import TileRace

TOKEN= os.environ['BOT_TOKEN']
client = discord.Client(intents=discord.Intents.all())
race = TileRace()

logging.basicConfig(
    format="%(asctime)s %(name)s:%(levelname)-8s %(message)s",
    filename="/var/log/tilemap.log"
)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
discord_log = logging.getLogger('discord')
discord_log.setLevel(logging.WARNING)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="!signup"))
    log.info(f'on_ready,{client.user},presence state set')

@client.event
async def on_reaction_add(reaction, user):
    kyle = client.get_emoji(1160014756040687626)
    if reaction.emoji != kyle:
        return
    channel = client.get_channel(1159942565408280597)
    if channel != reaction.message.channel:
        return
    await race.complete(reaction.message, user)

@client.event
async def on_message(m):
    if m.author == client.user:
        return
    if m.content == '!signup':
        await race.signup(m)
    if m.content == '!list':
        await race.list(m)
    if m.content == '!roll':
        await race.roll(m)
    if m.content == '!challenges':
        await m.reply(race.get_challenges(m))
    if m.content == '!roll_back':
        await race.roll_back(m)
    if m.content.startswith('!choice'):
        await race.choice(m)
    if m.content == '!positions':
        await race.get_position(m)


client.run(TOKEN)
