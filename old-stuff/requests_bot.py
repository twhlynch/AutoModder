import discord, subprocess
from discord import app_commands

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

with open(".token", "r") as f:
    bot_token = f.read().strip()
request_channel_id = 1135841466992820254
guild_id = 1135362081454043286

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=guild_id))
    print("Ready!")

@tree.command(
    name='mod',
    description='Request a modded APK (name, URL, or list of names/URLs)',
    guild=discord.Object(id=guild_id)
)
async def mod(interaction: discord.Interaction, app_list: str):
    user_id = interaction.user.id
    await interaction.response.send_message(f'Request for `{app_list}` submitted.')
    subprocess.Popen(["python", "download_apk.py", app_list])

client.run(bot_token)
