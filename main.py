import discord
import logging

from tilerace import TileRace

TOKEN='MTE2MDAwOTY1ODMzMzkzNzY3NQ.G6c8p4.zsr5nP73KYvDCvxuIEUfwP9FdrQADW_LysLsZs'
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
    await race.complete(reaction.message, reaction, user)

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
        await race.get_challenges(m)
    if m.content == '!roll_back':
        await race.roll_back(m)
    if m.content[0:6] == '!choice':
        await race.choice(m)


client.run(TOKEN)
