import discord
import logging

from .tilerace import TileRace

TOKEN=''
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
        await race.challenges(m.author)

client.run(TOKEN)
