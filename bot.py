import discord
import logging

TOKEN=''
client = discord.Client(intents=discord.Intents.all())

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
        await signup(m)
    if m.content == '!list':
        await list(m)

signup_list = []

async def signup(message):
    signup_list.append(message.author)
    await message.add_reaction('\U00002705')
    log.info(f'signup,{message.author},added to signup_list')

async def list(message):
    mod_role = message.guild.get_role(690247456587382805)
    if mod_role not in message.author.roles:
        return
    await message.reply(signup_list.join('\n'))

client.run(TOKEN)
